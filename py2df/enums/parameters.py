"""
Enums for parameters and attributes in classes.
"""
from enum import auto, unique
from .enum_util import AutoLowerNameEnum


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
    # TODO: Finish this list -- unsures below; sort after sure
    IF_VARIABLE = auto()
    IF_ENTITY = auto()
    IF_GAME = auto()
    SET_VARIABLE = auto()
    ELSE = auto()
    FUNCTION = auto()
    PROCESS = auto()
    SELECT_OBJECT = auto()
    ENTITY_ACTION = auto()
    ENTITY_EVENT = auto()  # ???? PLAYER_EVENT appears just as EVENT...


@unique
class BracketType(AutoLowerNameEnum):
    NORM = auto()
    REPEAT = auto()


@unique
class BracketDirection(AutoLowerNameEnum):
    OPEN = auto()
    CLOSE = auto()
