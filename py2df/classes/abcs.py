"""
Generic base classes for the library.
"""
import abc
from enums import BlockType
import typing

from classes.mc_types import Item


class Codeblock(metaclass=abc.ABCMeta):
    """
    An ABC that describes any codeblock - event, action etc.

    `Attributes`
    -------------
        `block:` Type of block - instance of enums.BlockType

        `args`: Arguments

        `action`: Enum CodeblockActionType - Specific action/description of it - e.g. event name

        `length`: The space, in Minecraft blocks, that this codeblock occupies. (Most are 2, but some, like IFs, are 1)

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
            attribs = ["block", "args", "action", "length"]  # must have those attributes to be a codeblock.
            if all(any(attr in B.__dict__ for B in o_cls.__mro__) for attr in attribs):
                return True
        return NotImplemented


class Action(metaclass=abc.ABCMeta):
    """
    An ABC that describes any action - Player Action, Game Action, Entity Action or Control. Must implement Codeblock.
    """
    __slots__ = ()

    @classmethod
    def __subclasshook__(cls, o_cls: type):
        """
        Checks if the given class is a subclass of Action (implements it).
        :param o_cls: Class to check.
        :return: True if subclass; NotImplemented otherwise
        """

        if cls is Action:
            if Codeblock.__subclasshook__(o_cls) is NotImplemented:  # must be a Codeblock
                return NotImplemented

            try:  # TODO: Entity action
                if BlockType(getattr(o_cls, "block")) in (BlockType.PLAYER_ACTION, BlockType.GAME_ACTION):
                    return True  # must be one of BlockType.PLAYER_ACTION or BlockType.GAME_ACTION
            except ValueError:  # not a valid block type
                return NotImplemented  # not an Action

        return NotImplemented  # #


class Event(metaclass=abc.ABCMeta):
    """
    An ABC that describes any event - Player Event or Entity Event. Must implement Codeblock.
    """
    __slots__ = ()

    @classmethod
    def __subclasshook__(cls, o_cls: type):
        """
        Checks if the given class is a subclass of Event (implements it).
        :param o_cls: Class to check.
        :return: True if subclass; NotImplemented otherwise
        """

        if cls is Event:
            if Codeblock.__subclasshook__(o_cls) is NotImplemented:
                return NotImplemented

            try:  # TODO: Entity event?
                if BlockType(getattr(o_cls, "block")) == BlockType.EVENT:  # must be event.
                    return True
            except ValueError:  # not a valid block type
                return NotImplemented  # not an Action

        return NotImplemented


class BracketedBlock(metaclass=abc.ABCMeta):
    """
    An ABC that describes any codeblock with brackets. Can be used on a `with` construct. Must implement CodeBlock.
    """
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
        """
        Places the OPEN bracket. Can have two types: NORM and REPEAT
        :return:
        """
        raise NotImplementedError

    @abc.abstractmethod
    def __exit__(self):
        """
        Places the CLOSE bracket. Can have two types: NORM and REPEAT
        :return:
        """
        raise NotImplementedError


# TODO: Customizable start block (Functions and processes)

class JSONData(metaclass=abc.ABCMeta):
    """
    An ABC that describes a class implementing `.as_json_data()'.
    """
    __slots__ = ()

    @abc.abstractmethod
    def as_json_data(self) -> typing.Union[str, int, float, dict, list, tuple]:
        """
        Exports this class as raw json data (not as string, but as a valid json data type).
        :return: One of str, int, float, dict, list or tuple (which is converted to list).
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
    """
    An ABC that describes a JSON Data class that can also build itself from pre-existing JSON data.
    """
    __slots__ = ()

    @abc.abstractmethod
    def as_json_data(self) -> typing.Union[str, int, float, dict, list, tuple]:
        """
        Exports this class as parsed json data (not as string, but as a valid json data type).
        :return: One of str, int, float, dict, list or tuple (which is converted to list).
        """
        raise NotImplementedError

    @classmethod
    @abc.abstractmethod
    def from_json_data(cls: type, data: typing.Union[str, int, float, dict, list, tuple]):
        """
        Builds a class instance using pre-existing PARSED JSON data. (Str, int, float, dict, list, tuple).
        :param data: The parsed JSON data.
        :return: The new class instance.
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
    """
    An ABC that describes a class representing an item or DF type.
    """
    __slots__ = ()

    @abc.abstractmethod
    def as_json_data(self):
        """
        Exports this class as parsed json data (not as string, but as a valid json data type).
        :return: One of str, int, float, dict, list or tuple (which is converted to list).
        """
        raise NotImplementedError

    @abc.abstractmethod
    def to_item(self) -> Item:
        """
        Converts this class to an equivalent Item.
        :return: Item instance.
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
