"""
Enums for parameters and attributes in classes.
"""
from enum import auto, unique, Enum
from .enum_util import AutoLowerNameEnum


@unique
class BlockType(AutoLowerNameEnum):  # TODO: Verify Function, Process and Player Event json data
    """Contains all types of different codeblocks."""
    CALL_FUNC = auto(
    )  #: Calls functions made by a Function block. Code will not continue past this until the Function completes.
    CONTROL = auto()  #: Used to control the execution of some or all code blocks after it.
    ELSE = auto(
    )  #: Executes the code inside it if the condition right before it wasn't met.
    ENTITY_ACTION = auto()  #: Used to do something related to an entity or multiple entities.
    ENTITY_EVENT = auto()  #: Used to execute code when an entity does something or when something happens to an entity.
    FUNCTION = auto()  #: Used to define a line of code that can be called with a Call Function block.
    GAME_ACTION = auto()  #: Used to do something related to the plot and everyone playing it.
    IF_ENTITY = auto(
    )  #: Used to execute the code inside it if a certain condition related to an entity or multiple entities is met.
    IF_GAME = auto()  #: Used to execute the code inside it if a certain condition related to the plot is met.
    IF_PLAYER = auto()  #: Used to execute the code inside it if a certain condition related to a player is met.
    IF_VAR = auto()  #: Executes the code inside it if a certain condition related to the value of a variable is met.
    PLAYER_ACTION = auto()  #: Used to do something related to a player or multiple players.
    PLAYER_EVENT = "event"  #: Used to execute code when something is done by (or happens to) a player.
    PROCESS = auto()  #: Used to execute code when the process is started using a Start Process block.
    REPEAT = auto()  #: Used to repeat the code inside it.
    SELECT_OBJ = auto(
    )  #: Used to change the selection on the current line of code, which will affect the targets of most code blocks.
    SET_VAR = auto()  #: Used to set the value of a dynamic variable.
    START_PROCESS = auto(
    )  #: Starts processes made by a Process block. The Process is asynchronous; code will continue past this block.


@unique
class BracketType(AutoLowerNameEnum):
    """Contains all types of brackets (:attr:`REPEAT` is for Repeat blocks; :attr:`NORM` for all If's and Else)."""
    NORM = auto()  #: Normal bracket; occurs on If-related and Else blocks.
    REPEAT = auto()  #: Repeat bracket; occurs on Repeat blocks.


@unique
class BracketDirection(AutoLowerNameEnum):
    """Contains the directions of brackets (:attr:`OPEN` opens the block inserting space and :attr:`CLOSE` closes)."""
    OPEN = auto()  #: Opening bracket.
    CLOSE = auto()  #: Closing bracket.


@unique
class PlotSizes(Enum):
    """An :class:`Enum` that relates each plot size to its respective width, in blocks. E.g.: Basic Plot is 51x51."""
    BASIC_PLOT = 51
    LARGE_PLOT = 101
    MASSIVE_PLOT = 301
