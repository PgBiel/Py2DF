import typing
from .enum_util import AutoLowerNameEnum
from enum import auto, unique, Enum


@unique
class HideFlags(Enum):
    """
    List of flags to hide. Note that they can be summed to combine multiple flags. ALL has all flags combined.

    Supported operations:
    ---------------------
    `a + b`: Combines both flags. (E.g.: HideFlags.ENCHANTMENTS + HideFlags.ATTRIBUTE_MODIFIERS)

    `a | b`: Same as `a + b`; combines flags.

    `a - b`: Removes a flag from a combination of flags. (E.g.: HideFlags.ALL - HideFlags.ENCHANTMENTS)
    """
    ENCHANTMENTS = 1
    ATTRIBUTE_MODIFIERS = 2
    UNBREAKABLE = 4
    BLOCKS_CAN_DESTROY = 8
    BLOCKS_CAN_PLACE_ON = 16
    MISC_FLAGS = 32  # such as potion effects, "StoredEnchantments", written book "generation" and "author",
    ALL = 63         # "Explosion", "Fireworks", and map tooltips

    def __add__(self, other: "HideFlags"):
        if not isinstance(other, type(self)):
            raise TypeError(f"Incompatible operation types {type(self)} and {type(other)}")

        return _HideFlagsSum(self.value | other.value)

    def __or__(self, other: "HideFlags"):
        return self.__add__(other)

    def __sub__(self, other: "HideFlags"):
        if not isinstance(other, type(self)):
            raise TypeError(f"Incompatible operation types {type(self)} and {type(other)}")

        return _HideFlagsSum(abs(self.value - other.value))


class _HideFlagsSum(HideFlags):  # subclass to allow `isinstance` checks
    __slots__ = ("value",)

    def __init__(self, value: int):
        self.value: int = value


@unique
class Enchantments(AutoLowerNameEnum):
    AQUA_AFFINITY = auto()
    BANE_OF_ARTHROPODS = auto()
    BINDING_CURSE = auto()
    BLAST_PROTECTION = auto()
    CHANNELING = auto()
    DEPTH_STRIDER = auto()
    EFFICIENCY = auto()
    FEATHER_FALLING = auto()
    FIRE_ASPECT = auto()
    FIRE_PROTECTION = auto()
    FLAME = auto()
    FORTUNE = auto()
    FROST_WALKER = auto()
    IMPALING = auto()
    INFINITY = auto()
    KNOCKBACK = auto()
    LOOTING = auto()
    LOYALTY = auto()
    LUCK_OF_THE_SEA = auto()
    LURE = auto()
    MENDING = auto()
    MULTISHOT = auto()
    PIERCING = auto()
    POWER = auto()
    PROJECTILE_PROTECTION = auto()
    PROTECTION = auto()
    PUNCH = auto()
    QUICK_CHARGE = auto()
    RESPIRATION = auto()
    RIPTIDE = auto()
    SHARPNESS = auto()
    SILK_TOUCH = auto()
    SMITE = auto()
    SWEEPING = auto()
    THORNS = auto()
    UNBREAKING = auto()
    VANISHING_CURSE = auto()
