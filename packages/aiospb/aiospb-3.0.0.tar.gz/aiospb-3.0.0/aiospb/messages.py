import abc
from dataclasses import asdict, dataclass, field
from typing import Any, Self

from . import Clock
from .data import Metric, MetricChange, MetricChangeRequest


class MessageContent(abc.ABC):
    """Interface of a message content"""

    @property
    def type(self) -> str:
        """Define content type"""
        value = self.__class__.__name__[:-7]
        return value.upper()

    @abc.abstractclassmethod
    def from_dict(cls, value: dict[str, Any]) -> Self:
        """Create content from a dict value"""

    @abc.abstractmethod
    def to_dict(self) -> dict[str, Any]:
        """Convert to plain dict"""


@dataclass
class NbirthContent(MessageContent):
    seq: int
    metrics: list[Metric]

    @classmethod
    def from_dict(cls, value: dict[str, Any]) -> Self:
        """Create content from a dict value"""
        metrics = [Metric.from_dict(value_) for value_ in value["metrics"]]
        return cls(value["seq"], metrics)

    def to_dict(self) -> dict[str, Any]:
        """Convert to plain dict"""
        return {
            "metrics": [metric.to_dict() for metric in self.metrics],
            "seq": self.seq,
        }


@dataclass
class NdeathContent(MessageContent):
    bd_seq: Metric

    @classmethod
    def from_dict(cls, value: dict[str, Any]) -> Self:
        """Create content from a dict value"""
        return cls(Metric.from_dict(value["metrics"][0]))

    def to_dict(self) -> dict[str, Any]:
        """Convert to plain dict"""
        return {
            "metrics": [self.bd_seq.to_dict()],
        }


@dataclass
class NdataContent(MessageContent):
    seq: int
    changes: list[MetricChange]

    @classmethod
    def from_dict(cls, value: dict[str, Any]) -> Self:
        """Create content from a dict value"""
        return cls(
            value["seq"],
            [MetricChange.from_dict(value_) for value_ in value["metrics"]],
        )

    def to_dict(self) -> dict[str, Any]:
        """Convert to plain dict"""
        return {
            "seq": self.seq,
            "metrics": [change.to_dict() for change in self.changes],
        }


@dataclass
class NcmdContent(MessageContent):
    requests: list[MetricChangeRequest]

    @classmethod
    def from_dict(cls, value: dict[str, Any]) -> Self:
        """Create content from a dict value"""
        return cls(
            [MetricChangeRequest.from_dict(value_) for value_ in value["metrics"]]
        )

    def to_dict(self) -> dict[str, Any]:
        """Convert to plain dict"""
        return {"metrics": [request.to_dict() for request in self.requests]}


@dataclass
class StateContent(MessageContent):
    online: bool

    @classmethod
    def from_dict(cls, value: dict[str, Any]) -> Self:
        """Create content from a dict value"""
        return cls(value["online"])

    def to_dict(self) -> dict[str, Any]:
        """Convert to plain dict"""
        return {"online": self.online}


@dataclass
class WarningContent(MessageContent):
    name: str
    description: str
    args: list = field(default=list)

    @classmethod
    def from_dict(cls, value: dict[str, Any]) -> Self:
        """Create content from a dict value"""
        return cls(value["name"], value["description"], value["args"])

    def to_dict(self) -> dict[str, Any]:
        """Convert to plain dict"""
        return asdict(self)


@dataclass(frozen=True)
class Message:
    topic: str
    content: MessageContent
    timestamp: int  # Time in ms when the message was sent

    _CONTENTS = {
        "STATE": StateContent,
        "NBIRTH": NbirthContent,
        "NDATA": NdataContent,
        "NDEATH": NdeathContent,
    }

    @property
    def component_name(self) -> str:
        if "/STATE/" in self.topic:
            return self.topic.split("/")[-1]
        else:
            groups = self.topic.split("/")
            return f"{groups[1]}/{groups[3]}"

    @property
    def content_type(self) -> str:
        if "/STATE/" in self.topic:
            return "STATE"
        else:
            return self.topic.split("/")[2]

    @classmethod
    def create(cls, component_name: str, content: MessageContent, clock: Clock) -> Self:
        if content.type == "STATE":
            topic = f"spBv1.0/STATE/{component_name}"
        else:
            group, node_name = component_name.split("/")
            topic = f"spBv1.0/{group}/{content.type}/{node_name}"
        return cls(topic, content, clock.now())

    @classmethod
    def from_payload(cls, payload: dict[str, Any]) -> Self:
        """Return the topic where the message should be sent"""
        content = payload.copy()
        topic = content.pop("topic")
        if "/STATE/" in topic:
            Content = StateContent
        else:
            Content = cls._CONTENTS[topic.split("/")[2]]

        timestamp = content.pop("timestamp")
        return cls(topic, Content.from_dict(content), timestamp)

    def get_payload(self) -> dict[str, Any]:
        """Return payload to be published"""
        payload = {
            "topic": self.topic,
            "timestamp": self.timestamp,
        }
        payload.update(self.content.to_dict())
        return payload
