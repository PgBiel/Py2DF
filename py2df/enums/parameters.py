"""
Enums for parameters and attributes in classes.
"""
from enum import auto, unique
from .enum_util import AutoLowerNameEnum


@unique
class BlockType(AutoLowerNameEnum):
    PLAYER_EVENT = "event"
    PLAYER_ACTION = auto()
    GAME_ACTION = auto()
    IF_PLAYER = auto()
    REPEAT = auto()
    START_PROCESS = auto()
    CALL_FUNCTION = auto()
    CONTROL = auto()
    IF_VAR = auto()
    IF_ENTITY = auto()
    IF_GAME = auto()
    SET_VARIABLE = auto()
    ELSE = auto()
    FUNCTION = auto()
    PROCESS = auto()
    SELECT_OBJECT = auto()
    ENTITY_ACTION = auto()
    ENTITY_EVENT = auto()


@unique
class BracketType(AutoLowerNameEnum):
    NORM = auto()
    REPEAT = auto()


@unique
class BracketDirection(AutoLowerNameEnum):
    OPEN = auto()
    CLOSE = auto()
