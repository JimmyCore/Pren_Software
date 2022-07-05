from enum import Enum


class VehicleAction(Enum):
    STOP = b"drive stop\n"
    TEN_PERCENT = b"drive 10%"
    TWENTY_PERCENT = b"drive 20%"
    THIRTY_PERCENT = b"drive 30%"
    FOURTY_PERCENT = b"drive 40%"
    HALF_SPEED = b"drive 50%"
    SIXTY_PERCENT = b"drive 60%"
    SEVENTY_PERCENT = b"drive 70%"
    EIGHTY_PERCENT = b"drive 80%"
    NINETY_PERCENT = b"drive 90%"
    FULL_SPEED = b"drive start\n"
