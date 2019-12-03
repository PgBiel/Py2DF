from .enum_util import AutoSnakeToCapitalizedWordsEnum
from enum import auto, unique


@unique
class ParticleType(AutoSnakeToCapitalizedWordsEnum):
    """Contains all types of particles usable in DiamondFire."""
    ANGRY_VILLAGER = auto()
    BARRIER = auto()
    BUBBLE = auto()
    BUBBLE_POP = auto()
    CLOUD = auto()
    CONDUIT = auto()
    CRIT = auto()
    DAMAGE_HEARTS = auto()
    DOLPHIN_TRAIL = auto()
    DRAGON_BREATH = auto()
    ELDER_GUARDIAN = auto()
    ENCHANTMENT_RUNES = auto()
    END_ROD = auto()
    FIREWORK_SPARKLES = auto()
    FISHING_TRAIL = auto()
    FLAME = auto()
    HAPPY_VILLAGER = auto()
    HEART = auto()
    HUGE_EXPLOSION = auto()
    LARGE_EXPLOSION = auto()
    LARGE_SMOKE = auto()
    LAVA = auto()
    LAVA_DRIP = auto()
    MAGIC_CRIT = auto()
    MOB_SPELL = auto()
    MUSIC_NOTE = auto()
    MYCELIUM = auto()
    PORTAL = auto()
    RAIN_SPLASH = auto()
    REDSTONE = auto()
    SLIME = auto()
    SMALL_EXPLOSION = auto()
    SMOKE = auto()
    SNOWBALL = auto()
    SPIT = auto()
    SQUID_INK = auto()
    SWEEP_ATTACK = auto()
    TOTEM = auto()
    WATER_DRIP = auto()
    WATER_SPLASH = auto()
    WITCH_MAGIC = auto()


@unique  # <- still don't know which enum type to use! Snake->Words? Snake->Pascal?
class CustomSpawnEggType(AutoSnakeToCapitalizedWordsEnum):
    pass  # TODO: Use in Minecraft and find out its json; Ender Dragon, Giant, Iron/Snow Golem, etc


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
class GameValueType(AutoSnakeToCapitalizedWordsEnum):
    pass  # TODO: Use in Minecraft and find out its json
