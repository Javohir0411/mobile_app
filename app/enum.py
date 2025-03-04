from enum import Enum


class ItemConditionEnum(Enum):
    NEW = "new"
    USED = "used"


class ItemImeiEnum(Enum):
    REGISTERED = "registered"
    UNREGISTERED = "unregistered"


class UserGenderEnum(Enum):
    MALE = "male"
    FEMALE = "female"
    OTHER = "other"


class CurrencyEnum(Enum):
    USD = "usd"
    UZS = "uzs"


class UserRoleEnum(Enum):
    GUEST = "guest"
    USER = "user"