"""
Dataclasses; classes whose only purpose is to hold specific data.
"""
import typing
import math
from .. import constants
from .abc import JSONData, Settable
from ..enums import Enchantments, TagType, CodeblockActionType, BlockType
from ..utils import remove_u200b_from_doc, all_attr_eq
from ..constants import DEFAULT_VAL, ITEM_ID_TAG

AnyNumber = typing.Union[int, float]


class Enchantment(Settable):
    """
    Represents an Enchantment to be used within :class:`~py2df.classes.mc_types.Item`.
    
    Attributes\u200b
    -----------
        ench_type : :class:`~py2df.enums.misc_mc_enums.Enchantments`
            Type of enchantment.
        
        level : :class:`int`
            The level of this enchantment. (Cannot surpass **{0}**)

    **Supported comparisons**

    ``a == b``: Checks if every attribute is the same.

    ``a != b``: Same as ``not a == b``

    ``a > b``, ``a >= b``, ``a < b``, ``a <= b``: Compares both of the enchantments' levels.

    **Supported operations**

    ``a + b``, ``a - b``, ``a * b``, ``a ** b``, ``a / b``, ``a // b``: Executes said operation on both's levels.

    ``a += b``, ``a -= b``...: Executes said operation on both's levels and sets to the new :class:`Enchantment` .

    Note that, in all operations, ``a`` must be an instance of :class:`Enchantment` , while ``b`` can either be
    another instance of the class or be an :class:`int` (or :class:`float` - the results are rounded down).
    """
    __slots__ = ("ench_type", "level")
    ench_type: Enchantments
    level: int

    def __init__(self, ench_type: Enchantments, level: int = 1):
        """
        Initialize this Enchantment.

        Parameters
        ----------
        ench_type : :class:`~py2df.enums.misc_mc_enums.Enchantments`
            The type of enchantment this is.

        level : :class:`int`, optional
            The level of this enchantments (default is 1).
        """
        if abs(self.level) > constants.MAX_ENCHANTMENT_LEVEL:
            raise OverflowError(f"Enchantment level too big (max {constants.MAX_ENCHANTMENT_LEVEL})")

        self.ench_type = Enchantments(ench_type)

        self.level = int(level)

    def __repr__(self):
        return f"<{self.__class__.__name__} ench_type={self.ench_type.value} level={self.level}>"

    def __str__(self):
        return self.ench_type.value + f" * {self.level}"

    def copy(self) -> "Enchantment":
        """
        Produces an identical copy of this :class:`Enchantment` object.

        Returns
        -------
        :class:`Enchantment`
            The identical copy of this object.
        """
        return Enchantment(self.ench_type, self.level)

    def set(self, ench_type: Enchantments = DEFAULT_VAL, level: int = DEFAULT_VAL) -> "Enchantment":
        """
        Sets the values of this :class:`Enchantment` .

        Parameters
        ----------
        ench_type : :class:`~py2df.enums.misc_mc_enums.Enchantments`, optional
            The type of enchantment this is.

        level : :class:`int`
            The level of this enchantment.

        Returns
        -------
        :class:`Enchantment`
            self to allow chaining
        """
        if ench_type != DEFAULT_VAL:
            self.ench_type = Enchantments(ench_type)

        if level != DEFAULT_VAL:
            self.level = int(level)

        return self

    def __eq__(self, other: "Enchantment") -> bool:
        return all_attr_eq(self, other)

    def __ne__(self, other: "Enchantment") -> bool:
        return not self.__eq__(other)

    def __lt__(self, other: typing.Union["Enchantment", AnyNumber]):
        if type(self) == type(other):
            return self.level < other.level
        else:
            return self.level < other

    def __le__(self, other: typing.Union["Enchantment", AnyNumber]):
        if type(self) == type(other):
            return self.level <= other.level
        else:
            return self.level <= other

    def __gt__(self, other: typing.Union["Enchantment", AnyNumber]):
        if type(self) == type(other):
            return self.level > other.level
        else:
            return self.level > other

    def __ge__(self, other: typing.Union["Enchantment", AnyNumber]):
        if type(self) == type(other):
            return self.level >= other.level
        else:
            return self.level >= other

    def __hash__(self):
        return hash((self.__class__.__name__, self.ench_type.value, self.level))

    def __add__(self, other: typing.Union["Enchantment", AnyNumber]):
        new = self.copy()
        new.level += other.level if type(self) == type(other) else other
        new.level = int(new.level)
        return new

    def __radd__(self, other: typing.Union["Enchantment", AnyNumber]):
        return self.__add__(other)

    def __mul__(self, other: typing.Union["Enchantment", AnyNumber]):
        new = self.copy()
        new.level *= other.level if type(self) == type(other) else other
        new.level = int(new.level)
        return new

    def __rmul__(self, other: typing.Union["Enchantment", AnyNumber]):
        return self.__mul__(other)

    def __sub__(self, other: typing.Union["Enchantment", AnyNumber]):
        new = self.copy()
        new.level -= other.level if type(self) == type(other) else other
        new.level = int(new.level)
        return new

    def __truediv__(self, other: typing.Union["Enchantment", AnyNumber]):
        new = self.copy()
        new.level /= other.level if type(self) == type(other) else other
        new.level = int(new.level)
        return new

    def __floordiv__(self, other: typing.Union["Enchantment", AnyNumber]):
        new = self.copy()
        new.level //= other.level if type(self) == type(other) else other
        new.level = int(new.level)
        return new

    def __mod__(self, other: typing.Union["Enchantment", AnyNumber]):
        new = self.copy()
        new.level %= other.level if type(self) == type(other) else other
        new.level = int(new.level)
        return new

    def __pow__(self, other: typing.Union["Enchantment", AnyNumber], modulo=None):
        new = self.copy()
        new.level = int(pow(
            self.level, other.level if type(self) == type(other) else other, modulo
        ))
        return new

    def __abs__(self):
        return self.copy().set(level=abs(self.level))

    def __pos__(self):
        return self.copy()


Enchantment.__doc__ = str(Enchantment.__doc__).format(constants.MAX_ENCHANTMENT_LEVEL)


class Tag(JSONData):
    """
    Represents a tag, generally for internal use.

    Attributes
    ----------\u200b
        tag : str
            The tag's name.

        option : Union[:class:`bool`, :class:`int`, :class:`~py2df.enums.enum_util.TagType`]
            The option chosen for this tag.

        action : :class:`~py2df.enums.enum_util.CodeblockActionType`
            The action type of the codeblock this tag is in.

        block : :class`~py2df.enums.parameters.BlockType`
            The type of codeblock this tag is in.
    """
    tag: str
    option: typing.Union[bool, int, TagType]
    action: CodeblockActionType
    block: BlockType

    def __init__(
        self, tag: str, option: typing.Union[bool, int, TagType], action: CodeblockActionType, block: BlockType
    ):
        """
        Initializes this tag.

        Parameters
        ----------
        tag : str
            The tag's name.

        option : Union[:class:`bool`, :class:`int`, :class:`~py2df.enums.enum_util.TagType`]
            The option chosen for this tag.

        action : :class:`~py2df.enums.enum_util.CodeblockActionType`
            The action type of the codeblock this tag is in.

        block : :class`~py2df.enums.parameters.BlockType`
            The type of codeblock this tag is in.
        """
        self.tag = str(tag)
        self.option = option
        self.action = action
        self.block = BlockType(block)

    def as_json_data(self) -> dict:
        """
        Produces a JSON-serializable dict representing this tag.

        Returns
        -------
        :class:`dict`
        """
        return dict(
            id=ITEM_ID_TAG,
            data=dict(
                option=getattr(self.option, "value", str(self.option)),
                tag=str(self.tag),
                action=getattr(self.action, "value", str(self.action)),
                block=getattr(self.block, "value", str(self.block))
            )
        )

    def set(
        self, tag: str = DEFAULT_VAL, option: typing.Union[bool, int, TagType] = DEFAULT_VAL,
        action: CodeblockActionType = DEFAULT_VAL, block: BlockType = DEFAULT_VAL
    ) -> "Tag":
        """
        Sets given :class:`Tag` attributes.

        Parameters
        ----------
        tag : str, optional
            The tag's name.

        option : Union[:class:`bool`, :class:`int`, :class:`~py2df.enums.enum_util.TagType`], optional
            The option chosen for this tag.

        action : :class:`~py2df.enums.enum_util.CodeblockActionType`, optional
            The action type of the codeblock this tag is in.

        block : :class`~py2df.enums.parameters.BlockType`, optional
            The type of codeblock this tag is in.

        Returns
        -------
        :class:`Tag`
            self to allow chaining
        """
        if tag != DEFAULT_VAL:
            self.tag = str(tag)

        if option != DEFAULT_VAL:
            self.option = option

        if action != DEFAULT_VAL:
            self.action = action

        if block != DEFAULT_VAL:
            self.block = BlockType(block)

        return self

    def __eq__(self, other):
        return all_attr_eq(self, other)

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} tag={self.tag} option={self.option} action={self.action} \
block={self.block}>"

    def __str__(self) -> str:
        return self.tag

    def __hash__(self):
        return hash((self.__class__.__name__, self.tag, str(self.option), str(self.action), str(self.block)))


remove_u200b_from_doc(Enchantment, Tag)
