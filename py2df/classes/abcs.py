"""
Generic base classes for the library.
"""
import abc
from enums import BlockType
import typing

from classes.utilities import Arguments


class Codeblock(metaclass=abc.ABCMeta):
    """
    An ABC that describes any codeblock - event, action etc.

    `Attributes`:
        block: Type of block - instance of enums.BlockType
        args: Arguments
        action: Specific action/description of it - e.g. event name

    """
    block: BlockType
    args: Arguments
    action: str
    __slots__ = ()

    @classmethod
    def __subclasshook__(cls, o_cls: type):
        """
        Checks if the given class is a subclass of Codeblock (implements it).
        :param o_cls: Class to check.
        :return: True if subclass; NotImplemented otherwise
        """

        if cls is Codeblock:
            attribs = ["block", "args", "action"]  # must have those attributes to be a codeblock.
            if any(attr in B.__dict__ for B in o_cls.__mro__ for attr in attribs):
                return True
        return NotImplemented


class Action(metaclass=abc.ABCMeta):
    """
    An ABC that describes any action - Player Action, Game Action or Entity Action. Must implement Codeblock.
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

        return NotImplemented


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

        if cls is Action:
            if Codeblock.__subclasshook__(o_cls) is NotImplemented:
                return NotImplemented

            try:  # TODO: Entity event?
                if BlockType(getattr(o_cls, "block")) == BlockType.EVENT:
                    return True
            except ValueError:  # not a valid block type
                return NotImplemented  # not an Action

        return NotImplemented
