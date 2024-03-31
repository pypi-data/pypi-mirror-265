import asyncio
from typing import Callable, Coroutine
import logging

from aiospb import Clock, RealClock
from aiospb.data import Metric, MetricChange, MetricChangeRequest, ValueType
from aiospb.groups import MqttServer
from aiospb.messages import (
    Message,
    NcmdContent,
    StateContent,
    WarningContent,
)
from aiospb.mqtt import Will

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class HostApplication:
    """Implementation of Host Application"""

    def __init__(
        self,
        hostname: str,
        mqtt_server: MqttServer,
        *node_groups: str,
        clock: Clock | None = None,
        max_delay: int = 10,
    ):
        if not node_groups:
            raise ValueError("Not node groups to listen are defined")
        self._groups = node_groups

        self._client = mqtt_server.create_client()
        self._hostname = hostname
        self._callbacks = {}
        self._nodes = {}
        self._clock = clock if clock else RealClock()
        self._state = "offline"
        self._listen_nodes = None
        self._max_delay = max_delay
        self._node_sequences = {}

    @property
    def hostname(self) -> str:
        """Name of the host application"""
        return self._hostname

    @property
    def state(self):
        return self._state

    async def establish_session(self):
        """Init session to listen edge nodes"""

        await self._client.connect(
            self._hostname,
            will=Will(
                Message.create(self._hostname, StateContent(False), self._clock),
                1,
                True,
            ),
        )
        if self._groups:
            for group in self._groups:
                await self._client.subscribe(f"spBv1.0/{group}/#", qos=0)
        else:
            await self._client.subscribe("spBv1.0/+/+/+/#", qos=0)

        await self._client.publish(
            Message.create(self._hostname, StateContent(True), self._clock),
            qos=1,
            retain=True,
        )
        logger.debug(f'Host application "{self._hostname}" has established session')
        self._listen_nodes = asyncio.create_task(self._recieve_node_messages())

    def done(self):
        return self._listen_nodes is None or self._listen_nodes.done()

    def listen_nodes(
        self,
        callback: Callable[[Message], Coroutine[None, None, None]],
        node_filter: str | None = None,
    ) -> None:
        """Add one callable observer when it rece"""
        if node_filter not in self._callbacks:
            self._callbacks[node_filter] = []

        self._callbacks[node_filter].append(callback)

    async def _recieve_node_messages(self):
        while True:
            message: Message = await self._client.deliver_message()
            delay = (self._clock.now() - message.timestamp) / 1000
            await self._notify(message)
            logger.debug(
                f"Host app '{self._hostname}' has recieved {message.content_type} with delay of {delay} s"
            )

            if delay > self._max_delay:
                await self._notify(
                    Message.create(
                        message.component_name,
                        WarningContent(
                            "ExcessOfDelay",
                            f"Delay (seconds) is over max {self._max_delay} s",
                            [delay],
                        ),
                        self._clock,
                    )
                )
                logger.debug(
                    f'Host app "{self._hostname}" has notified warning by delay'
                )

    async def _notify(self, message):
        awaitables = [callback(message) for callback in self._callbacks[None]]
        node_name = message.component_name
        if node_name in self._callbacks:
            awaitables.extend(
                [callback(message) for callback in self._callbacks[node_name]]
            )
        await asyncio.gather(*awaitables)

    async def request_change_to_metrics(
        self, node_name: str, *change_requests: MetricChangeRequest
    ):
        """Request changes to metrics"""
        await self._client.publish(
            Message.create(node_name, NcmdContent(list(change_requests)), self._clock),
            qos=0,
            retain=False,
        )

    async def terminate_session(self):
        """Close cleanly a session"""
        if self._listen_nodes:
            self._listen_nodes.cancel()

        await self._client.publish(
            Message.create(self._hostname, StateContent(False), self._clock),
            qos=1,
            retain=True,
        )
        await self._client.disconnect()
        logger.debug(
            f'Host application "{self._hostname}" has cleanly terminated session'
        )
