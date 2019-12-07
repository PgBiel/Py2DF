"""
Enum related utilities.
"""
from enum import Enum


class CodeblockActionType:
    """
    An ABC for types of Codeblock `action` values (enums).
    """
    pass


class ActionType(CodeblockActionType):
    """
    An ABC for enums of action types (Player Action, Entity Action, Game Action or Control).
    """
    pass


class EventType(CodeblockActionType):
    """
    An ABC for enums of event types (Player Event and Entity Event).
    """
    pass


class IfType(CodeblockActionType):
    """
    An ABC for enums of If types (If Player, If Variable, If Entity and If Game).
    """
    pass


class UtilityBlockType(CodeblockActionType):
    """
    An ABC for enums of utility types (Repeat, Set Var and Select Object).
    """
    pass


keep_upper = ("XP", "AI", "TNT", "PFX", "HSL", "HSB", "RGB", "UUID", "UI", "CPU")  # strings to keep uppercase


class AutoNameEnum(Enum):
    """
    An enum whose auto values are the respective names of the constants.
    """

    def _generate_next_value_(name, _start, _count, _last_values):
        return name


class AutoLowerNameEnum(Enum):
    """
    An enum whose auto values are the respective *lowercase* names of the constants.
    """

    def _generate_next_value_(name, _start, _count, _last_values):
        return name.lower()


class AutoUpperNameEnum(Enum):
    """
    An enum whose auto values are the respective *uppercase* names of the constants.
    """

    def _generate_next_value_(name, _start, _count, _last_values):
        return name.upper()


class AutoSnakeToPascalCaseNameEnum(Enum):
    """
    An enum whose auto values are the respective *PascalCase* names of the constants (instead of SNAKE_CASE).
    """

    def _generate_next_value_(name, _start, _count, _last_values):
        return "".join(map(
            lambda s: s.upper() if s in keep_upper else s.capitalize(),
            name.split("_")
        ))  # TEST_TEST_TEST => TestTestTest


class AutoSnakeToCapitalizedWordsEnum(Enum):
    """
    An enum whose auto values are the respective *Capitalized Words* names of the constants (instead of SNAKE_CASE).
    """

    def _generate_next_value_(name, _start, _count, _last_values):
        return "".join(map(
            lambda s: s.upper() if s in keep_upper else s.capitalize() + " ",
            name.split("_")
        )).strip()  # TEST_TEST_TEST => Test Test Test


class TagType(AutoSnakeToCapitalizedWordsEnum):
    """
    An ABC for Tag-related enums.
    """
    pass
