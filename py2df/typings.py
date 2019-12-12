import collections
import typing
from enum import Enum

from .classes.abc import Itemable
from .classes.mc_types import DFNumber, DFGameValue, DFText, DFLocation, DFPotion, Item, DFCustomSpawnEgg
from .classes.variable import DFVariable
from .utils import flatten


class ParamTypes:
    """Custom type annotations for parameters in humanized methods."""
    Numeric = typing.Union[int, float, DFNumber, DFGameValue, DFVariable]
    """Union[:class:`int`, :class:`float`, :class:`~.DFNumber`, :class:`~.DFGameValue`, :class:`~.DFVariable`] : The
possible types of a numeric parameter."""

    Textable = typing.Union[str, DFText, DFGameValue, DFVariable]
    """Union[:class:`str`, :class:`~.DFText`, :class:`~.DFGameValue`, :class:`~.DFVariable`] : The possible types of a \
text parameter."""

    Listable = typing.Union[DFGameValue, DFVariable]
    """Union[:class:`~.DFGameValue`, :class:`~.DFVariable`] : The possible types of a List (in DiamondFire) \
parameter."""

    Locatable = typing.Union[DFLocation, DFGameValue, DFVariable]
    """Union[:class:`~.DFLocation`, :class:`~.DFGameValue`, :class:`~.DFVariable`] : The possible types of a Location \
parameter."""

    Potionable = typing.Union[DFPotion, DFGameValue, DFVariable]
    """Union[:class:`~.DFPotion`, :class:`~.DFGameValue`, :class:`~.DFVariable`] : The possible types of a Potion \
parameter."""

    ItemParam = typing.Union[Itemable, Item, DFCustomSpawnEgg, DFGameValue, DFVariable]
    """Union[:class:`~.Itemable`, :class:`~.DFGameValue`, :class:`~.DFVariable`] : The possible types of an Item \
parameter."""

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


_P = typing.TypeVar("_P", Param, Numeric, Textable, Listable, Locatable, Potionable, ItemParam, DFVariable)


@typing.overload
def p_check(
    obj: Numeric, typeof: typing.Type[Numeric], arg_name: typing.Optional[str] = None, *, convert: bool = True
) -> Numeric: ...


@typing.overload
def p_check(
    obj: Textable, typeof: typing.Type[Textable], arg_name: typing.Optional[str] = None, *, convert: bool = True
) -> Textable: ...


@typing.overload
def p_check(
    obj: Listable, typeof: typing.Type[Listable], arg_name: typing.Optional[str] = None, *, convert: bool = True
) -> Listable: ...


@typing.overload
def p_check(
    obj: Locatable, typeof: typing.Type[Locatable], arg_name: typing.Optional[str] = None, *, convert: bool = True
) -> Locatable: ...


@typing.overload
def p_check(
    obj: Potionable, typeof: typing.Type[Potionable], arg_name: typing.Optional[str] = None, *, convert: bool = True
) -> Potionable: ...


@typing.overload
def p_check(
    obj: ItemParam, typeof: typing.Type[ItemParam], arg_name: typing.Optional[str] = None, *, convert: bool = True
) -> ItemParam: ...


@typing.overload
def p_check(
    obj: DFVariable, typeof: typing.Type[DFVariable], arg_name: typing.Optional[str] = None, *, convert: bool = True
) -> DFVariable: ...


@typing.overload
def p_check(
    obj: Param, typeof: typing.Type[Param], arg_name: typing.Optional[str] = None, *, convert: bool = True
) -> Param: ...


def p_check(obj: _P, typeof: typing.Type[_P], arg_name: typing.Optional[str] = None, *, convert: bool = True) -> _P:
    """Checks an object for being a valid param type, and raises a TypeError if that does not occur. For checking
    and returning a bool, see :func:`p_bool_check`.

    Parameters
    ----------
    obj : :attr:`ParamTypes.Param`
        The object to check.

    typeof : Type[:attr:`ParamTypes.Param`]
        The parameter type to check.

    convert : :class:`bool`, optional
        Whether or not the object should be converted from :class:`str`, :class:`int` or :class:`float` to,
        respectively, :class:`~.DFText` (for str) or :class:`~.DFNumber` (for int/float). Defaults to ``True``.

    arg_name : Optional[:class:`str`], optional
        The name of the argument, in order to have a more specific error. Defaults to ``None`` (no name given).

    Returns
    -------
    :attr:`ParamTypes.Param`
        The object, given there are no type incompatibilities.

    Raises
    ------
    :exc:`TypeError`
        If the object is found to not match the required param type.

    See Also
    --------
    :func:`p_bool_check`
    """
    class _Check:  # kinda hacky solution, but...
        _val: typeof

    p_typeof = typing.get_type_hints(_Check, globalns=None, localns=None)['_val']
    valid_types: typing.List[type] = flatten(
        [getattr(type_, "__args__", type_) for type_ in getattr(p_typeof, "__args__", [p_typeof])]
    )  # ^this allows Union[] to be specified as well, such that Union[Numeric, Locatable] works, for example.

    if not isinstance(obj, tuple(valid_types)):
        valid_names = ("Param", "Numeric", "Textable", "Locatable", "Potionable", "ItemParam")
        corresponding_values = (Param, Numeric, Textable, Locatable, Potionable, ItemParam)

        try:
            name = valid_names[corresponding_values.index(typeof)]
            msg = f"Object must be a valid {name} parameter."

        except (IndexError, ValueError):
            msg = f"Object must correspond to the appropriate parameter type."

        raise TypeError(msg + (f" (Arg '{arg_name}')" if arg_name else ""))

    if convert:
        return convert_numeric(convert_text(typing.cast(_P, obj)))

    return typing.cast(_P, obj)


@typing.overload
def p_bool_check(
    obj: Numeric, typeof: typing.Type[Numeric]
) -> Numeric: ...


@typing.overload
def p_bool_check(
    obj: Textable, typeof: typing.Type[Textable]
) -> Textable: ...


@typing.overload
def p_bool_check(
    obj: Listable, typeof: typing.Type[Listable]
) -> Listable: ...


@typing.overload
def p_bool_check(
    obj: Locatable, typeof: typing.Type[Locatable]
) -> Locatable: ...


@typing.overload
def p_bool_check(
    obj: Potionable, typeof: typing.Type[Potionable]
) -> Potionable: ...


@typing.overload
def p_bool_check(
    obj: ItemParam, typeof: typing.Type[ItemParam]
) -> ItemParam: ...


@typing.overload
def p_bool_check(
    obj: DFVariable, typeof: typing.Type[DFVariable]
) -> DFVariable: ...


@typing.overload
def p_bool_check(
    obj: Param, typeof: typing.Type[Param]
) -> Param: ...


def p_bool_check(obj: _P, typeof: typing.Type[_P]) -> bool:
    """Checks an object for being a valid param type, returning True if the type matches and False otherwise. For
    checking and raising an error, see :func:`p_check`.

    Parameters
    ----------
    obj : :attr:`ParamTypes.Param`
        The object to check.

    typeof : Type[:attr:`ParamTypes.Param`]
        The parameter type to check.

    Returns
    -------
    :attr:`ParamTypes.Param`
        The object, given there are no type incompatibilities.

    See Also
    --------
    :func:`p_check`
    """
    class _Check:  # kinda hacky solution, but...
        _val: typeof

    p_typeof = typing.get_type_hints(_Check, globalns=None, localns=None)['_val']

    valid_types: typing.List[type] = flatten(
        [getattr(type_, "__args__", type_) for type_ in getattr(p_typeof, "__args__", [p_typeof])]
    )

    return isinstance(obj, tuple(valid_types))
