"""
Enums for parameters and attributes in classes.
"""
from enum import Enum, auto, unique
from enums.enum_util import AutoLowerNameEnum


@unique
class BlockType(AutoLowerNameEnum):
    EVENT = auto()
    PLAYER_ACTION = auto()
    GAME_ACTION = auto()
    IF_PLAYER = auto()
    REPEAT = auto()
    START_PROCESS = auto()
    CALL_FUNCTION = auto()
    CONTROL = auto()
    # TODO: Finish this list


@unique
class BracketType(AutoLowerNameEnum):
    NORM = auto()
    REPEAT = auto()


@unique
class BracketDirection(AutoLowerNameEnum):
    OPEN = auto()
    CLOSE = auto()
