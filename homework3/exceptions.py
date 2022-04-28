class RespondErrorException(Exception):
    pass


class ResponseStatusCodeException(Exception):
    pass


class CannotGetCSRFToken(Exception):
    pass


class SegmentIsNotCreated(Exception):
    pass


class UnknownRequestInMethod(Exception):
    pass