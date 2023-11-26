from enum import Enum


class RoleEnum(str, Enum):
    REPRESENT = "represent"
    CLIENT = "client"

    @classmethod
    def choices(cls):
        return tuple((i.value, i.name) for i in cls)


class StatusEnum(str, Enum):
    CANCEL = "cancel"
    WAITING = "waiting"
    SUCCESS = "success"

    @classmethod
    def choices(cls):
        return tuple((i.value, i.name) for i in cls)
