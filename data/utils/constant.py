from enum import Enum


class Status(Enum):
    ACTIVE = 1
    INACTIVE = 0


class AccessLevel(Enum):
    ADMIN = 0
    USER = 1
