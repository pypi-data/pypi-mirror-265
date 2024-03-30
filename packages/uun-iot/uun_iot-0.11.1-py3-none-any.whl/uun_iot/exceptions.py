class UuAppClientException(Exception):
    """Internal error in request pre-processing occured."""


class TokenError(UuAppClientException):
    """Error when getting/validating a token occured."""


class TokenCommandError(TokenError):
    """Server error when getting a token occured."""


class EventException(Exception):
    """ Exception in event management system. """


class UnsupportedEvent(EventException):
    """Unknown gateway event."""


class EventRegisterAlreadyInstantiated(EventException):
    pass

class EventRegisterNotYetInstantiated(EventException):
    pass
