import typing
from .enum_util import AutoLowerNameEnum
from enum import auto, unique, IntFlag
from ..constants import SECTION_SIGN
from ..utils import remove_u200b_from_doc


class HideFlags(IntFlag):
    """Represents flags to hide from an :class:`~.Item` (i.e., to not display). Note that they can be OR'ed to
    hide multiple flags (i.e., ``a | b`` to hide both `a` and `b`). Use HIDE_ALL_FLAGS for all flags combined.

    Note that this subclasses :class:`enum.IntFlag` which, in turn, subclasses :class:`int`, meaning all integer
    operations are supported.


    .. container:: comparisons

        .. describe:: a == b, a != b

            Checks if two HideFlags instances represent the same flags.

        .. describe:: a > b, a < b, a >= b, a <= b

            Compares the HideFlags instances' values.

    .. container:: operations

        Note that all integer operations not listed here are supported, but return an :class:`int` instead of a
        :class:`HideFlags` (when applicable).

        .. describe:: a | b

            Combines both flags. (E.g.: ``HideFlags.ENCHANTMENTS | HideFlags.ATTRIBUTE_MODIFIERS`` means that
            both enchantments and attribute modifiers should be hidden from the item.)

        .. describe:: ~a

            Obtains a :class:`HideFlags` instance representing all except `a`'s flag(s).

        .. describe:: b in a

            Returns ``True`` if `a` contains all of `b`'s flags, otherwise ``False``.

        .. describe:: a & b, a ^ b

            Runs the specified logic operations (AND and XOR, respectively) between the values,
            returning the corresponding :class:`HideFlags` instance.

        .. describe:: a + b, a - b, a / b, ...

            Executes the given operation in the same way as integers.


    Attributes
    ----------\u200b
    value : :class:`int`
        The unique integer representing the hidden flags of this instance. This is the value used
        when executing integer operations (such as ``a + b`` or ``a - b``).
    """
    ENCHANTMENTS = 1
    ATTRIBUTE_MODIFIERS = 2
    UNBREAKABLE = 4
    BLOCKS_CAN_DESTROY = 8
    BLOCKS_CAN_PLACE_ON = 16
    MISC_FLAGS = 32  # such as potion effects, "StoredEnchantments", written book "generation" and "author",
    # "Explosion", "Fireworks", and map tooltips

    def __repr__(self):  # from `re.RegexFlag`
        if self._name_ is not None:
            return f'HideFlags.{self._name_}'
        value = self._value_
        members = []
        negative = value < 0
        if negative:
            value = ~value
        for m in self.__class__:
            if value & m._value_:
                value &= ~m._value_
                members.append(f'HideFlags.{m._name_}')
        if value:
            members.append(hex(value))
        res = '|'.join(members)
        if negative:
            if len(members) > 1:
                res = f'~({res})'
            else:
                res = f'~{res}'
        return res


ALL_HIDE_FLAGS = HideFlags(sum(list(HideFlags)))
"""The :class:`HideFlags` instance containing all flags, meaning all kinds of flags should be hidden."""


@unique
class Enchantments(AutoLowerNameEnum):
    """Enchantment types in Minecraft 1.14.4."""
    AQUA_AFFINITY         = auto()
    BANE_OF_ARTHROPODS    = auto()
    BINDING_CURSE         = auto()
    BLAST_PROTECTION      = auto()
    CHANNELING            = auto()
    DEPTH_STRIDER         = auto()
    EFFICIENCY            = auto()
    FEATHER_FALLING       = auto()
    FIRE_ASPECT           = auto()
    FIRE_PROTECTION       = auto()
    FLAME                 = auto()
    FORTUNE               = auto()
    FROST_WALKER          = auto()
    IMPALING              = auto()
    INFINITY              = auto()
    KNOCKBACK             = auto()
    LOOTING               = auto()
    LOYALTY               = auto()
    LUCK_OF_THE_SEA       = auto()
    LURE                  = auto()
    MENDING               = auto()
    MULTISHOT             = auto()
    PIERCING              = auto()
    POWER                 = auto()
    PROJECTILE_PROTECTION = auto()
    PROTECTION            = auto()
    PUNCH                 = auto()
    QUICK_CHARGE          = auto()
    RESPIRATION           = auto()
    RIPTIDE               = auto()
    SHARPNESS             = auto()
    SILK_TOUCH            = auto()
    SMITE                 = auto()
    SWEEPING              = auto()
    THORNS                = auto()
    UNBREAKING            = auto()
    VANISHING_CURSE       = auto()


class Color:
    """Represents all possible colors and formats of Minecraft. Accessing any attribute returns a string."""
    BLACK         = SECTION_SIGN + "0"
    DARK_BLUE     = SECTION_SIGN + "1"
    DARK_GREEN    = SECTION_SIGN + "2"
    DARK_AQUA     = SECTION_SIGN + "3"
    DARK_RED      = SECTION_SIGN + "4"
    DARK_PURPLE   = SECTION_SIGN + "5"
    GOLD          = SECTION_SIGN + "6"
    GRAY          = SECTION_SIGN + "7"
    DARK_GRAY     = SECTION_SIGN + "8"
    BLUE          = SECTION_SIGN + "9"
    GREEN         = SECTION_SIGN + "a"
    AQUA          = SECTION_SIGN + "b"
    RED           = SECTION_SIGN + "c"
    LIGHT_PURPLE  = SECTION_SIGN + "d"
    YELLOW        = SECTION_SIGN + "e"
    WHITE         = SECTION_SIGN + "f"
    OBFUSCATED    = SECTION_SIGN + "k"
    BOLD          = SECTION_SIGN + "l"
    STRIKETHROUGH = SECTION_SIGN + "m"
    UNDERLINE     = SECTION_SIGN + "n"
    ITALIC        = SECTION_SIGN + "o"
    RESET         = SECTION_SIGN + "r"


Colour = Color  # alias


remove_u200b_from_doc(HideFlags)
