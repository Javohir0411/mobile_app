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