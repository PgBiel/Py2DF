from .enum_util import AutoSnakeToCapitalizedWordsEnum, AutoLowerNameEnum
from .materials import Material
from enum import auto, unique, Enum


@unique
class ParticleType(AutoSnakeToCapitalizedWordsEnum):
    """Contains all types of particles usable in DiamondFire."""
    ANGRY_VILLAGER    = auto()
    BARRIER           = auto()
    BUBBLE            = auto()
    BUBBLE_POP        = auto()
    CLOUD             = auto()
    CONDUIT           = auto()
    CRIT              = auto()
    DAMAGE_HEARTS     = auto()
    DOLPHIN_TRAIL     = auto()
    DRAGON_BREATH     = auto()
    ELDER_GUARDIAN    = auto()
    ENCHANTMENT_RUNES = auto()
    END_ROD           = auto()
    FIREWORK_SPARKLES = auto()
    FISHING_TRAIL     = auto()
    FLAME             = auto()
    HAPPY_VILLAGER    = auto()
    HEART             = auto()
    HUGE_EXPLOSION    = auto()
    LARGE_EXPLOSION   = auto()
    LARGE_SMOKE       = auto()
    LAVA              = auto()
    LAVA_DRIP         = auto()
    MAGIC_CRIT        = auto()
    MOB_SPELL         = auto()
    MUSIC_NOTE        = auto()
    MYCELIUM          = auto()
    PORTAL            = auto()
    RAIN_SPLASH       = auto()
    REDSTONE          = auto()
    SLIME             = auto()
    SMALL_EXPLOSION   = auto()
    SMOKE             = auto()
    SNOWBALL          = auto()
    SPIT              = auto()
    SQUID_INK         = auto()
    SWEEP_ATTACK      = auto()
    TOTEM             = auto()
    WATER_DRIP        = auto()
    WATER_SPLASH      = auto()
    WITCH_MAGIC       = auto()


@unique
class CustomSpawnEggType(Enum):
    IRON_GOLEM = (Material.POLAR_BEAR_SPAWN_EGG, "Iron Golem")
    KILLER_BUNNY = (Material.RABBIT_SPAWN_EGG, "Killer Bunny")
    SNOW_GOLEM = (Material.GHAST_SPAWN_EGG, "Snow Golem")
    ILLUSIONER = (Material.VILLAGER_SPAWN_EGG, "Illusioner")
    GIANT = (Material.ZOMBIE_SPAWN_EGG, "Giant")
    WITHER = (Material.WITHER_SKELETON_SPAWN_EGG, "Wither")
    ENDERDRAGON = (Material.ENDERMAN_SPAWN_EGG, "Enderdragon")


@unique
class PotionEffect(AutoSnakeToCapitalizedWordsEnum):
    """Contains all types of potion effects available in DiamondFire."""
    ABSORPTION = auto()  #: Grants ``4 * level`` absorption (shield) health
    BAD_LUCK = auto()  #: Deteriorates drops from loot tables based on level
    BLINDNESS = auto()  #: Obscures the player's vision with black fog and prevents sprinting
    CONDUIT_POWER = auto()  #: Increases underwater vision, mining speed, and prevents drowning
    DOLPHINS_GRACE = "Dolphin's Grace"  #: Increases swimming speed by 40%
    FIRE_RESISTANCE = auto()  #: Grants immunity to fire and lava damage
    GLOWING = auto()  #: Draws an outline around the entity that is visible through walls
    HASTE = auto()  #: Increases mining speed by ``20% * level``, and attack speed by ``10% * level``
    HEALTH_BOOST = auto()  #: Increases maximum health by ``4 * level``
    HUNGER = auto()  #: Increases food exhaustion by ``0.1 * level`` per second
    INSTANT_DAMAGE = auto()  #: Instantly inflicts ``3 * 2 ^ level`` damage
    INSTANT_HEALTH = auto()  #: Instantly heals ``2 * 2 ^ level`` health
    INVISIBILITY = auto()  #: Causes the entity to disappear
    JUMP_BOOST = auto()  #: Increases jump height to ``0.5 + level``
    LEVITATION = auto()  #: Levitates the player upwards by ``0.875 * level``  blocks per second
    LUCK = auto()  #: Improves drops from loot tables based on level
    MINING_FATIGUE = auto()  #: Greatly reduces mining speed, and attack speed by ``10% * level``
    NAUSEA = auto()  #: Wobbles and warps the player's vision
    NIGHT_VISION = auto()  #: Enables vision at full brightness everywhere
    POISON = auto()  #: Deals 1 damage every ``1.25 * level`` seconds
    REGENERATION = auto()  #: Heals 1 health every ``2.5 * level`` seconds
    RESISTANCE = auto()  #: Reduces damage taken by ``20% * level``
    SATURATION = auto()  #: Instantly replenishes ``1 * level`` hunger and ``2 * level`` saturation, or do so each tick
    SLOW_FALLING = auto()  #: Reduces falling speed by 70% and prevents fall damage
    SLOWNESS = auto()  #: Reduces walking speed by ``15% * level``
    SPEED = auto()  #: Increases walking speed by ``20% * level``
    STRENGTH = auto()  #: Increases melee-dealt damage by ``3 * level``
    WATER_BREATHING = auto()  #: Prevents the loss of breath underwater
    WEAKNESS = auto()  #: Reduces melee-dealt damage by ``4 * level``
    WITHER = auto()  #: Deals 1 damage every ``2 * level`` seconds (and can kill)


@unique
class VariableScope(AutoLowerNameEnum):
    """Represents the possible Variable Scopes."""
    UNSAVED = auto()
    SAVED = auto()
    LOCAL = auto()


@unique
class GameValueType(AutoSnakeToCapitalizedWordsEnum):
    """Represents the types of Game Values there are in DiamondFire. In the Documentation of each item, the "Return
    Type" is what the game value actually represents functionally.
    """
    ARMOR_ITEMS = auto()
    """The items in the target's armor slots.

    Returns
    -------
    :attr:`~.Listable`
        Contains one Item entry for each armor slot (air if empty, 4 in total)
    """

    ARMOR_POINTS = auto()
    """The target's armor points, which has a base value that can be altered by items.

    Returns
    -------
    :attr:`~.Numeric`
        0.0 (no armor) to 20.0 (full bar)
    """

    ARMOR_TOUGHNESS = auto()
    """The target's armor toughness, which has a base value that can be altered by items.

    Returns
    -------
    :attr:`~.Numeric`
        0.0 or above (full set of diamond armor = 8.0)
    """

    ATTACK_DAMAGE = auto()
    """The target's attack damage, which has a base value that can be altered by items.

    Returns
    -------
    :attr:`~.Numeric`
        0.0 or higher (more damage)
    """

    ATTACK_SPEED = auto()
    """The target's attack speed, which has a base value that can be altered by items.

    Returns
    -------
    :attr:`~.Numeric`
        0.0 or higher (faster)
    """

    CPU_USAGE = auto()
    """The percent of the plot's CPU (as seen in /lagslayer) being used this instant.

    Returns
    -------
    :attr:`~.Numeric`
        Usage, from 0% to 100%
    """

    CLOSE_INVENTORY_EVENT_CAUSE = auto()
    """The reason the player's inventory was closed in this event.

    Returns
    -------
    :attr:`~.Textable`
        Close Cause: "player", "code", "open_new",  "teleport", "unloaded",  "cant_use", "disconnect",  "death", "unknown"
    """

    CURSOR_ITEM = auto()
    """The item on the target's cursor (used when moving items in the inventory).

    Returns
    -------
    :class:`~py2df.classes.mc_types.Item`
        Item on the cursor
    """

    DAMAGE_EVENT_CAUSE = auto()
    """The type of damage taken or dealt in this event.

    Returns
    -------
    :attr:`~.Textable`
        Damage Cause: ``"block_explosion"``, ``"contact"`` (cactus),  ``"cramming"``, ``"custom"`` (damage action),
        ``"dragon_breath"``, ``"drowning"``, ``"dryout"`` (fish on land), ``"entity_attack"``,  ``"entity_explosion"``,
        ``"entity_sweep_attack"``,  ``"fall"``, ``"falling_block"``, ``"fire"`` (in fire block),  ``"fire_tick"``,
        ``"fly_into_wall"``, ``"hot_floor"`` (magma block), ``"lava"``, ``"magic"``, ``"melting"`` (snowman),
        ``"poison"``, ``"projectile"``,  ``"starvation"`` ``"suffocation"``, ``"thorns"``,  ``"void"``, ``"wither"``
    """

    ENTITY_TYPE = auto()
    """The target's entity type.

    Returns
    -------
    :attr:`~.Textable`
        Entity type, e.g. "tipped_arrow" or "cow"
    """

    EVENT_BLOCK_FACE = auto()
    """The side of the block at which this event occurred.

    Returns
    -------
    :attr:`~.Textable`
        Block Face: "up", "down", "north", "east",  "south", "west", "none"
    """

    EVENT_BLOCK_LOCATION = auto()
    """The block this event occurred at.

    Returns
    -------
    :attr:`~.Locatable`
        Center of block
    """

    EVENT_BOW_POWER = auto()
    """The force percentage the bow was drawn with in the Shoot Bow event.

    Returns
    -------
    :attr:`~.Numeric`
        0.0% to 100.0% (fully charged)
    """

    EVENT_CLICKED_SLOT_INDEX = auto()
    """The index of the clicked inventory slot in this event.

    Returns
    -------
    :attr:`~.Numeric`
        From 1 (first slot) up to the inventory's size
    """

    EVENT_CLICKED_SLOT_ITEM = auto()
    """The inventory item clicked on in this event.

    Returns
    -------
    :class:`~py2df.classes.mc_types.Item`
        Item in slot (before the click event)
    """

    EVENT_CLICKED_SLOT_NEW_ITEM = auto()
    """The inventory item clicked with in this event.

    Returns
    -------
    :class:`~py2df.classes.mc_types.Item`
        Item in slot (after the click event)
    """

    EVENT_COMMAND = auto()
    """The entire command line entered in this event.

    Returns
    -------
    :attr:`~.Textable`
        Command, with the first "@" excluded
    """

    EVENT_COMMAND_ARGUMENTS = auto()
    """The separated parts of the event command.

    Returns
    -------
    :attr:`~.Listable`
        Contains one Text entry for each word in the command (split by " ")
    """

    EVENT_DAMAGE = auto()
    """The amount of damage dealt in this event.

    Returns
    -------
    :attr:`~.Numeric`
        0.0 or above
    """

    EVENT_ITEM = auto()
    """Gets the item in an item related event.

    Returns
    -------
    :class:`~py2df.classes.mc_types.Item`
        Main item in event
    """

    EVENT_NEW_HELD_SLOT = auto()
    """The hotbar slot the player is changing to in this event.

    Returns
    -------
    :attr:`~.Numeric`
        1 (leftmost slot) to 9 (rightmost slot)
    """

    EXPERIENCE_LEVEL = auto()
    """The target's experience level.

    Returns
    -------
    :attr:`~.Numeric`
        0 (no levels) or above
    """

    EXPERIENCE_PROGRESS = auto()
    """The target's experience progress to the next level.

    Returns
    -------
    :attr:`~.Numeric`
        0.0% (no progress) to 100.0% (next level)
    """

    EYE_LOCATION = auto()
    """The target's location, but adjusted to its eye height.

    Returns
    -------
    :attr:`~.Locatable`
        Eye location and rotation
    """

    FACING_DIRECTION = auto()
    """The direction the target is looking in.

    Returns
    -------
    :attr:`~.Textable`
        Direction: "north", "east", "south",  "west"
    """

    FALL_DISTANCE = auto()
    """The target's distance fallen in blocks.

    Returns
    -------
    :attr:`~.Numeric`
        0.0 (not falling) or higher (falling down)
    """

    FIRE_TICKS = auto()
    """Burn ticks remaining on the target.

    Returns
    -------
    :attr:`~.Numeric`
        0 (not on fire) or above (burning)
    """

    FOOD_EXHAUSTION = auto()
    """The target's exhaustion level, which is increased by the player's actions.

    Returns
    -------
    :attr:`~.Numeric`
        0.0 (minimum) to 4.0 (reset point)
    """

    FOOD_LEVEL = auto()
    """The target's remaining food points.

    Returns
    -------
    :attr:`~.Numeric`
        0 (starving) to 20 (full bar)
    """

    FOOD_SATURATION = auto()
    """The target's saturation level, which depends on the types of food consumed.

    Returns
    -------
    :attr:`~.Numeric`
        0.0 (minimum), up to the player's food level
    """

    HELD_SLOT = auto()
    """The target's selected hotbar slot index.

    Returns
    -------
    :attr:`~.Numeric`
        1 (leftmost slot) to 9 (rightmost slot)
    """

    HOTBAR_ITEMS = auto()
    """The target's current hotbar items.

    Returns
    -------
    :attr:`~.Listable`
        Contains one Item entry for each hotbar slot (air if empty, 9 in total)
    """

    INVENTORY_ITEMS = auto()
    """The target's inventory items (includes hotbar).

    Returns
    -------
    :attr:`~.Listable`
        Contains one Item entry for each inventory slot (air if empty, 36 in total)
    """

    INVENTORY_MENU_ITEMS = auto()
    """The target's current inventory menu items.

    Returns
    -------
    :attr:`~.Listable`
        Contains one Item entry for each menu slot (air if empty)
    """

    LOCATION = auto()
    """The target's location.

    Returns
    -------
    :attr:`~.Locatable`
        Location and rotation, at feet height
    """

    MAIN_HAND_ITEM = auto()
    """The target's currently held item.

    Returns
    -------
    :class:`~py2df.classes.mc_types.Item`
        Item in the selected hotbar slot
    """

    MAXIMUM_HEALTH = auto()
    """The target's maximum health points.

    Returns
    -------
    :attr:`~.Numeric`
        Maximum health, 1.0 or above
    """

    OFF_HAND_ITEM = auto()
    """The target's currently held off hand item.

    Returns
    -------
    :class:`~py2df.classes.mc_types.Item`
        Item in the offhand slot
    """

    OPEN_INVENTORY_TITLE = auto()
    """The title of the target's opened inventory.

    Returns
    -------
    :attr:`~.Textable`
        Inventory title, or "none" if no menu, or the player's inventory, is open
    """

    PITCH = auto()
    """The pitch (up/down rotation) of the target's position.

    Returns
    -------
    :attr:`~.Numeric`
        -90.0 to 90.0
    """

    PLAYER_COUNT = auto()
    """The amount of players playing on the plot.

    Returns
    -------
    :attr:`~.Numeric`
        Player count
    """

    POTION_EFFECTS = auto()
    """The target's active potion effects.

    Returns
    -------
    :attr:`~.Listable`
        Contains one  Potion Effect entry for each active effect on the target
    """

    REMAINING_AIR = auto()
    """The target's remaining air ticks.

    Returns
    -------
    :attr:`~.Numeric`
        0 (drowning) to 300 (maximum air)
    """

    REMAINING_HEALTH = auto()
    """The target's remaining health points.

    Returns
    -------
    :attr:`~.Numeric`
        0.0 (dead) up to the target's maximum health (20.0 by default)
    """

    SADDLE_ITEM = auto()
    """The target's currently worn saddle or carpet.

    Returns
    -------
    :class:`~py2df.classes.mc_types.Item`
        Item in the saddle/decor slot
    """

    SELECTION_SIZE = auto()
    """The amount of targets in the current selection.

    Returns
    -------
    :attr:`~.Numeric`
        0 (no targets) or above
    """

    SELECTION_TARGET_NAMES = auto()
    """The name of each target in the current selection.

    Returns
    -------
    :attr:`~.Listable`
        Contains one Text entry (name) for each target
    """

    SELECTION_TARGET_UUIDS = "Selection Target UUIDs"
    """The UUID of each target in the current selection.

    Returns
    -------
    :attr:`~.Listable`
        Contains one Text entry (UUID) for each target
    """

    SERVER_TPS = auto()
    """The amount of game Ticks Per Second the server is currently able to handle.

    Returns
    -------
    :attr:`~.Numeric`
        20.0 (no server lag) or below (decreases with more lag)
    """

    SERVER_TIME = auto()
    """Returns the server system time in seconds with millisecond precision.

    Returns
    -------
    :attr:`~.Numeric`
        Server time
    """

    SPAWN_LOCATION = auto()
    """The target's original spawn location.

    Returns
    -------
    :attr:`~.Locatable`
        Location this entity was created at
    """

    TARGET_BLOCK_FACE = auto()
    """The side of the block the target is looking at.

    Returns
    -------
    :attr:`~.Textable`
        Block Face: "up", "down", "north", "east",  "south", "west", "none"
    """

    TARGET_BLOCK_LOCATION = auto()
    """The block the target is looking at.

    Returns
    -------
    :attr:`~.Locatable`
        Center of block
    """

    TARGET_FLUID_LOCATION = auto()
    """The location of the block the target is looking at, also detecting fluids.

    Returns
    -------
    :attr:`~.Locatable`
        Center of block
    """

    TELEPORT_CAUSE = auto()
    """The cause of teleportation in player teleport events.

    Returns
    -------
    :attr:`~.Textable`
        Teleport Cause: "chorus_fruit", "end_gateway",  "end_portal", "ender_pearl",  "nether_portal", "spectate", 
    """

    UUID = "UUID"
    """The target's universally unique identifier.

    Returns
    -------
    :attr:`~.Textable`
        Target UUID
    """

    X_COORDINATE = "X-Coordinate"
    """The X coordinate of the target's position.

    Returns
    -------
    :attr:`~.Numeric`
        Coordinate
    """

    Y_COORDINATE = "Y-Coordinate"
    """The Y coordinate of the target's position.

    Returns
    -------
    :attr:`~.Numeric`
        Coordinate
    """

    YAW = auto()
    """The yaw (left/right rotation) of the target's position.

    Returns
    -------
    :attr:`~.Numeric`
        -180.0 to 180.0
    """

    Z_COORDINATE = "Z-Coordinate"
    """The Z coordinate of the target's position.

    Returns
    -------
    :attr:`~.Numeric`
        Coordinate
    """


GVAL_NUMERIC = [
    GameValueType.ARMOR_POINTS,
    GameValueType.ARMOR_TOUGHNESS,
    GameValueType.ATTACK_DAMAGE,
    GameValueType.ATTACK_SPEED,
    GameValueType.CPU_USAGE,
    GameValueType.EVENT_BOW_POWER,
    GameValueType.EVENT_CLICKED_SLOT_INDEX,
    GameValueType.EVENT_DAMAGE,
    GameValueType.EVENT_NEW_HELD_SLOT,
    GameValueType.EXPERIENCE_LEVEL,
    GameValueType.EXPERIENCE_PROGRESS,
    GameValueType.FALL_DISTANCE,
    GameValueType.FIRE_TICKS,
    GameValueType.FOOD_EXHAUSTION,
    GameValueType.FOOD_LEVEL,
    GameValueType.FOOD_SATURATION,
    GameValueType.HELD_SLOT,
    GameValueType.MAXIMUM_HEALTH,
    GameValueType.PITCH,
    GameValueType.PLAYER_COUNT,
    GameValueType.REMAINING_AIR,
    GameValueType.REMAINING_HEALTH,
    GameValueType.SELECTION_SIZE,
    GameValueType.SERVER_TPS,
    GameValueType.SERVER_TIME,
    GameValueType.X_COORDINATE,
    GameValueType.Y_COORDINATE,
    GameValueType.YAW,
    GameValueType.Z_COORDINATE
]

GVAL_TEXTABLE = [
    GameValueType.CLOSE_INVENTORY_EVENT_CAUSE,
    GameValueType.DAMAGE_EVENT_CAUSE,
    GameValueType.ENTITY_TYPE,
    GameValueType.EVENT_BLOCK_FACE,
    GameValueType.EVENT_COMMAND,
    GameValueType.FACING_DIRECTION,
    GameValueType.OPEN_INVENTORY_TITLE,
    GameValueType.TARGET_BLOCK_FACE,
    GameValueType.TELEPORT_CAUSE,
    GameValueType.UUID
]

GVAL_LOCATABLE = [
    GameValueType.EVENT_BLOCK_LOCATION,
    GameValueType.EYE_LOCATION,
    GameValueType.LOCATION,
    GameValueType.SPAWN_LOCATION,
    GameValueType.TARGET_BLOCK_LOCATION,
    GameValueType.TARGET_FLUID_LOCATION
]

GVAL_LISTABLE = [
    GameValueType.ARMOR_ITEMS,
    GameValueType.EVENT_COMMAND_ARGUMENTS,
    GameValueType.HOTBAR_ITEMS,
    GameValueType.INVENTORY_ITEMS,
    GameValueType.INVENTORY_MENU_ITEMS,
    GameValueType.POTION_EFFECTS,
    GameValueType.SELECTION_TARGET_NAMES,
    GameValueType.SELECTION_TARGET_UUIDS
]

GVAL_ITEM = [
    GameValueType.CURSOR_ITEM,
    GameValueType.EVENT_CLICKED_SLOT_ITEM,
    GameValueType.EVENT_CLICKED_SLOT_NEW_ITEM,
    GameValueType.EVENT_ITEM,
    GameValueType.MAIN_HAND_ITEM,
    GameValueType.OFF_HAND_ITEM,
    GameValueType.SADDLE_ITEM
]

