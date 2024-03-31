"""Main components of sparkplug standard"""
import abc
import asyncio
import logging
from functools import singledispatchmethod
from queue import Queue
from typing import Literal

from aiospb.mqtt import MqttClient, Will

from . import Clock, RealClock
from . import messages as m
from .data import DataType, Metric, MetricChange, MetricChangeRequest, ValueType

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

_NODES_STATES = Literal["online", "offline", "publishing"]


class DeviceConnectionError(Exception):
    ...


class DeviceDriver(abc.ABC):
    """Connection to real devices or direct interfaces"""

    @abc.abstractmethod
    async def load_metrics(self) -> list[Metric]:
        """Load metrics from system"""

    @abc.abstractmethod
    async def scan_metrics(self, aliases: list[int] | None = None) -> list[Metric]:
        """Scan the device for last state of metrics"""

    @abc.abstractmethod
    async def write_metric(self, request: MetricChangeRequest) -> MetricChange:
        """Write metric to system"""


class HistoricalStore(abc.ABC):
    """Store historical changes to retrieve when host application is online"""

    @abc.abstractmethod
    async def save(self, changes: list[MetricChange]):
        """Save all change metrics of a scan"""

    @abc.abstractmethod
    async def load(self) -> list[MetricChange]:
        """Load all historical metric changes"""

    @abc.abstractmethod
    async def has_data(self) -> bool:
        """Has data stored?"""

    @abc.abstractmethod
    async def clear(self):
        """Clear content of historical"""


class OnmemHistoricalStore(HistoricalStore):
    """Store historical changes on memory. Not recomemded if host will be stopped for a long time"""

    def __init__(self):
        self._changes = []

    async def save(self, changes: list[MetricChange]):
        self._changes.extend(changes)

    async def load(self) -> list[MetricChange]:
        changes = [
            MetricChange(
                change.ts,
                change.value,
                change.data_type,
                change.alias,
                change.metric_name,
                change.properties,
                is_historical=True,
            )
            for change in self._changes
        ]
        self._changes.clear()
        return changes

    async def has_data(self):
        return bool(self._changes)

    async def clear(self):
        self._changes.clear()


class EdgeNode:
    """Gateway connected to mqtt and to one or more hardware devices"""

    def __init__(
        self,
        name: str,
        group_name: str,
        mqtt_client: MqttClient,
        device_driver: DeviceDriver,
        historical_store: HistoricalStore | None = None,
        primary_hostname: str = "",
        scan_rate: int = 60000,  # Scan every minute
        clock: Clock | None = None,
    ):
        self._name = f"{group_name}/{name}"
        self._primary_hostname = primary_hostname
        self._clock = clock if clock else RealClock()

        self._driver = device_driver
        self._client = mqtt_client
        self._historical_store = (
            historical_store if historical_store else OnmemHistoricalStore()
        )

        self._seq = 255
        self._inner_metrics = {
            "bdSeq": m.Metric(
                "bdSeq", self._clock.now(), 255, data_type=DataType.Int64
            ),
            "Node Control/Rebirth": m.Metric(
                "Node Control/Rebirth",
                self._clock.now(),
                False,
                data_type=DataType.Boolean,
            ),
            "Node Control/Reboot": m.Metric(
                "Node Control/Reboot",
                self._clock.now(),
                False,
                data_type=DataType.Boolean,
            ),
            "Node Control/Scan Rate": m.Metric(
                "Node Control/Scan Rate",
                self._clock.now(),
                scan_rate,
                data_type=DataType.Int64,
            ),
        }
        self._metrics_by_name: dict[str, Metric] = {}
        self._metrics_by_alias: dict[int, Metric] = {}

        self._incomings_task = None
        self._outcomings_task = None
        self._scanning_task = None
        self._changes_queue = Queue()
        self._state: _NODES_STATES = "offline"

    @property
    def name(self) -> str:
        """Return name of edge of network node"""
        return self._name.split("/")[1]

    @property
    def group_name(self) -> str:
        """Return the name of the group of nodes it beyong to"""
        return self._name.split("/")[0]

    @property
    def state(self) -> _NODES_STATES:
        """Return the current state of node"""
        return self._state

    @property
    def primary_hostname(self) -> str:
        """Name of primary host application"""
        return self._primary_hostname

    @property
    def metrics(self) -> dict[str, Metric]:
        """Return a dict with all the metrics of the node"""
        metrics = self._inner_metrics.copy()
        metrics.update(self._metrics_by_name)
        return metrics

    def clear_metrics(self):
        """Remove all not internal metrics"""
        self._metrics_by_name.clear()
        self._metrics_by_alias.clear()

    def _add_metric(self, metric: Metric):
        """Add new metric in node"""
        self._metrics_by_name[metric.name] = metric
        if metric.alias:
            self._metrics_by_alias[metric.alias] = metric

    def _get_seq(self):
        self._seq = self._seq + 1 if self._seq != 255 else 0
        return self._seq

    def _get_bd_seq(self):
        bd_seq = self._inner_metrics["bdSeq"]
        value = int(bd_seq.value) + 1 if bd_seq.value != 255 else 0
        bd_seq = Metric("bdSeq", self._clock.now(), value, data_type=DataType.Int64)
        self._inner_metrics["bdSeq"] = bd_seq
        return value

    async def _publish_data_contents(self):
        while True:
            if self._state == "publishing":
                # Publish Ndata messages
                changes = []
                while not self._changes_queue.empty():
                    changes.append(self._changes_queue.get())

                if not changes:
                    await self._clock.asleep(0)
                    continue

                logger.info(f"Publishing {len(changes)} changes from node {self.name}")
                await self._client.publish(
                    m.Message.create(
                        self._name,
                        m.NdataContent(self._get_seq(), changes),
                        self._clock,
                    ),
                    qos=0,
                    retain=False,
                )
            else:
                await self._clock.asleep(0)

    async def _scan_metrics(self):
        scan_rate = int(self._inner_metrics["Node Control/Scan Rate"].value)
        while True and scan_rate:
            now = self._clock.now()
            next_scan_time = (now // scan_rate + 1) * scan_rate
            await self._clock.asleep((next_scan_time - now) / 1000)

            metrics = await self._driver.scan_metrics()

            changes = []
            for metric in metrics:
                old_metric = self._metrics_by_name[metric.name]
                change = old_metric.compare(metric)
                if change:
                    self._add_metric(metric)
                    changes.append(change)

            logger.debug(
                f"{self._name} has detected {len(changes)} changes to be published"
            )

            if self._state == "publishing":
                if await self._historical_store.has_data():
                    logger.debug(f"Getting historical data from node {self.name}")
                    for change in await self._historical_store.load():
                        self._changes_queue.put(change)
                    await self._historical_store.clear()

                for change in changes:
                    self._changes_queue.put(change)
            else:
                logger.debug(f"{self._name} is storing changes in historical")
                await self._historical_store.save(changes)

    async def _handle_incomming_messages(self):
        while True:
            message: m.Message = await self._client.deliver_message()
            await self._handle_content(message.content)

    @singledispatchmethod
    async def _handle_content(self, content: m.MessageContent):
        raise NotImplementedError(
            f"Content type {type(content)} is not managed by a Edge Node"
        )

    @_handle_content.register
    async def _handle_state_content(self, content: m.StateContent):
        if content.online:
            self._state = "publishing"
            await self._publish_birth_certificate()
        else:
            self._state = "online"

    @_handle_content.register
    async def _handle_command_content(self, content: m.NcmdContent):
        logger.debug(f"{self._name} has recieved command {content}")
        for request in content.requests:
            if request.metric_name == "Node Control/Rebirth" and request.value is True:
                self._state = "online"  # Stops sending data
                # topic = f"spBv1.0/{self.group_name}/NDATA/{self.name}"
                await self._client.publish(
                    m.Message.create(
                        self._name,
                        m.NdataContent(
                            self._get_seq(),
                            [
                                MetricChange(
                                    self._clock.now(),
                                    True,
                                    DataType.Boolean,
                                    metric_name="Node Control/Rebirth",
                                )
                            ],
                        ),
                        self._clock,
                    ),
                    qos=0,
                    retain=False,
                )
                await self._publish_birth_certificate()
            if request.metric_name == "Node Control/Reboot" and request.value is True:
                await self.terminate_session()
                await self.establish_session()
            else:
                loop = asyncio.get_event_loop()
                loop.create_task(self._process_metric_change(request))

    async def _process_metric_change(self, request: MetricChangeRequest):
        change = await self._driver.write_metric(request)
        logger.debug(f"{self._name} has procesed change {change}")

        metric = (
            self._metrics_by_alias[change.alias]
            if change.alias
            else self._metrics_by_name[change.metric_name]
        )

        self._add_metric(
            Metric(
                metric.name,
                change.timestamp,
                change.value,
                metric.data_type,
                metric.properties,
                metric.alias,
                metric.is_transient,
            )
        )
        self._changes_queue.put(change)

    async def _publish_birth_certificate(self):
        self.clear_metrics()
        metrics = await self._driver.load_metrics()

        for metric in metrics:
            self._add_metric(metric)

        logger.debug(
            f"{self._name} publishes birth certificate with {len(metrics)} metrics"
        )
        await self._client.publish(
            m.Message.create(
                self._name,
                m.NbirthContent(self._get_seq(), list(self.metrics.values())),
                self._clock,
            ),
            qos=0,
            retain=False,
        )
        self._state = "publishing"

    async def establish_session(self):
        """Create a session"""

        self._get_bd_seq()
        await self._client.connect(
            self._name,
            will=Will(
                m.Message.create(
                    self._name,
                    m.NdeathContent(self._inner_metrics["bdSeq"]),
                    self._clock,
                ),
                0,
                False,
            ),
        )
        await self._client.subscribe("spBv1.0/STATE/+", qos=1)
        await self._client.subscribe(
            f"spBv1.0/{self.group_name}/NCMD/{self.name}", qos=0
        )

        self._state = "online"

        self._outcomings_task = asyncio.create_task(self._publish_data_contents())
        self._incomings_task = asyncio.create_task(self._handle_incomming_messages())
        self._scanning_task = asyncio.create_task(self._scan_metrics())

    async def terminate_session(self):
        """Finish a session cleanly, leaving the node clean"""
        if self._outcomings_task is not None:
            self._outcomings_task.cancel()
            self._outcomings_task = None
        if self._scanning_task is not None:
            self._scanning_task.cancel()
            self._scanning_task = None
        if self._incomings_task is not None:
            self._incomings_task.cancel()
            self._incomings_task = None

        self._state = "offline"
        if self._client:
            logger.info(f"Publishing clean Death Certificate from node {self.name}")
            await self._client.publish(
                m.Message.create(
                    self._name,
                    m.NdeathContent(self._inner_metrics["bdSeq"]),
                    self._clock,
                ),
                0,
                False,
            )

        await self._client.disconnect()
