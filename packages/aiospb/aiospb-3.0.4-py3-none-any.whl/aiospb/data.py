from dataclasses import dataclass, field, asdict
from enum import Enum
from typing import Any, Mapping, Self


class DataType(Enum):
    Unknown = 0
    Int8 = 1
    Int16 = 2
    Int32 = 3
    Int64 = 4
    UInt8 = 5
    UInt16 = 6
    UInt32 = 7
    UInt64 = 8
    Float = 9
    Double = 10
    Boolean = 11
    String = 12
    DateTime = 13
    Text = 14
    UUID = 15
    DataSet = 16
    Bytes = 17
    File = 18
    Template = 19
    PropertySet = 20
    PropertySetList = 21
    Int8Array = 22
    Int16Array = 23
    Int32Array = 24
    Int64Array = 25
    UInt8Array = 26
    UInt16Array = 27
    UInt32Array = 28
    UInt64Array = 29
    FloatArray = 30
    DoubleArray = 31
    BooleanArray = 32
    StringArray = 33
    DateTimeArray = 34


ValueType = bool | int | float | str | None


@dataclass(frozen=True)
class PropertyValue:
    data_type: DataType
    value: ValueType

    @classmethod
    def from_dict(cls, payload):
        return cls(
            DataType[payload["type"]],
            None if payload.get("is_null") else payload["value"],
        )

    def to_dict(self):
        result: dict[str, ValueType] = {"type": self.data_type.name}
        if self.value is None:
            result["is_null"] = True
        else:
            result["value"] = self.value
        return result


class QualityOptions(Enum):
    BAD = 0
    GOOD = 192
    STALE = 500


@dataclass(frozen=True)
class QualityValue(PropertyValue):
    """Standard property of metric"""

    def __init__(self, value: QualityOptions):
        if value not in QualityOptions:
            raise ValueError(f"The value {value} is not valid")
        super().__init__(DataType.Int32, value.value)


@dataclass
class MetricChange:
    timestamp: int
    value: int | bool | str | float | None
    data_type: DataType
    alias: int | None = None
    metric_name: str = ""
    properties: dict[str, PropertyValue] = field(default_factory=dict)
    is_historical: bool = False

    @classmethod
    def from_dict(cls, dict_value: dict[str, Any]) -> Self:
        """Create metric from dict definition"""

        properties = {
            key: PropertyValue.from_dict(value)
            for key, value in dict_value.get("properties", {}).items()
        }
        alias = dict_value.get("alias")
        metric_name = "" if alias is not None else dict_value.get("name", "")
        value = None if dict_value.get("is_null") else dict_value["value"]
        is_historical = True if dict_value.get("is_historical") else False

        return cls(
            dict_value["timestamp"],
            value,
            DataType[dict_value["dataType"]],
            alias,
            metric_name,
            properties,
            is_historical,
        )

    def to_dict(self) -> dict[str, ValueType]:
        """Create dict from metric change object"""

        result = {"timestamp": self.timestamp, "dataType": self.data_type.name}
        if self.alias:
            result["alias"] = self.alias
        else:
            result["name"] = self.metric_name
        if self.value is None:
            result["is_null"] = True
        else:
            result["value"] = self.value
        properties = {key: value.to_dict() for key, value in self.properties.items()}
        if properties:
            result["properties"] = properties

        if self.is_historical:
            result["is_historical"] = True

        return result

    # def update_metric(self, metric: Metric) -> Metric:
    #     """Update metric values from the change"""

    #     if self.timestamp <= metric.timestamp or self.is_historical:
    #         # Metric can not be updated with a previous change
    #         return metric

    #     if not self.properties and self.value == metric.value:
    #         return metric

    #     properties = {}
    #     for key, value in metric.properties.items():
    #         properties[key] = (
    #             value if key not in self.properties else self.properties[key]
    #         )

    #     return Metric(
    #         metric.name,
    #         self.timestamp,
    #         self.value,
    #         metric.data_type,
    #         properties,
    #         metric.alias,
    #         metric.is_transient,
    #     )


@dataclass(frozen=True)
class Metric:
    """Metric owned by a edge node or device"""

    name: str
    timestamp: int
    value: int | bool | str | float | None
    data_type: DataType
    properties: dict[str, PropertyValue] = field(default_factory=dict)
    alias: int | None = None
    is_transient: bool = False

    @classmethod
    def from_dict(cls, value: dict[str, Any]):
        properties = {
            key: PropertyValue.from_dict(value_)
            for key, value_ in value.get("properties", {}).items()
        }

        metric_value = None if value.get("is_null") else value.get("value")
        return cls(
            value.get("name", ""),
            value["timestamp"],
            metric_value,
            DataType[value["dataType"]],
            properties,
            value.get("alias", None),
            value.get("is_transient", False),
        )

    def to_dict(self):
        result = {
            "name": self.name,
            "timestamp": self.timestamp,
            "dataType": self.data_type.name,
        }
        if self.value is None:
            result["is_null"] = True
        else:
            result["value"] = self.value

        if self.is_transient:
            result["is_transient"] = True

        if self.alias:
            result["alias"] = self.alias

        properties = {}
        for key, value in self.properties.items():
            properties[key] = value.to_dict()

        if properties:
            result["properties"] = properties

        return result

    def compare(self, metric: Self) -> MetricChange | None:
        if metric.name != self.name:
            raise ValueError("Metrics has diferent names!!")

        if set(metric.properties.keys()) != set(self.properties.keys()):
            raise ValueError("Properties definitions has changed")

        if metric.timestamp <= self.timestamp:
            return

        if metric.value == self.value and metric.properties == self.properties:
            return

        properties = {}
        for key, value in metric.properties.items():
            if self.properties[key] != value:
                properties[key] = value

        alias = self.alias
        name = "" if alias else self.name
        return MetricChange(
            metric.timestamp, metric.value, self.data_type, alias, name, properties
        )


@dataclass(frozen=True)
class MetricChangeRequest:
    timestamp: int
    value: ValueType
    data_type: DataType
    metric_name: str = ""
    alias: int | None = None

    def to_dict(self):
        result = {
            "timestamp": self.timestamp,
            "value": self.value,
            "dataType": self.data_type.name,
        }
        if self.alias is not None:
            result["alias"] = self.alias
        else:
            result["name"] = self.metric_name
        return result

    @classmethod
    def from_dict(cls, payload: dict[str, Any]) -> Self:
        return cls(
            payload["timestamp"],
            payload["value"],
            DataType[payload["dataType"]],
            payload.get("name", ""),
            payload.get("alias"),
        )
