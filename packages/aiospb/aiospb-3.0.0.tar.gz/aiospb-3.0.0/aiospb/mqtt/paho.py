from typing import Any

import aiomqtt

from ..messages import (
    Message,
)
from . import MessageEncoder, MqttClient, MqttConnectionError, Will


class PahoMqttClient(MqttClient):
    def __init__(
        self,
        config: dict[str, Any],
        encoder: MessageEncoder,
    ):
        self._config = config
        self._client = None
        self._client_id = None
        self._encoder = encoder

    async def connect(self, component_name: str, will: Will):
        payload = self._encoder.encode(will.message.get_payload())
        will_ = aiomqtt.Will(
            will.message.topic, payload, qos=will.qos, retain=will.retain
        )
        self._client_id = component_name

        tls_pars = None
        if self._config.get("ca_certs"):
            tls_pars = aiomqtt.TLSParameters(ca_certs=self._config["ca_certs"])

        self._client = aiomqtt.Client(
            self._config["hostname"],
            int(self._config["port"]),
            identifier=component_name,
            username=self._config["username"],
            password=self._config["password"],
            will=will_,
            tls_params=tls_pars,
            keepalive=30,
        )

        await self._client.__aenter__()  # Connect with aiomqtt

    async def publish(self, message: Message, qos: int, retain: bool):
        if not self._client or not self._client_id:
            raise MqttConnectionError("Client not connected to Mqtt Server")

        payload = self._encoder.encode(message.get_payload())
        await self._client.publish(message.topic, payload, qos=qos, retain=retain)

    async def subscribe(self, topic: str, qos: int):
        if not self._client or not self._client_id:
            raise MqttConnectionError("Client not connected to Mqtt Server")

        await self._client.subscribe(topic, qos=qos)

    async def deliver_message(self) -> Message:
        # if self._client is None:
        #     raise MqttConnectionError(f"Client is not connected, so no messages")

        message = await anext(self._client.messages)

        payload = self._encoder.decode(message.payload.decode())
        payload["topic"] = message.topic.value
        return Message.from_payload(payload)

    async def disconnect(self):
        if self._client is None:
            return

        await self._client.__aexit__(None, None, None)
