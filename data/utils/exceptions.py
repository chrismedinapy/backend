class ErrorCode:
    INVALID_PARAMETER = 0
    INVALID_TOKEN = 1
    UNAUTHORIZED = 2
    NOT_FOUND = 3
    UNEXPECTED = 4
    DUPLICATED = 5
    USED_INVITATION = 6
    MEMBERS_EXCEEDED = 7
    NOT_THE_OWNER = 8


class EntityNotFound(Exception):
    def __init__(self, message='Entity not found'):
        self.error_code = ErrorCode.NOT_FOUND
        self.status_code = 404
        self.message = message
        super().__init__(self.message)


class DuplicatedRecord(Exception):
    def __init__(self, message='Duplicate record does not allow'):
        self.error_code = ErrorCode.DUPLICATED
        self.status_code = 409
        self.message = message
        super().__init__(self.message)


class InvalidOperation(Exception):
    def __init__(self, message='Invalid operation exception'):
        self.error_code = ErrorCode.UNEXPECTED
        self.status_code = 500
        self.message = message
        super().__init__(self.message)


class InvalidParameter(Exception):
    def __init__(self, message='Invalid Parameter'):
        self.error_code = ErrorCode.INVALID_PARAMETER
        self.status_code = 400
        self.message = message
        super().__init__(self.message)
