"""
Event handler registration using ``@on`` decorator.
"""

import logging
from enum import IntEnum
from functools import partial
from typing import (Callable, Dict, Iterable, List, Optional, Tuple,
                    Union)

from ..exceptions import (EventException, EventRegisterAlreadyInstantiated,
                          EventRegisterNotYetInstantiated, UnsupportedEvent)
from ..typing import IModule, ModuleId
from ..utils import canonical_id_from_str, class_ids, instance_ids
from .typing import EventHandlerRegister, TEvent, TSubEvent

logger = logging.getLogger(__name__)


# jediný coupling Gateway a uživatelských modulů je pomocí
# eventů: aktivně a configu: pasivně (updating pointer)
class EventRegister:
    _ehandlers: EventHandlerRegister
    _modules: Dict[ModuleId, IModule]
    instantiated: bool

    def __init__(self):
        self._ehandlers: EventHandlerRegister = {
            "start": {},
            "stop": {},
            "update": {},
            "tick": {},
            "external": {},
        }
        self.instantiated = False

    @staticmethod
    def from_existing(register: "EventRegister"):
        x = __class__()
        x._ehandlers = register._ehandlers
        return x

    # TODO do @overload with possible arguments and return types of eventn+args when possible
    # when Python >= 3.8 for Literal
    def on(self, eventn: TEvent, subevent: Optional[TSubEvent] = None):
        """Decorator for event handler registration.

        Synopsis: ``on(event[,subevent])``

        Supported events: ``tick``, ``update``, ``start``, ``stop``, ``external``.

        ============= =======================================================================
            event                   description
        ============= =======================================================================
         ``update``    gateway's configuration was updated
         ``tick``      timer has ticked (timer configured in JSON config)
         ``start``     `Gateway` has started
         ``stop``      `Gateway` is stopping, please end module's action as soon as possible
         ``external``  a registered command was issued using socket IPC
        ============= =======================================================================

        ================================= ===================================================================
                      decorator                      description
        ================================= ===================================================================
         ``@on("update")``                gateway's configuration was updated
         ``@on("tick" [,timer_id])``      timer tick (configured in JSON)
         ``@on("start")``                 `Gateway` has started (via :meth:`~uun_iot.Gateway.Gateway.start`)
         ``@on("stop")``                  `Gateway` is stopping (via :meth:`~uun_iot.Gateway.Gateway.stop`)
         ``@on("external", cmd_name)``    an external command was issued using socket IPC
        ================================= ===================================================================

            - ``@on("tick" [,timer_id] )`` can take another argument to specify the timer id
              (see ``gateway.moduleTimers`` key in configuration JSON), ie. ``on(fn)``,
              or  ``on(fn, "timerId")`` with :func:`fn` being the handler function.

            - ``@on("external", cmd_name)`` decorator takes another argument to
              specify the name of the registered command

        Handlers registered for the corresponding event with this decorator will be
        called on corresponding event by :class:`~uun_iot.Gateway.Gateway` or
        :class:`~uun_iot.Gateway.Config` objects. Passed arguments are different for each
        event and the methods have to take these arguments. Note: ``self`` denotes
        method's module instance, `origin` indicates which module initiates the event

        ============= ======================= ===================================
            event       handler synopsis             origin
        ============= ======================= ===================================
         ``update``    ``handler(self)``        :class:`~uun_iot.Gateway.Config`
         ``tick``      ``handler(self)``        :class:`~uun_iot.Gateway.Gateway`
         ``start``     ``handler(self, evs)``   :class:`~uun_iot.Gateway.Gateway`
         ``stop``      ``handler(self)``        :class:`~uun_iot.Gateway.Gateway`
         ``external``  ``handler(self, msg)``   :class:`~uun_iot.Gateway.Gateway`
        ============= ======================= ===================================

        where

            - ``evs = (g.runev, g.stopev)`` is a tuple of :class:`threading.Event`
              attributes :attr:`~uun_iot.Gateway.Gateway.runev` and
              :attr:`~uun_iot.Gateway.Gateway.stopev`. Here, ``g`` is the corresponding
              :class:`~uun_iot.Gateway.Gateway` instance.
            - ``msg`` is a tuple ``msg=(cmd, rest_msg)``, where cmd is the issued command
              and ``rest_msg`` is the rest of the message received by socket IPC

        Warning:
            
            When the Gateway invokes @start and @stop handlers, it runs all of the handlers in a
            separate thread and subsequently waits for all the threads to finish. Make sure to
            return from handler as soon as all the neccessary functionality is finished and if
            needed, run the non-essential part of the handler in a separate thread using
            threading.Thread.

            This mechanism is in place in order to start all the neccessary services on which other
            modules might depend. Currently, there is no way to wait for one @start handlers in
            another @start handler.

        Note:

            In a typical use case, `@on` decorators are invoked on method/class definition,
            not at run-time. This can be seen on examples below.

        Examples:

            - ``timer`` event without ID

                - configuration:

                    .. code-block:: json

                        {
                            "gateway": {
                                "moduleTimers": {
                                    "timerModule": 1
                                }
                            }
                        }

                .. code-block:: python


                    from uun_iot import on, Module
                    class TimerModule(Module):
                        @on("tick")
                        def periodical(self):
                            print("Tick tock every 1 s.")

            - ``timer`` event with ID

                - configuration

                    .. code-block:: json

                        {
                            "gateway": {
                                "moduleTimers": {
                                    "sendReceive": {
                                        "send": 2,
                                        "get": 1
                                    }
                                }
                            }
                        }

                .. code-block:: python

                    class SendReceive(Module):
                        @on("tick", "get")
                        def get(self):
                            print(f"Retrieving data...")

                        @on("tick", "send")
                        def send(self):
                            print(f"Sending data...")

            - ``start`` event

                - configuration:

                    .. code-block:: json

                        {
                            "gateway": {}
                        }

                .. code-block:: python

                    class AdvancedDataMeasurement(Module):
                        @on("start")
                        def oneshot(self, evs):
                            runev, stopev = evs
                            while runev.is_set():
                                print("Polling for voltage reading from voltmeter...")
                                data = 53.8
                                if data > 50:
                                    time.sleep(1)
                                else:
                                    time.sleep(1.5)
                                    print(data)

            - ``external`` event

                - configuration:

                    .. code-block:: json

                        {
                            "gateway": {}
                        }

                .. code-block:: python

                    class ExternallyControlledModule(Module):
                        @on("external", "action1")
                        def handle_cmd(self, msg):
                            cmd, msg = msg
                            assert(cmd == "action1")
                            print(msg)

                >>> echo "action1 This message was created outside of the main Python app." | nc -U path/to/unix/socket.sock
                >>> # the main app prints
                >>> 'This message was created outside of the main Python app.'

        Warning:

            *Dev note TODO.* Is method unbounding needed?
            The decorators are usually specified at definition time, thus there is
            no associated instance to the method.
            In case there would be registered a method corresponding to existing instance,
            it would cause problems as Gateway always passes ``self=instance`` as a argument.

        Args:
            eventn (str): one of ``tick``, ``update``, ``start``, ``stop``, ``external``
            subevent (str): optional. See tables above for when subevent can be specified
        """

        if self.instantiated:
            raise EventRegisterAlreadyInstantiated()

        if eventn not in self._ehandlers:
            raise UnsupportedEvent(
                f"Event type '{eventn}' is not recognized. "
                "Known events are:"
                f"`{self._ehandlers.keys()}`."
            )

        if eventn in ["start", "stop", "update"]:
            if subevent is not None:
                raise EventException(
                    f"Invalid subevent argument to event '{eventn}'. The argument"
                    f" must be None, got '{subevent}'."
                )
        if eventn == "external":
            if subevent is None:
                raise EventException(
                    "Invalid subevent argument to event 'external'. The argument"
                    f" must not be None, got '{subevent}'."
                )
            if subevent in [
                list(module_dict.keys())
                for _, module_dict in self._ehandlers["external"].items()
            ]:
                raise EventException(
                    "Subevent '{subevent}' of event 'external' already registered! The"
                    " subevents=commands have to be unique across all modules."
                )

        def wrapper(f):
            try:
                clsname = f.__qualname__.split(".")[-2]
                assert "<locals>" not in clsname
            except (KeyError, AssertionError) as e:
                raise EventException(
                    "Only method registration is supported, define the function as a"
                    " method in a class."
                ) from e
            canonical_module_id = canonical_id_from_str(clsname)

            if canonical_module_id in self._ehandlers[eventn]:
                mdict = self._ehandlers[eventn][canonical_module_id]
                if subevent in mdict:
                    # overwriting
                    orig_handler = mdict[subevent]
                    if orig_handler == f:
                        logger.info(
                            "Registering an already registered handler for '%s.%s',"
                            " handler signature: '%s'",
                            eventn,
                            subevent,
                            repr(f),
                        )
                        return f
                    else:
                        raise ValueError(
                            "Tried to register two handlers for event"
                            f" '{eventn}.{subevent}' of canonical module id"
                            f" '{canonical_module_id}'. Original handler signature:"
                            f" '{repr(orig_handler)}',  new handler: '{repr(f)}'",
                        )
                        # raise ValueError(
                        #    "Tried to register two handlers for event '%s.%s'. Original"
                        #    " handler signature: '%s',  new handler: '%s'",
                        #    eventn,
                        #    subevent,
                        #    repr(orig_handler),
                        #    repr(f),
                        # )
                elif eventn == "tick":
                    # tick supports both None and named subevents
                    # BUT not at the same time, ie. if there is a registered None
                    # subevent, no other named subevents cannot be difined and vice versa
                    if (None in mdict and subevent is not None) or (
                        None not in mdict and subevent is None
                    ):
                        raise EventException(
                            "Either specify non-null subevent name for all events for"
                            f" this module '{clsname}' or specify a single null"
                            " subevent."
                        )
            else:
                # new module entry
                self._ehandlers[eventn][canonical_module_id] = {}

            self._ehandlers[eventn][canonical_module_id][subevent] = f
            return f

        return wrapper

    def assign_instances(
        self, module_inst_list: Iterable[IModule]
    ) -> Dict[ModuleId, IModule]:
        """Assign class instance with registered method of the class for each
        instance in the list.

        Currently, there can be at most one instance to each registered
        method's class. An example: a method of class TestModule gets
        registered using @on("start"). Only one instance of TestModule can be
        passed via :attr:`module_inst_list`.

        (If this is not sufficient for certain usecases, alternative solution
        would be to https://stackoverflow.com/a/3054505 for those special
        usecases.)

        Upon calling this method, bound event handlers to the unique instance
        of corresponding modules.

        This is used internally to clear some remnants of mass importing (for ex. when testing).

        Args:
            module_inst_list: an iterable of module instances

        Returns:
            a dictionary in format { module_id: module_instance } containing
                only those instances which are present in module_inst_list AND they
                have at least one registered method. ``module_id`` is set to module_instance.id,
                or via utils.moduleId(module_instance.__class__)
        """
        if self.instantiated:
            raise EventRegisterAlreadyInstantiated()

        # populate map {canonical_id: real_id}
        canonical_to_real_id = {}
        for instance in module_inst_list:
            canonical_mid, real_mid = instance_ids(instance)
            if canonical_mid in canonical_to_real_id:
                raise EventException(
                    "At most one instance of a given class can be passed. Duplicate"
                    f" canonical id: '{canonical_mid}'"
                )
            canonical_to_real_id[canonical_mid] = real_mid

        # ensure ids listed in handlers are subset of instances
        to_delete = []
        registered_canonical_ids = set()
        for eventn, event_dict in self._ehandlers.items():
            for canon_mid in event_dict:
                # either delete or rename
                if canon_mid not in canonical_to_real_id.keys():
                    to_delete.append((eventn, canon_mid))
                else:
                    registered_canonical_ids.add(canon_mid)
        # logger.warning("to_delete: %s", to_delete)
        # logger.warning("registered_canonical_ids: %s", registered_canonical_ids)

        for eventn, canon_mid in to_delete:
            del self._ehandlers[eventn][canon_mid]

        # ensure return dictionary is subset in ehandlers
        real_id_inst = {}
        for inst in module_inst_list:
            canonical_mid, _ = instance_ids(inst)
            if canonical_mid in registered_canonical_ids:
                real_id_inst[canonical_to_real_id[canonical_mid]] = inst

        # in ehandlers: rename canonical to real ids and bound methods to the corresponding instance
        for eventn, event_dict in self._ehandlers.items():
            assert isinstance(event_dict, dict)
            for canon_id in list(event_dict.keys()):  # loop over fixed key list
                real_id = canonical_to_real_id[canon_id]
                self._ehandlers[eventn][real_id] = {
                    subev: partial(
                        event_dict[canon_id][subev],
                        real_id_inst[real_id],
                    )
                    for subev in event_dict[canon_id]
                    if real_id in real_id_inst
                }
                if real_id != canon_id:
                    del self._ehandlers[eventn][canon_id]

        self.instantiated = True
        return real_id_inst

    def get_handlers(
        self,
        eventn: TEvent,
        *,
        module: Union[ModuleId, "True"] = True,
        subevent: Union[Optional[TSubEvent], "True"] = None,
    ) -> Union[Dict[ModuleId, Callable], Dict[TSubEvent, Callable], Callable, None]:
        """Return a dictionary of handlers corresponding to given selection criteria.

        If the tuple :attr:`module` and :attr:`subevent` uniquely determines a handler,
        return the corresponding handler. If no such handler exists, return None.

        In addition, either :attr:`module`, or :attr:`subevent` can assume
        value of "wildcard" value of ``True``. Only one of them may by ``True``
        at the same time.

        Note that ``subevent=None`` has special handling in order for the user
        not to notice any inconsistent behaivour with function of ``@on``.

        Args:
            eventn: mandatory argument, the event name
            module: module ID, default ``True``. If ``True``, return a dictionary { module_id: handler } where handler
              corresponds to module_id and subevent. Should the dictionary be
              empty, return ``None`` instead.
            subevent: subevent ID, default ``None``. See :method:`on` for what
              is the meaning of subevent. If ``True``, return a dictionary {
              subevent: handler } where handler corresponds to module_id and
              subevent. Should the dictionary be empty, return ``None`` instead.

        Returns:
            Either a dict with handlers, the handler, or None if no handler for
            the given combination exists. If ``module="module-id"`` and
            ``subevent=True`` and the only handler select would be one with
            ``subevent=None``, return directly the handler instead.

        Raises:
            ValueError: if both :attr:`module` and :attr:`subevent` are None
        """

        if not self.instantiated:
            raise EventRegisterNotYetInstantiated()

        # module=True, subevent --> return { mid: handler_of_subevent_and_mid }
        # module; subevent=True --> return { subev: handler_of_subevent_and_mid }
        ehandler = self._ehandlers[eventn]

        if module is True and subevent is True:
            if eventn == "external":
                # external has unique subevents across all modules
                ret = {}
                for mid, mdict in ehandler.items():
                    for subev, f in mdict.items():
                        ret[subev] = f
                return ret if ret else None
            raise ValueError("Both module and subevent cannot be True.")

        if module is True:
            ret = {
                mid: ehandler[mid][subevent]
                for mid in ehandler
                if subevent in ehandler[mid]
            }
            return ret if ret != {} else None

        if subevent is True:
            if module in ehandler:
                handlers = ehandler[module]
                if len(handlers) == 1 and None in handlers:
                    return handlers[None]
                return handlers
            return None

        if module in ehandler and subevent in ehandler[module]:
            return ehandler[module][subevent]

        return None

    # if subevent is not None and subevent is not True and module is None:
    #    module = True

    # ehandler = self._ehandlers[eventn]

    # ret = {}
    # if module in ehandler:
    #    handlers = ehandler[module]
    #    if subevent in handlers:
    #        return handlers[subevent]
    #    if subevent is True:
    #        if len(handlers) == 1 and None in handlers:
    #            return handlers[None]
    #        else:
    #            return handlers
    #    # key subevent in handlers[module] does not exist
    #    return None
    # if module is True:
    #    if subevent == True:
    #        raise ValueError("Both module and subevent cannot be Filter.Any.")
    #    ret = {
    #        mid: ehandler[mid][subevent]
    #        for mid in ehandler
    #        if subevent in ehandler[mid]
    #    }

    #    if ret != {}:
    #        return ret
    # return None

    def get_subevent_names(self, eventn: TEvent) -> List[TSubEvent]:
        """Return all subevent names of given event. If multiple modules have
        the same subevents, returns the subevents multiple times.

        Args:
            eventn: event name
        """
        subevs = []
        ehandler = self._ehandlers[eventn]
        for mid in ehandler:
            subevs += list(filter(lambda x: x is not None, ehandler[mid].keys()))
        return subevs


def _unbound_function(f: Callable) -> Callable:
    """
    If the function :func:`f` is bounded (ie. it is a method in some object instance,
    unbound it and return it. Otherwise, return original :func:`f`.
    """
    if hasattr(f, "__self__"):
        f = f.__func__
    return f
