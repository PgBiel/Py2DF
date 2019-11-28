from .enum_util import AutoSnakeToPascalCaseNameEnum, IfType
from enum import auto, unique


@unique
class IfPlayerType(AutoSnakeToPascalCaseNameEnum, IfType):
    BLOCK_EQUALS = auto()
    CMD_ARG_EQUALS = auto()
    CMD_EQUALS = auto()
    CURSOR_ITEM = auto()
    HAS_ALL_ITEMS = auto()
    HAS_EFFECT = auto()
    HAS_ITEM = auto()
    HAS_ROOM_FOR_ITEM = auto()
    HAS_SLOT_ITEM = auto()
    INV_OPEN = auto()
    IN_WORLD_BORDER = auto()
    IS_BLOCKING = auto()
    IS_FLYING = auto()
    IS_GLIDING = auto()
    IS_GROUNDED = auto()
    IS_HOLDING = auto()
    IS_HOLDING_MAIN = auto()
    IS_HOLDING_OFF = auto()
    IS_LOOKING_AT = auto()
    IS_NEAR = auto()
    IS_SNEAKING = auto()
    IS_SPRINTING = auto()
    IS_SWIMMING = auto()
    IS_WEARING = auto()
    ITEM_EQUALS = auto()
    MENU_SLOT_EQUALS = auto()
    NAME_EQUALS = auto()
    NO_ITEM_COOLDOWN = auto()
    SLOT_EQUALS = auto()
    STANDING_ON = auto()


@unique
class IfVariableType(AutoSnakeToPascalCaseNameEnum, IfType):
    NOT_EQUALS = " != "
    EQUALS = " = "
    CONTAINS = auto()
    GREATER_THAN = ">"
    GREATER_THAN_OR_EQUAL_TO = ">="
    IN_RANGE = auto()
    IS_NEAR = auto()
    ITEM_EQUALS = auto()
    ITEM_HAS_TAG = auto()
    LESS_THAN = "<"
    LESS_THAN_OR_EQUAL_TO = "<="
    LIST_CONTAINS = auto()
    LIST_VALUE_EQ = auto()
    TEXT_MATCHES = auto()
    VAR_IS_TYPE = auto()


@unique
class IfEntityType(AutoSnakeToPascalCaseNameEnum, IfType):
    EXISTS = auto()
    IS_ITEM = auto()
    IS_MOB = auto()
    IS_NEAR = auto()
    IS_PROJ = auto()
    IS_TYPE = auto()
    IS_VEHICLE = auto()
    NAME_EQUALS = auto()
    STANDING_ON = auto()


@unique
class IfGameType(AutoSnakeToPascalCaseNameEnum, IfType):
    BLOCK_EQUALS = auto()
    BLOCK_POWERED = auto()
    CMD_ARG_EQUALS = auto()
    COMMAND_EQUALS = auto()
    CONTAINER_HAS = auto()
    CONTAINER_HAS_ALL = auto()
    EVENT_BLOCK_EQUALS = auto()
    EVENT_CANCELLED = auto()
    EVENT_ITEM_EQUALS = auto()
    SIGN_HAS_TXT = auto()
