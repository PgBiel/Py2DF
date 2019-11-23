"""
Generic base classes for the library.
"""
import abc
import enums
import typing


class Codeblock(metaclass=abc.ABCMeta):
    """
    An ABC that describes any codeblock - event, action etc.

    `Attributes`:
        block: Type of block - instance of enums.BlockType
        args: Arguments
        action: Specific action/description of it - e.g. event name

    """
    block: enums.BlockType

    @classmethod
    def __subclasshook__(cls, o_cls: type):
        if cls is Codeblock:
            attribs = ["block", "args", "action"]
            if any(attr in B.__dict__ for B in o_cls.__mro__ for attr in attribs):
                return True
        return NotImplemented


class Action(metaclass=abc.ABCMeta):
    """
    An ABC that describes any action - Player Action, Game Action or Entity Action. Must implement Codeblock.
    """
    pass

#
