import collections
import typing
from enum import Enum

from .classes import DFNumber, DFGameValue, DFText, DFLocation, DFPotion, Itemable, Item, DFCustomSpawnEgg


class ParamTypes:
    """Custom type annotations for parameters in humanized methods."""
    Numeric = typing.Union[int, float, DFNumber, DFGameValue]  # TODO: var
    """Union[:class:`int`, :class:`float`, :class:`~.DFNumber`, :class:`~.DFGameValue`] : The possible types of a \
numeric parameter."""

    Textable = typing.Union[str, DFText, DFGameValue]
    """Union[:class:`str`, :class:`~.DFText`, :class:`~.DFGameValue`] : The possible types of a text parameter."""

    Listable = typing.Union[DFGameValue]
    """Union[:class:`~.DFGameValue`] : The possible types of a List (in DiamondFire) parameter."""

    Locatable = typing.Union[DFLocation, DFGameValue]
    """Union[:class:`~.DFLocation`, :class:`~.DFGameValue`] : The possible types of a Location parameter."""

    Potionable = typing.Union[DFPotion, DFGameValue]
    """Union[:class:`~.DFPotion`, :class:`~.DFGameValue`] : The possible types of a Potion parameter."""

    ItemParam = typing.Union[Itemable, Item, DFCustomSpawnEgg, DFGameValue]
    """Union[:class:`~.Itemable`, :class:`~.DFGameValue`] : The possible types of an Item parameter."""

    # TODO: VarParam

    Param = typing.Union[
        "ParamTypes.Numeric", "ParamTypes.Textable", "ParamTypes.Listable", "ParamTypes.Potionable",
        "ParamTypes.ItemParam"
    ]
    """Union[:attr:`Numeric`, :attr:`Textable`, :attr:`Listable`, :attr:`Potionable`, :attr:`ItemParam`] : All the \
possible parameter types."""


Numeric = ParamTypes.Numeric

Textable = ParamTypes.Textable

Listable = ParamTypes.Listable

Locatable = ParamTypes.Locatable

Potionable = ParamTypes.Potionable

ItemParam = ParamTypes.ItemParam

Param = ParamTypes.Param


def convert_numeric(param: Numeric) -> Numeric:
    """Converts ints and floats from a Numeric parameter to the appropriate DFNumber, while leaving
    Game Values and Variables untouched.

    Parameters
    ----------
    param : :attr:`~.Numeric`
        The numeric parameter to convert.

    Returns
    -------
    :attr:`~.Numeric`
        Resulting conversion, or the parameter itself if nothing required change.
    """
    if isinstance(param, (int, float)):
        return DFNumber(param)

    return param


def convert_text(param: Textable) -> Textable:
    """Converts strs from a Textable parameter to the appropriate DFText, while leaving
    Game Values and Variables untouched.

    Parameters
    ----------
    param : :attr:`~.Textable`
        The text parameter to convert.

    Returns
    -------
    :attr:`~.Textable`
        Resulting conversion, or the parameter itself if nothing required change.
    """
    if isinstance(param, (str, collections.UserString)):
        return DFText(str(param))

    return param
