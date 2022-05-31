from enum import Enum


class VehicleAction(Enum):
    STOP = "drive stop"
    TEN_PERCENT = "drive 10%"
    TWENTY_PERCENT = "drive 20%"
    THIRTY_PERCENT = "drive 30%"
    FOURTY_PERCENT = "drive 40%"
    HALF_SPEED = "drive 50%"
    SIXTY_PERCENT = "drive 60%"
    SEVENTY_PERCENT = "drive 70%"
    EIGHTY_PERCENT = "drive 80%"
    NINETY_PERCENT = "drive 90%"
    FULL_SPEED = "drive start"
