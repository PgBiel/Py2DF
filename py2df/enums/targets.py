from .enum_util import AutoSnakeToPascalCaseNameEnum
from ..utils import remove_u200b_from_doc
from enum import auto, unique


class Target:
    """Represents any target of any action."""
    pass


class SelectionTarget(Target):
    """Represents the current selection.

    Attributes
    ----------\u200b
        value : :class:`str`
            Equal to ``"Selection"`` , always.
    """
    value: str = "Selection"

    def __repr__(self):
        return f"<{self.__class__.__name__}>"

    def __str__(self):
        return self.value


@unique
class PlayerTarget(Target, AutoSnakeToPascalCaseNameEnum):
    """Contains the different targets a Player Action can have."""
    DEFAULT = auto()  #: The main player involved in the current Player Event.
    SELECTION = auto()  #: The current selection (selected player/s).
    ALL_PLAYERS = auto()  #: All players in the plot.
    DAMAGER = auto()  #: The damager in a damage-related event.
    SHOOTER = auto()  #: The shooter in a projectile-related event.
    KILLER = auto()  #: The killer in a kill-related event.
    VICTIM = auto()  #: The victim in a kill-related or damage-related event.


@unique
class EntityTarget(Target, AutoSnakeToPascalCaseNameEnum):
    """Contains the different targets an Entity Action can have."""
    DEFAULT = auto(
    )   #: The main entity involved in the current Player/Entity Event, or the last spawned entity if none.
    SELECTION = auto()  #: The current selection (selected entity/entities or mob/s).
    ALL_ENTITIES = auto()  #: All entities on the plot.
    ALL_MOBS = auto()  #: All mobs on the plot.
    LAST_ENTITY = auto()   #: The most recently spawned entity.
    LAST_MOB = auto()   #: The most recently spawned mob.
    ENTITY_NAME = auto()  #: All entities whose names are equal to the text in the first parameter.
    MOB_NAME = auto()  #: All mob whose names are equal to the text in the first parameter.
    # TODO: Check if Entity_Name and Mob_Name are the actual targets on entity actions, or if just "Name"
    PROJECTILE = auto()  #: The projectile in a projectile-related event.
    KILLER = auto()  #: Selects the killer in a kill-related event.
    VICTIM = auto()  #: Selects the victim in a kill-related or damage-related event.


remove_u200b_from_doc(SelectionTarget)
