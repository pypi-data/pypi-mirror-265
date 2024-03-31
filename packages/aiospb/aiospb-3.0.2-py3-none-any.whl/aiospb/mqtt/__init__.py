import abc
from dataclasses import dataclass
from typing import Any

from aiospb.messages import Message


class MqttConnectionError(Exception):
    ...


@dataclass
class Will:
    message: Message
    qos: int
    retain: bool


class MessageEncoder(abc.ABC):
    """Encode the message before sending it as payload in the message"""

    @abc.abstractmethod
    def encode(self, payload_dict: dict[str, Any]) -> str:
        """Convert a message to a payload"""

    @abc.abstractmethod
    def decode(self, payload: str) -> dict[str, Any]:
        """Convert payload to a message object"""


class MqttClient(abc.ABC):
    @abc.abstractmethod
    async def connect(self, component_name: str, will=Will):
        """Connect a component to MQTT server"""

    @abc.abstractmethod
    async def publish(self, topic: str, message: Message, qos: int, retain: bool):
        """Publish a message  to the topic"""

    @abc.abstractmethod
    async def deliver_message(self) -> Message:
        """Return a messsage recieved from the MQTT Server"""

    @abc.abstractmethod
    async def subscribe(self, topic: str, qos: int):
        """Subscribe the component to recieve messages from a topic"""

    @abc.abstractmethod
    async def disconnect(self):
        """Disconnect the client from the MQTT server"""
