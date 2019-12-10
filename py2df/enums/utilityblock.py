from .enum_util import AutoSnakeToPascalCaseNameEnum, UtilityBlockType, TagType
from enum import unique, auto, Enum


# region:types

@unique
class RepeatType(UtilityBlockType, AutoSnakeToPascalCaseNameEnum):
    """Contains all types of Repeat blocks."""
    ADJACENT = auto(
    )  #: Repeats code once for each block adjacent to a location. Each iteration, the var is set to the current block.
    FOR_EACH = auto(
    )  #: Repeats code once for every index of a list. Each iteration, the var is set to the value at the current index.
    FOREVER = auto(
    )  #: Repeats code forever.
    GRID = auto(
    )  #: Repeats code once for every block in a region. Each iteration, the var is set to the curr. block's location.
    N_TIMES = "N Times"  #: Repeats code multiple times.
    SPHERE = auto()  #: Repeats code once for every evenly distributed sphere point.
    WHILE_COND = auto()  #: Repeats code while a certain condition is true.


@unique
class SetVarType(UtilityBlockType, AutoSnakeToPascalCaseNameEnum):
    """Contains all types of Set Variable blocks."""
    ABSOLUTE_VALUE = auto()  #: Makes negative numbers positive.
    ADD = "+="  #: Increments a number variable by 1 or more other numbers.
    ADD_ITEM_ATTRIBUTE = auto()  #: Adds an attribute modifier to the item, which is active in a certain equipment slot.
    ADD_ITEM_ENCHANT = auto()  #: Adds the given enchant to the item.
    ALIGN_LOC = auto()  #: Aligns a location to the center or corner of the block it is in.
    APPEND_LIST = auto()  #: Adds a list to the end of another list.
    APPEND_VALUE = auto()  #: Adds a value to the end of a list.
    AVERAGE = auto()  #: Sets a variable to the average of the given numbers.
    CLAMP_NUMBER = auto(
    )  #: Checks if a number is between a minimum and maximum value, and if not, sets it to the nearest.
    COSINE = auto()  #: Sets a variable to the trigonometric cosine function of a number.
    CREATE_LIST = auto()  #: Creates a list from the given values.
    DISTANCE = auto()  #: Sets a variable to the distance between two locations.
    DUPLICATE_TEXT = auto()  #: Duplicates the text variable some amount of times.
    FACE_DIRECTION = auto()  #: Rotates a location to face a direction.
    FACE_LOCATION = auto()  #: Makes a location face another location.
    FIND_CENTER = auto()  #: Finds an average position (center) of the given locations.
    GET_BLOCK_DATA = auto()  #: Sets a variable to the block metadata tag value at a location.
    GET_BLOCK_POWER = auto()  #: Sets a variable to the redstone power level of a block.
    GET_BLOCK_TYPE = auto()  #: Sets a variable to the block material at a location.
    GET_BOOK_TEXT = auto()  #: Gets the given book's text.
    GET_COLOR_CHANNEL = auto()  #: Gets one of the RGB / HSB / HSL number values of a color.
    GET_CONTAINER_ITEMS = auto()  #: Sets a variable to the contents of a container at a location.
    GET_CONTAINER_NAME = auto()  #: Sets a variable to the name of a container at a location.
    GET_COORD = auto()  #: Reads the X, Y, Z, pitch, or yaw coordinate of a location variable.
    GET_DIRECTION = auto()  #: Sets a variable to the direction this location is rotated in.
    GET_HEAD_OWNER = auto()  #: Gets the given player head's owner's name or UUID.
    GET_ITEM_AMOUNT = auto()  #: Gets the given item's stack size.
    GET_ITEM_COLOR = auto()  #: Gets the color hexadecimal of a colorable item.
    GET_ITEM_DURA = auto()  #: Gets the given item's current or maximum durability.
    GET_ITEM_ENCHANTS = auto()  #: Gets the given item's list of enchantments.
    GET_ITEM_LORE = auto()  #: Gets the given item's lore list.
    GET_ITEM_NAME = auto()  #: Gets the given item's name.
    GET_ITEM_TAG = auto()  #: Gets the text value of a custom item tag.
    GET_ITEM_TYPE = auto()  #: Gets the given item's material.
    GET_LIST_VALUE = auto()  #: Gets the stored value at the specified list index.
    GET_PITCH = auto()  #: Sets a variable to a location's pitch.
    GET_POTION_AMP = auto()  #: Gets the given potion's amplifier.
    GET_POTION_DUR = auto()  #: Gets the given potion's tick duration.
    GET_POTION_TYPE = auto()  #: Gets the given potion's effect type.
    GET_SIGN_TEXT = auto()  #: Sets a variable to the text on a sign.
    GET_SOUND_PITCH = auto()  #: Gets the given sound's pitch or note.
    GET_SOUND_TYPE = auto()  #: Gets the given sound's type.
    GET_SOUND_VOLUME = auto()  #: Gets the given sound's volume.
    GET_VALUE_INDEX = auto()  #: Searches for a value in a list and, if found, gets the index.
    GET_X = auto()  #: Sets a variable to a location's X coordinate.
    GET_Y = auto()  #: Sets a variable to a location's Y coordinate.
    GET_YAW = auto()  #: Sets a variable to a location's yaw.
    GET_Z = auto()  #: Sets a variable to a location's Z coordinate.
    HSB_COLOR = auto()  #: Creates a color hex based on hue, saturation and brightness.
    HSL_COLOR = auto()  #: Creates a color hex based on hue, saturation and luminosity.
    INSERT_LIST_INDEX = auto(
    )  #: Inserts a value into a list at the specified index, shifting all values at and after the index back one index.
    JOIN_TEXT = auto()  #: Combines a list of text values.
    LIST_LENGTH = auto()  #: Gets the amount of indices a list has.
    MIX_COLORS = auto()  #: Mixes two or more hexadecimal colors into a new color.
    NORMAL_RANDOM = auto(
    )  #: Sets a variable to a random number using a normal distribution: values closer to ? are more likely to appear.
    PARSE_NUMBER = auto()  #: Sets a the variable to numerical equivalent of a text variable if possible.
    PARSE_PITCH = auto()  #: 
    PARSE_X = auto()  #: 
    PARSE_Y = auto()  #: 
    PARSE_YAW = auto()  #: 
    PARSE_Z = auto()  #: 
    PERLIN_NOISE = auto()  #: Gets a Perlin noise value: A type of fractal gradient noise.
    PURGE_VARS = auto()  #: Clears all variables of which the name matches the given text.
    RANDOM_LOC = auto()  #: Sets the variable to a random location between two locations.
    RANDOM_NUMBER = auto()  #: Sets a variable to a random number in between two other numbers.
    RANDOM_OBJ = auto()  #: Sets a variable to a random value.
    RANDOMIZE_LIST = auto()  #: Randomizes the order of a list's values.
    REMOVE_ITEM_TAG = auto()  #: Removes a custom item tag.
    REMOVE_LIST_INDEX = auto()  #: Removes a list index and shifts all values after the index back one index.
    REMOVE_LIST_VALUE = auto()  #: Removes all matching values from the list.
    REPLACE_TEXT = auto()  #: Searches for part of a text variable and replaces it.
    REVERSE_LIST = auto(
    )  #: Flips the order of a list's values, making values at the back switch places with values in the front.
    RGB_COLOR = auto()  #: Creates a color hex based on red, green and blue channels.
    RM_TEXT = auto()  #: Removes all instances of a certain text item from a text variable.
    ROUND = auto()  #: Rounds a number to a multiple. Rounds to a whole number by default.
    SET_ALL_COORDS = auto()  #: Changes a location's coordinates or creates a new location.
    SET_BOOK_TEXT = auto()  #: Sets the given book's text.
    SET_BREAKABILITY = auto()  #: Sets whether an item is unbreakable.
    SET_CAN_DESTROY = auto()  #: Sets the block types which the item can destroy (in gamemode adventure).
    SET_CAN_PLACE_ON = auto()  #: Sets the block types which the item can place on (in gamemode adventure).
    SET_CASE = auto()  #: Changes the capitalization of a given text, such as uppercase.
    SET_COORD = auto()  #: Changes the X, Y, Z, pitch, or yaw coordinate of a location variable.
    SET_COORDS = auto()  #: Sets a variable to a set of coordinates (location).
    SET_HEAD_OWNER = auto()  #: Sets the owning player of a player head item.
    SET_ITEM_AMOUNT = auto()  #: Sets the given item's stack size.
    SET_ITEM_COLOR = auto()  #: Sets the color of a colorable item.
    SET_ITEM_DURA = auto()  #: Sets the given item's durability.
    SET_ITEM_ENCHANTS = auto()  #: Sets the given item's list of enchantments.
    SET_ITEM_FLAGS = auto()  #: Sets which components of the item are visible, similar to /hideflags.
    SET_ITEM_LORE = auto()  #: Sets the given item's lore list.
    SET_ITEM_NAME = auto()  #: Sets the given item's name.
    SET_ITEM_TAG = auto()  #: Sets the value of or creates a custom stored tag value.
    SET_ITEM_TYPE = auto()  #: Sets the given item's material.
    SET_LIST_VALUE = auto()  #: Sets the stored value at the specified list index.
    SET_PITCH = auto()  #: Sets the pitch of a location variable.
    SET_POTION_AMP = auto()  #: Sets the given potion's amplifier.
    SET_POTION_DUR = auto()  #: Sets the given potion's duration.
    SET_POTION_TYPE = auto()  #: Sets the given potion's effect type.
    SET_SOUND_PITCH = auto()  #: Sets the given sound's pitch or note.
    SET_SOUND_TYPE = auto()  #: Sets the given sound's type.
    SET_SOUND_VOLUME = auto()  #: Sets the given sound's volume.
    SET_TO = "="  #: Assigns a value to a variable.
    SET_TO_ADDITION = "+"  #: Sets a variable to the sum of the given values.
    SET_TO_MOD = "%"  #: Sets a dynamic variable to the remainder after dividing two numbers with a whole quotient.
    SET_TO_POWER = "Exponent"  #: Raises a number to the power of an exponent.
    SET_TO_PRODUCT = "x"  #: Sets a dynamic variable to the product of 2 or more numbers.
    SET_TO_QUOTIENT = "Division"  #: Sets a dynamic variable to the quotient between 2 or more numbers.
    SET_TO_ROOT = "Root"  #: Finds the root of a number.
    SET_TO_SUBTRACTION = "-"  #: Sets a dynamic variable to the difference between a set of numbers.
    SET_X = auto()  #: Sets the X coordinate of a location variable.
    SET_Y = auto()  #: Sets the Y coordinate of a location variable.
    SET_YAW = auto()  #: Sets the yaw of a location variable.
    SET_Z = auto()  #: Sets the Z coordinate of a location variable.
    SHIFT_ALL_AXES = auto()  #: Shifts a location's coordinates on the X-Axis, Y-Axis and Z-Axis.
    SHIFT_ALL_DIRS = auto()  #: Shifts a location in multiple directions, based on its rotation (pitch/yaw)
    SHIFT_AXIS = auto()  #: Shifts the X, Y, or Z coordinate of a location on its axis.
    SHIFT_DIRECTION = auto(
    )  #: Shifts a location forwards or sideways. The direction is based on its rotation (pitch/yaw).
    SHIFT_LOCATION = auto()  #: Shifts the location in some direction.
    SHIFT_ROTATION = auto()  #: Rotates a location by shifting its pitch (up/down) or yaw (left/right) value.
    SHIFT_TOWARDS = auto()  #: Shifts a location a certain distance towards another location.
    SINE = auto()  #: Sets a variable to the trigonometric sine function of a number.
    SORT_LIST = auto()  #: Sorts a list's values.
    SPLIT_TEXT = auto()  #: Splits a text variable into a list of text variables.
    SUBTRACT = "-="  #: Decrements a number variable by 1 or more other numbers.
    TANGENT = auto()  #: Sets a variable to the trigonometric tangent function of a number.
    TEXT = auto()  #: Sets a variable to text, or combines multiple values into one text.
    TEXT_LENGTH = auto()  #: Sets a variable to the length of a text variable.
    TRANSLATE_COLORS = auto()  #: Converts color codes written in "&" format to functional color codes, or vice versa.
    TRIM_LIST = auto()  #: Trims a list variable, starting and ending at a certain index.
    TRIM_TEXT = auto()  #: Trims a text variable, starting and ending at a certain character.
    VORONOI_NOISE = auto(
    )  #: Gets a Voronoi noise value: A cellular noise in which the value of an entire cell is calculated.
    WORLEY_NOISE = auto(
    )  #: Gets a Worley noise value: A cellular noise in which the distance between two cells' nuclei is calculated.
    WRAP_NUMBER = auto()  #: Checks if a number is between two bounds and if not, wraps it around the farthest bound.


@unique
class SelectObjectType(UtilityBlockType, AutoSnakeToPascalCaseNameEnum):
    """Contains all types of Select Object blocks."""
    ALL_ENTITIES = auto()  #: Selects all entities on the plot.
    ALL_MOBS = auto()  #: Selects all mobs on the plot.
    ALL_PLAYERS = auto()  #: Selects all players that are on the plot.
    DAMAGER = auto()  #: Selects the damager in a damage-related event. The damager can be a player or an entity.
    DEFAULT_ENTITY = auto(
    )  #: Selects the main entity involved in the current Player/Entity Event, or the last spawned entity if none.
    DEFAULT_PLAYER = auto()  #: Selects the main player involved in the current Player Event or Loop.
    ENTITIES_COND = auto()  #: Selects all entities that meet a certain condition.
    ENTITY_NAME = auto()  #: Selects all entities whose names are equal to the text in the chest.
    FILTER_SELECT = auto()  #: Filters the current selection by selecting all object that meet a certain condition.
    KILLER = auto()  #: Selects the killer in a kill-related event. The killer can be a player or an entity.
    LAST_ENTITY = auto()  #: Selects the most recently spawned entity.
    LAST_MOB = auto()  #: Selects the most recently spawned mob.
    MOB_NAME = auto()  #: Selects all mobs whose names are equal to the text in the chest.
    MOBS_COND = auto()  #: Selects all mobs that meet a certain condition.
    NONE = auto()  #: Selects nothing. All code blocks will act like they normally would if nothing was selected.
    PLAYER_NAME = auto()  #: Selects the player whose name is equal to the text in the chest.
    PLAYERS_COND = auto()  #: Selects all players that meet a certain condition.
    PROJECTILE = auto()  #: Selects the projectile in a projectile-related event.
    RANDOM_ENTITY = auto()  #: Selects a random entity.
    RANDOM_MOB = auto()  #: Selects a random mob.
    RANDOM_PLAYER = auto()  #: Selects a random player.
    RANDOM_SELECTED = auto()  #: Filters the current selection by selecting one or more random objects from it.
    SHOOTER = auto()  #: Selects the shooter in a projectile-related event.
    VICTIM = auto(
    )  #: Selects the victim in a kill-related or damage-related event. The victim can be a player or an entity.

# endregion:types

# region:tags


class RAdjacentPattern(TagType, Enum):
    CARDINAL = "Cardinal (4 blocks)"
    SQUARE = "Square (8 blocks)"
    ADJACENT = "Adjacent (6 blocks)"
    CUBE = "Cube (26 blocks)"

# endregion:tags
