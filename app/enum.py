from enum import Enum


class ItemConditionEnum(str, Enum):
    NEW = "new"
    USED = "used"


class ItemImeiEnum(str, Enum):
    REGISTERED = "registered"
    UNREGISTERED = "unregistered"


class UserGenderEnum(str, Enum):
    MALE = "male"
    FEMALE = "female"
    OTHER = "other"


class CurrencyEnum(str, Enum):
    USD = "usd"
    UZS = "uzs"


class UserRoleEnum(str, Enum):
    GUEST = "guest"
    USER = "user"