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
    FILE_NOT_SUPPORTED = 9
    NOT_MEMBER = 10


class NotMember(Exception):
    def __init__(self, message='You are not a member!'):
        self.error_code = ErrorCode.NOT_MEMBER
        self.status_code = 401
        self.message = message
        super().__init__(self.message)


class UnauthorizedEntity(Exception):
    def __init__(self, message='You are not the owner!'):
        self.error_code = ErrorCode.UNAUTHORIZED
        self.status_code = 401
        self.message = message
        super().__init__(self.message)


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


class InvalidToken(Exception):
    def __init__(self, message="Invalid Token format"):
        self.error_code = ErrorCode.INVALID_TOKEN
        self.status_code = 401
        self.message = message
        super().__init__(self.message)


class ExpiredToken(Exception):
    def __init__(self, message="Token expired"):
        self.error_code = ErrorCode.INVALID_TOKEN
        self.status_code = 401
        self.message = message
        super().__init__(self.message)


class FileNotSupported(Exception):
    def __init__(self, message='File is not supported'):
        self.error_code = ErrorCode.FILE_NOT_SUPPORTED
        self.status_code = 415
        self.message = message
        super().__init__(self.message)
