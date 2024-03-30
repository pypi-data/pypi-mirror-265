from typing import TYPE_CHECKING, Callable, Dict, List, Optional, Tuple, Union

from ..typing import ModuleId

# class EventType(Enum):
#    START =     "start"
#    STOP =      "stop"
#    UPDATE =    "update"
#    TICK =      "tick"
#
if not TYPE_CHECKING:
    TEvent = str
    TSubEvent = str
    EventHandlerRegister = Union[
        Dict[str, Dict],
        Dict[str, Dict[str, Callable]],
        Dict[str, Dict[str, Dict[str, Callable]]],
    ]
else:
    from typing import Literal  # assume Python >=3.8 for typing check
    from typing import TypedDict  # assume Python >=3.8 for typing check

    TEvent = Literal["start", "stop", "update", "tick", "external"]  # >= 3.8
    TSubEvent = str

    class EventHandlerRegister(TypedDict):
        start: Dict[ModuleId, Dict[None, Callable]]
        stop: Dict[ModuleId, Dict[None, Callable]]
        update: Dict[ModuleId, Dict[None, Callable]]
        tick: Dict[ModuleId, Dict[Optional[TSubEvent], Callable]]
        external: Dict[ModuleId, Dict[TSubEvent, Callable[[Tuple[TSubEvent, str]], str]]]

    # class DoubleIndex(UserDict):
    #    def __getitem__(self, xy):
    #        if xy in self.data.keys():
    #            return self.data[xy]
    #        x,y=xy
    #        if x is None:
    #            return [ self.data[(xx,y)] for xx, yy in self.data.keys() if yy==y ]
    #        if y is None:
    #            return [ self.data[(x,yy)] for xx, yy in self.data.keys() if xx==x ]
