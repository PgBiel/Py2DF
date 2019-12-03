"""
Generic base classes for the library.
"""
import abc
from ..enums import BlockType
from ..utils import remove_u200b_from_doc
import typing

from .mc_types import Item

# region:Codeblock


class Codeblock(metaclass=abc.ABCMeta):
    """An ABC that describes any codeblock - event, action etc.
    
    Attributes\u200b
    -------------
        block : :class:`~py2df.enums.parameters.BlockType`
            Type of block. (Class var)
    
        args : :class:`~py2df.classes.collections.Arguments`
            Arguments of this codeblock (Instance var)
    
        action : :class:`~py2df.enums.enum_util.CodeBlockActionType`
            Specific action/description of it - e.g. event name (Class var)
    
        length : :class:`int`
            The space, in Minecraft blocks, that this codeblock occupies. (Most are 2, but some, like IFs, are 1)
            (Class var)
    """
    # block: BlockType
    # args: Arguments
    # action: CodeblockActionType
    # length: int
    __slots__ = ()

    @classmethod
    def __subclasshook__(cls, o_cls: type):
        """
        Checks if the given class is a subclass of Codeblock (implements it).
        :param o_cls: Class to check.
        :return: True if subclass; NotImplemented otherwise
        """

        if cls is Codeblock:
            attribs = ["block", "action", "length"]  # must have those attributes to be a codeblock.
            if all(any(attr in B.__dict__ for B in o_cls.__mro__) for attr in attribs):
                return True
        return NotImplemented


class ActionBlock(metaclass=abc.ABCMeta):
    """An ABC that describes any action - Player Action, Game Action, Entity Action or Control.
    Must implement :class:`Codeblock`.

    Includes all of :class:`Codeblock` 's attributes, plus:

    Attributes\u200b
    -----------
        block : Union[:attr:`~py2df.enums.parameters.BlockType.PLAYER_ACTION`, \
:attr:`~py2df.enums.action.BlockType.ENTITY_ACTION`, :attr:`~py2df.enums.action.BlockType.GAME_ACTION`, \
:attr:`~py2df.enums.action.CONTROL`]
            The block type - either `Player Action`, `Entity Action`. `Game Action` or `Control`.
    """
    __slots__ = ()

    @classmethod
    def __subclasshook__(cls, o_cls: type):
        """
        Checks if the given class is a subclass of Action (implements it).
        :param o_cls: Class to check.
        :return: True if subclass; NotImplemented otherwise
        """

        if cls is ActionBlock:
            if Codeblock.__subclasshook__(o_cls) is NotImplemented:  # must be a Codeblock
                return NotImplemented

            try:  # TODO: Entity action
                if BlockType(getattr(o_cls, "block")) in (
                        BlockType.PLAYER_ACTION, BlockType.GAME_ACTION, BlockType.CONTROL, BlockType.ENTITY_ACTION
                ):
                    return True  # must be one of BlockType.PLAYER_ACTION or BlockType.GAME_ACTION
            except ValueError:  # not a valid block type
                return NotImplemented  # not an Action

        return NotImplemented  # #


class EventBlock(metaclass=abc.ABCMeta):
    """
    An ABC that describes any event - Player Event or Entity Event. Must implement :class:`Codeblock`.

    Includes all of :class:`Codeblock` 's attributes, plus:

    Attributes\u200b
    -----------
        block : Union[:attr:`~py2df.enums.parameters.BlockType.PLAYER_EVENT`, \
:attr:`~py2df.enums.action.BlockType.ENTITY_EVENT`]
            The block type - either `Player Event` or `Entity Event`.
    """
    __slots__ = ()

    @classmethod
    def __subclasshook__(cls, o_cls: type):
        """
        Checks if the given class is a subclass of Event (implements it).
        :param o_cls: Class to check.
        :return: True if subclass; NotImplemented otherwise
        """

        if cls is EventBlock:
            if Codeblock.__subclasshook__(o_cls) is NotImplemented:
                return NotImplemented

            try:
                if BlockType(getattr(o_cls, "block")) in (BlockType.PLAYER_EVENT, BlockType.ENTITY_EVENT):  # be event.
                    return True
            except ValueError:  # not a valid block type
                return NotImplemented  # not an Event

        return NotImplemented


class BracketedBlock(metaclass=abc.ABCMeta):
    """
    An ABC that describes any codeblock with brackets. Can be used on a `with` construct. Must implement
    :class:`CodeBlock`."""
    __slots__ = ()

    @classmethod
    def __subclasshook__(cls, o_cls: type):
        """
        Checks if the given class is a subclass of BracketedBlock (implements it).
        :param o_cls: Class to check.
        :return: True if subclass; NotImplemented otherwise
        """

        if cls is BracketedBlock:
            if Codeblock.__subclasshook__(o_cls) is NotImplemented:  # must be a Codeblock
                return NotImplemented

            attribs = ["__exit__", "__enter__"]  # must have those attributes to be a bracket block. (Used in a `with`)
            if all(any(attr in B.__dict__ for B in o_cls.__mro__) for attr in attribs):
                return True

        return NotImplemented

    @abc.abstractmethod
    def __enter__(self):
        """Places the OPEN bracket. Can have two types: :attr:`~py2df.enums.parameters.BracketType.NORM`
        and :attr:`~py2df.enums.parameters.BracketType.REPEAT`
        """
        raise NotImplementedError

    @abc.abstractmethod
    def __exit__(self):
        """Places the CLOSE bracket. Can have two types: :attr:`~py2df.enums.parameters.BracketType.NORM`
        and :attr:`~py2df.enums.parameters.BracketType.REPEAT`
        """
        raise NotImplementedError


class CallableBlock(metaclass=abc.ABCMeta):
    """An ABC that describes any callable - Function or Process. Must implement :class:`Codeblock`.

    Includes all of :class:`Codeblock` 's attributes, plus:

    Attributes\u200b
    ------------
        block : Union[:attr:`~py2df.enums.parameters.BlockType.FUNCTION`, \
:attr:`~py2df.enums.parameters.BlockType.PROCESS`]
            The type of the callable block - `Function` or `Process`.
    """
    __slots__ = ()

    @classmethod
    def __subclasshook__(cls, o_cls: type):
        """
        Checks if the given class is a subclass of Event (implements it).
        :param o_cls: Class to check.
        :return: True if subclass; NotImplemented otherwise
        """

        if cls is CallableBlock:
            if Codeblock.__subclasshook__(o_cls) is NotImplemented:
                return NotImplemented

            try:
                if BlockType(getattr(o_cls, "block")) in (BlockType.FUNCTION, BlockType.PROCESS):
                    return True
            except ValueError:  # not a valid block type
                return NotImplemented  # not a CallableBlock

        return NotImplemented

# endregion:Codeblock

# region:JSONData


class JSONData(metaclass=abc.ABCMeta):
    """An ABC that describes a class implementing ``.as_json_data()``."""
    __slots__ = ()

    @abc.abstractmethod
    def as_json_data(self) -> typing.Union[str, int, float, dict, list, tuple, bool]:
        """Exports this class as parsed json data (not as string, but as a valid json data type).

        Returns
        -------
        Union[:class:`str`, :class:`int`, :class:`float`, :class:`dict`, :class:`list`, :class:`tuple`, :class:`bool`]
        """
        raise NotImplementedError

    @classmethod
    def __subclasshook__(cls, o_cls: type):
        """
        Checks if the given class is a subclass of JSONData (implements it.)
        :param o_cls: Class to check.
        :return: True if subclass; NotImplemented otherwise
        """
        if cls is JSONData:
            if any("as_json_data" in B.__dict__ for B in o_cls.__mro__):
                return True  # has to have "as_json_data"

        return NotImplemented


class BuildableJSONData(metaclass=abc.ABCMeta):
    """An ABC that describes a JSON Data class that can also build itself from pre-existing JSON data."""
    __slots__ = ()

    @abc.abstractmethod
    def as_json_data(self) -> typing.Union[str, int, float, dict, list, tuple]:
        """Exports this class as parsed json data (not as string, but as a valid json data type).

        Returns
        -------
        Union[:class:`str`, :class:`int`, :class:`float`, :class:`dict`, :class:`list`, :class:`tuple`, :class:`bool`]
        """
        raise NotImplementedError

    @classmethod
    @abc.abstractmethod
    def from_json_data(cls: type, data: typing.Union[str, int, float, dict, list, tuple]) -> "BuildableJSONData":
        """Builds a class instance using pre-existing PARSED JSON data. (Str, int, float, dict, list, tuple).

        Parameters
        ----------
        data : Union[:class:`str`, :class:`int`, :class:`float`, :class:`dict`, :class:`list`, :class:`tuple`, \
:class:`bool`]
            The parsed JSON data.

        Returns
        -------
        :class:`BuildableJSONData`
            The new class instance.

        """
        raise NotImplementedError

    @classmethod
    def __subclasshook__(cls, o_cls: type):
        """
        Checks if the given class is a subclass of BuildableJSONData (implements it.)
        :param o_cls: Class to check.
        :return: `True` if subclass; `NotImplemented` otherwise
        """
        if cls is BuildableJSONData:
            if JSONData.__subclasshook__(o_cls) is NotImplemented:  # must be valid JSON data.
                return NotImplemented

            if any("from_json_data" in B.__dict__ for B in o_cls.__mro__):
                return True  # has to have "as_json_data"

        return NotImplemented


class Itemable(metaclass=abc.ABCMeta):
    """An ABC that describes a class representing an item or DF type (i.e., can be converted to
    :class:`~py2df.classes.mc_types.Item`)."""
    __slots__ = ()

    @abc.abstractmethod
    def as_json_data(self):
        """Exports this class as parsed json data (not as string, but as a valid json data type).

        Returns
        -------
        Union[:class:`str`, :class:`int`, :class:`float`, :class:`dict`, :class:`list`, :class:`tuple`, :class:`bool`]
        """
        raise NotImplementedError

    @abc.abstractmethod
    def to_item(self) -> Item:
        """Converts this class to an equivalent Item.

        Returns
        -------
        :class:`~py2df.classes.mc_types.Item`
        """
        raise NotImplementedError

    @classmethod
    def __subclasshook__(cls, o_cls: type):
        """
        Checks if the given class is a subclass of JSONData (implements it.)
        :param o_cls: Class to check.
        :return: True if subclass; NotImplemented otherwise
        """
        if cls is Itemable:
            if JSONData.__subclasshook__(o_cls) is NotImplemented:  # must be valid JSON data.
                return NotImplemented

            if any("to_item" in B.__dict__ for B in o_cls.__mro__):
                return True  # has to have "as_json_data"

        return NotImplemented

# endregion:JSONData

# region:Misc


class Settable(metaclass=abc.ABCMeta):
    """An ABC that describes a class that can be ``.set()`` ."""
    @abc.abstractmethod
    def set(self) -> "Settable":
        """
        Set this class instance's attributes.

        Returns
        -------
        :class:`Settable`
            self to allow chaining.
        """
        raise NotImplementedError

    @classmethod
    def __subclasshook__(cls, o_cls: type):
        """
        Checks if the given class is a subclass of Settable (implements it.)
        :param o_cls: Class to check.
        :return: True if subclass; NotImplemented otherwise
        """
        if cls is Settable and any("set" in B.__dict__ for B in o_cls.__mro__):
            return True  # has to have "set" attr

        return NotImplemented


class FunctionHolder(metaclass=abc.ABCMeta):
    """
    An ABC that describes a class holding a function.

    Attributes
    ----------\u200b
        function : Callable
            The function that an instance holds.
    """
    __slots__ = ()
    function: typing.Callable

    @classmethod
    def __subclasshook__(cls, o_cls: type):
        """
        Checks if the given class is a subclass of Settable (implements it.)
        :param o_cls: Class to check.
        :return: True if subclass; NotImplemented otherwise
        """
        if cls is FunctionHolder and any("function" in B.__dict__ for B in o_cls.__mro__):
            return True  # has to have "function" attr

        return NotImplemented


_abc_classes = (
    Codeblock, EventBlock, BracketedBlock, CallableBlock, ActionBlock, JSONData, BuildableJSONData, Itemable, Settable,
    FunctionHolder
)
remove_u200b_from_doc(_abc_classes)

# endregion:Misc
