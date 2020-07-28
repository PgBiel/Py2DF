"""
Dataclasses; classes whose only purpose is to hold specific data.
"""
import typing
import math
from .. import constants
from .abc import JSONData, Settable, Block
from ..enums import Enchantments, TagType, CodeblockActionType, BlockType, BracketDirection, BracketType
from ..utils import remove_u200b_from_doc, all_attr_eq
from ..constants import DEFAULT_VAL, ITEM_ID_TAG

AnyNumber = typing.Union[int, float]


class Enchantment(Settable):
    """
    Represents an Enchantment to be used within :class:`~py2df.classes.mc_types.Item`.

    Parameters\u200b
    ----------
    ench_type : :class:`~py2df.enums.misc_mc_enums.Enchantments`
        The type of enchantment this is.

    level : :class:`int`, optional
        The level of this enchantments (default is 1).


    .. container:: comparisons

       .. describe:: a == b, a != b

            Checks if every attribute is the same.

       .. describe::  a > b, a >= b, a < b, a <= b

            Compares both of the enchantments' levels.


    .. container:: operations

        Note that, in all operations, ``a`` must be an instance of :class:`Enchantment` , while ``b`` can either be
        another instance of the class or be an :class:`int` (or :class:`float` - the results are rounded down).

        .. describe:: a + b, a - b, a * b, a ** b, a / b, a // b

            Executes said operation on both's levels.

        .. describe:: str(a)

            Returns a string in the form "{ench_type} x {level}".

        .. describe:: hash(a)

            Returns an unique hash representing the Enchantment class, the instance's enchantment type and its
            level.

    
    Attributes\u200b
    -----------
        ench_type : :class:`~py2df.enums.misc_mc_enums.Enchantments`
            Type of enchantment.
        
        level : :class:`int`
            The level of this enchantment. (Cannot surpass **2 147 483 647**)
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
        self.ench_type = Enchantments(ench_type)

        self.level = int(level)

        if abs(self.level) > constants.MAX_ENCHANTMENT_LEVEL:
            raise OverflowError(f"Enchantment level too big (max {constants.MAX_ENCHANTMENT_LEVEL})")

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
        return hash((self.__class__, self.ench_type, self.level))

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


class Tag(JSONData):
    """
    Represents a tag, generally for internal use.

    Parameters
    ----------\u200b
    tag : str
        The tag's name.

    option : Union[:class:`bool`, :class:`int`, :class:`str`, :class:`~py2df.enums.enum_util.TagType`]
        The option chosen for this tag.

    action : :class:`~py2df.enums.enum_util.CodeblockActionType`
        The action type of the codeblock this tag is in.

    block : :class:`~py2df.enums.parameters.BlockType`
        The type of codeblock this tag is in.

    Attributes
    ----------\u200b
        tag : str
            The tag's name.

        option : Union[:class:`bool`, :class:`int`, :class:`str`, :class:`~py2df.enums.enum_util.TagType`]
            The option chosen for this tag.

        action : :class:`~py2df.enums.enum_util.CodeblockActionType`
            The action type of the codeblock this tag is in.

        block : :class:`~py2df.enums.parameters.BlockType`
            The type of codeblock this tag is in.
    """
    tag: str
    option: typing.Union[bool, int, TagType]
    action: CodeblockActionType
    block: BlockType

    def __init__(
        self, tag: str, option: typing.Union[bool, int, str, TagType], action: CodeblockActionType, block: BlockType
    ):
        """
        Initializes this tag.

        Parameters
        ----------
        tag : str
            The tag's name.

        option : Union[:class:`bool`, :class:`int`, :class:`str`, :class:`~py2df.enums.enum_util.TagType`]
            The option chosen for this tag.

        action : :class:`~py2df.enums.enum_util.CodeblockActionType`
            The action type of the codeblock this tag is in.

        block : :class:`~py2df.enums.parameters.BlockType`
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

        block : :class:`~py2df.enums.parameters.BlockType`, optional
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


class Bracket(Block, JSONData):
    """Represents a Bracket block (used within If's and Repeats).

    Parameters
    ----------\u200b
    direction : :class:`~py2df.enums.parameters.BracketDirection`
        The direction of this bracket (one of :attr:`~py2df.enums.parameters.BracketDirection.OPEN`
        and :attr:`~py2df.enums.parameters.BracketDirection.CLOSE`).

    bracket_type : :class:`~py2df.enums.parameters.BracketType`
        The type of this bracket, determining where it is used (either used on If's, represented by
        :attr:`~py2df.enums.parameters.BracketType.NORM`, or with a Repeat, represented by
        :attr:`~py2df.enums.parameters.BracketType.REPEAT`).

    Attributes
    ----------\u200b
    direction : :class:`~py2df.enums.parameters.BracketDirection`
        The direction of this bracket (one of :attr:`~py2df.enums.parameters.BracketDirection.OPEN`
        and :attr:`~py2df.enums.parameters.BracketDirection.CLOSE`).

    bracket_type : :class:`~py2df.enums.parameters.BracketType`
        The type of this bracket, determining where it is used (either used on If's, represented by
        :attr:`~py2df.enums.parameters.BracketType.NORM`, or with a Repeat, represented by
        :attr:`~py2df.enums.parameters.BracketType.REPEAT`).
    """
    __slots__ = ("direction", "bracket_type")
    direction: BracketDirection
    bracket_type: BracketType

    def __init__(self, direction: BracketDirection, bracket_type: BracketType):
        """
        Inits this Bracket.

        Parameters
        ----------
        direction : :class:`~py2df.enums.parameters.BracketDirection`
            The direction of this bracket (one of :attr:`~py2df.enums.parameters.BracketDirection.OPEN`
            and :attr:`~py2df.enums.parameters.BracketDirection.CLOSE`).

        bracket_type : :class:`~py2df.enums.parameters.BracketType`
            The type of this bracket, determining where it is used (either used on If's, represented by
            :attr:`~py2df.enums.parameters.BracketType.NORM`, or with a Repeat, represented by
            :attr:`~py2df.enums.parameters.BracketType.REPEAT`).
        """
        self.direction: BracketDirection = BracketDirection(direction)
        self.bracket_type: BracketType = BracketType(bracket_type)

    def as_json_data(self) -> dict:
        """Produces a JSON-serializable dict representing this Bracket.

        Returns
        -------
        :class:`dict`
            A JSON-serializable dict representing this Bracket.
        """
        return dict(
            id=constants.BRACKET_ID,
            direct=self.direction.value,
            type=self.bracket_type.value
        )

    def __repr__(self):
        return f"<{self.__class__.__name__} direction={repr(self.direction.value)} \
bracket_type={repr(self.bracket_type.value)}"


remove_u200b_from_doc(Enchantment, Tag, Bracket)
