import asyncio
from typing import Dict, List, Optional, Union

import nats
from confluent_kafka import Consumer, Producer
from nats.errors import Error as NatsError

import superstream.manager as manager
from superstream.client import _Client
from superstream.constants import (
    _CLIENT_RECONNECTION_UPDATE_SUBJECT,
    _NATS_INFINITE_RECONNECT_ATTEMPTS,
    _SUPERSTREAM_INTERNAL_USERNAME,
)
from superstream.exceptions import ErrGenerateConnectionId
from superstream.interceptors import _ConsumerInterceptor, _ProducerInterceptor
from superstream.types import ClientConfig, ClientReconnectionUpdateReq, Option
from superstream.utils import _name


async def _initialize_nats_connection(token: str, host: Union[str, List[str]]):
    global _broker_connection, _js_context, _nats_connection_id

    async def on_reconnected():
        global _nats_connection_id
        local_connection_id = ""
        for _, client in manager._clients.items():
            try:
                local_connection_id = await manager._generate_nats_connection_id()
                payload = (
                    ClientReconnectionUpdateReq(new_nats_connection_id=local_connection_id, client_id=client.client_id)
                    .model_dump_json()
                    .encode()
                )
                await manager._request(_CLIENT_RECONNECTION_UPDATE_SUBJECT, payload)
            except ErrGenerateConnectionId as e:
                await client._handle_error(
                    f"{_name(_initialize_nats_connection)} at {_name(manager._generate_nats_connection_id)}: {e!s}"
                )
                return
            except Exception as e:
                await client._handle_error(f"{_name(_initialize_nats_connection)} at broker connection request: {e!s}")
                return
        _nats_connection_id = local_connection_id

    async def error_cb(e: NatsError):
        """
        Error callback for NATS connection errors.
        It does nothing. Its purpose is to override the NATS default error callback that prints the error to the console on every reconnect attempt.
        """
        if e is None:
            return
        critical_errors = [
            "invalid checksum",
            "nats: maximum account",
            "authorization violation",
        ]
        for error in critical_errors:
            if error.lower() in str(e).lower():
                raise e

    try:
        manager._broker_connection = await nats.connect(
            max_reconnect_attempts=_NATS_INFINITE_RECONNECT_ATTEMPTS,
            reconnect_time_wait=1.0,
            user=_SUPERSTREAM_INTERNAL_USERNAME,
            password=token,
            servers=host,
            reconnected_cb=on_reconnected,
            error_cb=error_cb,
        )
        manager._js_context = manager._broker_connection.jetstream()
        manager._nats_connection_id = await manager._generate_nats_connection_id()
    except Exception as exception:
        if "nats: maximum account" in str(exception):
            raise Exception(
                "Cannot connect with superstream since you have reached the maximum amount of connected clients"
            ) from exception
        elif "invalid checksum" in str(exception):
            raise Exception("Error connecting with superstream: unauthorized") from exception
        else:
            raise Exception(f"Error connecting with superstream: {exception!s}") from exception


async def init_async(token: str, host: str, config: Dict, opts: Option) -> int:
    client_type = "kafka"
    conf = _confluent_config_handler(client_type, config)
    new_client = _Client(config=conf, learning_factor=opts.learning_factor)

    if manager._broker_connection is None:
        await _initialize_nats_connection(token, host)

    new_client.config.servers = opts.servers
    new_client.config.consumer_group_id = conf.consumer_group_id
    await new_client.register_client()

    manager._clients[new_client.client_id] = new_client

    await new_client.subscribe_updates()

    # ruff: noqa: RUF006
    asyncio.create_task(new_client.report_clients_update())

    # _configure_interceptors(new_config, new_client)
    return new_client.client_id


def _confluent_config_handler(client_type: str, confluent_config: dict) -> ClientConfig:
    acks = "WaitForAll"
    if "acks" in confluent_config:
        acks = {
            0: "NoResponse",
            1: "WaitForLocal",
            -1: "WaitForAll",
        }.get(confluent_config["acks"], "")

    compression_level = "CompressionLevelDefault"
    if 'compression.type' in confluent_config:
        compression_level = {
            0: "CompressionNone",
            1: "CompressionGZIP",
            2: "CompressionSnappy",
            3:"CompressionLz4",
            4: "CompressionZSTD",
        }.get(confluent_config["compression.type"], "CompressionLevelDefault")
    
    consumer_auto_offset = confluent_config.get("auto.offset.reset")
    consumer_auto_offset_int = -1
    if consumer_auto_offset is None:
        consumer_auto_offset = "earliest"
    else:
        if consumer_auto_offset == "earliest" or consumer_auto_offset == "smallest":
            consumer_auto_offset_int= -2
        elif consumer_auto_offset == "latest" or consumer_auto_offset == "largest":
            consumer_auto_offset_int = -1

    conf = ClientConfig(
        client_type=client_type,
        servers=confluent_config.get("bootstrap.servers") or "",
        producer_max_messages_bytes=confluent_config.get("message.max.bytes") or 1000000,
        producer_required_acks=acks,
        producer_timeout=confluent_config.get("request.timeout.ms") or 30000,
        producer_retry_max=confluent_config.get("message.send.max.retries") or 2147483647,
        producer_retry_backoff=confluent_config.get("retry.backoff.ms") or 100,
        producer_return_errors=confluent_config.get("delivery.report.only.error") or True,
        producer_flush_max_messages=confluent_config.get("queue.buffering.max.messages") or 100000,
        producer_compression_level=compression_level,
        # consumer properties
        consumer_group_id=confluent_config.get("group.id") or "",
        consumer_fetch_min=confluent_config.get("fetch.min.bytes") or 1,
        consumer_fetch_default=confluent_config.get("fetch.message.max.bytes") or 1048576,
        consumer_max_wait_time=confluent_config.get("fetch.wait.max.ms") or 500,
        consumer_return_errors=False, # doesn't support in confluent python sdk 
        consumer_offset_auto_commit_enable=confluent_config.get("enable.auto.commit") or True,
        consumer_offset_auto_commit_interval=confluent_config.get("auto.commit.interval.ms") or 60000,
        consumer_offsets_initial=consumer_auto_offset_int or -1,
        consumer_group_session_timeout=confluent_config.get("session.timeout.ms") or 45000,
        consumer_group_heart_beat_interval=confluent_config.get("heartbeat.interval.ms") or 3000,
        consumer_group_rebalance_timeout=confluent_config.get("max.poll.interval.ms") or 300000,
    )

    return conf


async def _init_producer(
    token: str, host: str, config: Dict, opts: Option, producer: Optional[Producer] = None
) -> Producer:
    client_id = await init_async(token, host, config, opts)
    return _ProducerInterceptor(client_id, config)


async def _init_consumer(
    token: str, host: str, config: Dict, opts: Option, consumer: Optional[Consumer] = None
) -> Consumer:
    client_id = await init_async(token, host, config, opts)
    return _ConsumerInterceptor(client_id, config)


def init(
    token: str,
    host: str,
    config: Dict,
    opts: Option,
    producer: Optional[Producer] = None,
    consumer: Optional[Consumer] = None,
) -> Union[Producer, Consumer]:
    if producer is None and consumer is None:
        raise Exception("superstream: either producer or consumer should be provided")
    try:
        if producer is not None:
            return asyncio.run(_init_producer(token, host, config, opts, producer))
        return asyncio.run(_init_consumer(token, host, config, opts, consumer))
    except Exception as e:
        print("superstream: ", str(e))
        return producer or consumer
