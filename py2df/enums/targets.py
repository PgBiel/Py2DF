from .enum_util import AutoSnakeToPascalCaseNameEnum
from enum import auto, unique


class Target(AutoSnakeToPascalCaseNameEnum):
    """Represents any target of any action."""
    pass


@unique
class PlayerTarget(Target):
    """Contains the different targets a Player Action can have."""
    DEFAULT = auto(),
    SHOOTER = auto()  # TODO: Player Target


@unique
class EntityTarget(Target):
    """Contains the different targets an Entity Action can have."""
    LAST_MOB = auto()  # TODO: Entity Target
