"""
Types used for type checking the library. Client developers can use these if they like,
but they're mostly for our own sanity checks during development/testing.
"""
from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Any, Generic, Literal, TypedDict, TypeVar, Union

if TYPE_CHECKING:
    from pax25.applications import BaseApplication
    from pax25.interfaces.types import DummyInterfaceConfig, FileInterfaceConfig


class EmptyDict(TypedDict):
    """
    Empty dictionary.
    """


def empty_dict_factory() -> EmptyDict:
    """
    Returns a cast EmptyDict to satisfy the type checker.
    """
    return {}


# The StationConfig object should always be JSON-serializable. This way we'll eventually
# be able to use JSON for configuration files.


# This means that all interface configs will ALSO need to be JSON-serializable.
class StationConfig(TypedDict):
    """
    Configuration for a station.
    """

    name: str
    interfaces: dict[str, Union["FileInterfaceConfig", "DummyInterfaceConfig"]]


@dataclass(frozen=True)
class FullAddress:
    """
    Address information used for connections.
    """

    def __init__(self, name: str, ssid: int) -> None:
        """
        Force both values to be uppercase.
        """
        # We use the raw __setattr__ on object because this
        # is a frozen class and will not support direct assignment.
        object.__setattr__(self, "name", name.upper())
        object.__setattr__(self, "ssid", ssid)

    name: str
    ssid: int


# Payload type variable
P = TypeVar("P", bound=dict[str, Any] | EmptyDict)


@dataclass
class BaseFrameType(Generic[P]):
    """
    Base type for frames decoded by interfaces (and sent to them for transmission).
    """

    source: FullAddress
    destination: FullAddress
    payload: P
    command: str


@dataclass
class DisconnectFrame(BaseFrameType[EmptyDict]):
    """
    Disconnect instruction frame. Used to instruct the frame queue to
    perform a clean disconnection.
    """

    command: Literal["disconnect"] = field(default_factory=lambda: "disconnect")
    payload: EmptyDict = field(default_factory=empty_dict_factory)


@dataclass
class ConnectFrame(BaseFrameType[EmptyDict]):
    """
    Connect instruction frame. Indicates the desire for one station
    to connect to another on a particular address.
    """

    command: Literal["connect"] = field(default_factory=lambda: "connect")
    payload: EmptyDict = field(default_factory=empty_dict_factory)


@dataclass
class BeaconFrame(BaseFrameType[EmptyDict]):
    """
    Frame announcing the existence of a station.
    """

    command: Literal["beacon"] = field(default_factory=lambda: "beacon")
    payload: EmptyDict = field(default_factory=empty_dict_factory)


@dataclass
class HeartbeatFrame(BaseFrameType[EmptyDict]):
    """
    Heartbeat instruction. Basically a no-op that verifies that everything's OK
    with the connection.
    """

    command: Literal["heartbeat"] = field(default_factory=lambda: "heartbeat")
    payload: EmptyDict = field(default_factory=empty_dict_factory)


class MessagePayload(TypedDict):
    """
    Payload for message frame. This only has two keys-- one, the bytes being sent.
    The other is a flag for if this message is 'outbound'. In this context, outbound
    means that it skips any application processing and the frame queue should send it
    directly to the relevant interface.
    """

    bytes: bytes
    outbound: bool


@dataclass
class MessageFrame(BaseFrameType[MessagePayload]):
    """
    Message instruction. Delivers some bytes from one address to another.
    """

    command: Literal["message"] = field(default_factory=lambda: "message")


Frame = DisconnectFrame | ConnectFrame | HeartbeatFrame | MessageFrame | BeaconFrame


class ConnectionStats(TypedDict):
    """
    Statistics produced by connections.
    """

    transmitted_bytes: int
    received_bytes: int
    receive_buffer_length: int
    send_buffer_length: int


# Map for the station's application registry
ApplicationMap = dict[str, dict[str, "BaseApplication[Any]"]]
