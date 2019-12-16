import collections
import typing
from enum import Enum

from .enums import GVAL_TEXTABLE, GVAL_NUMERIC, GVAL_LOCATABLE, GVAL_LISTABLE, GVAL_ITEM
from .classes.abc import Itemable
from .classes.mc_types import DFNumber, DFText, DFLocation, DFPotion, Item, DFCustomSpawnEgg, DFParticle
from .classes.variable import DFVariable, DFGameValue
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

    Potionable = typing.Union[DFPotion, DFVariable]  # there is no Game Value representing a potion effect.
    """Union[:class:`~.DFPotion`, :class:`~.DFVariable`] : The possible types of a Potion Effect parameter."""

    ParticleParam = typing.Union[DFParticle, DFVariable]  # no particle game value
    """Union[:class:`~.DFParticle`, :class:`~.DFVariable`] : The possible types of a Particle parameter."""

    ItemParam = typing.Union[Itemable, Item, DFCustomSpawnEgg, DFGameValue, DFVariable]
    """Union[:class:`~.Itemable`, :class:`~.DFGameValue`, :class:`~.DFVariable`] : The possible types of an Item \
parameter."""

    Param = typing.Union[
        "ParamTypes.Numeric", "ParamTypes.Textable", "ParamTypes.Listable", "ParamTypes.Potionable",
        "ParamTypes.ParticleParam", "ParamTypes.ItemParam"
    ]
    """Union[:attr:`Numeric`, :attr:`Textable`, :attr:`Listable`, :attr:`Potionable`, :attr:`ItemParam`] : All the \
possible parameter types."""


Numeric = ParamTypes.Numeric

Textable = ParamTypes.Textable

Listable = ParamTypes.Listable

Locatable = ParamTypes.Locatable

Potionable = ParamTypes.Potionable

ParticleParam = ParamTypes.ParticleParam

ItemParam = ParamTypes.ItemParam

Param = ParamTypes.Param

GVAL_TYPES = {
    Numeric: GVAL_NUMERIC,
    Textable: GVAL_TEXTABLE,
    Listable: GVAL_LISTABLE,
    Locatable: GVAL_LOCATABLE,
    ItemParam: GVAL_ITEM,
    Item: GVAL_ITEM,

    # a few common Unions
    typing.Union[Numeric, Locatable]: GVAL_NUMERIC + GVAL_LOCATABLE
}


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

    valid_names = (
        "Param", "Numeric", "Textable", "Locatable", "Potionable", "ItemParam",
        "Union[Numeric, Locatable]", "Union[Textable, ItemParam]"
    )
    corresponding_values = (
        Param, Numeric, Textable, Locatable, Potionable, ItemParam,
        typing.Union[Numeric, Locatable], typing.Union[Textable, ItemParam]
    )
    if not isinstance(obj, tuple(valid_types)):

        try:
            corresp_class_ind = corresponding_values.index(typeof)
            name = valid_names[corresp_class_ind]
            msg = f"Object must be a valid {repr(name)} parameter, not {repr(str(type(obj)))}."

        except (IndexError, ValueError):
            msg = f"Object must correspond to the appropriate parameter type, and not be a {repr(str(type(obj)))}."

        raise TypeError("{0}{1}".format(
            msg,
            f" (Arg '{arg_name}')" if arg_name else ""
        ))

    if GVAL_TYPES.get(typeof) and isinstance(obj, DFGameValue) and obj not in GVAL_TYPES[typeof]:
        try:
            corresp_class_ind = corresponding_values.index(typeof)
            name = valid_names[corresp_class_ind]
            msg = f"The DFGameValue type specified does not evaluate to a valid {repr(name)} parameter. (Check \
documentation to see valid 'GameValueType' attrs for this parameter type.)"

        except (IndexError, ValueError):
            msg = f"The DFGameValue type specified does not evaluate to a valid parameter of the required type. \
(Check documentation to see valid 'GameValueType' attrs for this parameter type.)"

        raise TypeError("{0}{1}".format(
            msg,
            f" (Arg '{arg_name}')" if arg_name else ""
        ))

    if convert:
        return convert_numeric(convert_text(typing.cast(_P, obj)))

    return typing.cast(_P, obj)


def p_bool_check(obj: _P, typeof: typing.Type[_P], gameval_check: bool = True, error_on_gameval: bool = False) -> bool:
    """Checks an object for being a valid param type, returning True if the type matches and False otherwise. For
    checking and raising an error, see :func:`p_check`.

    Parameters
    ----------
    obj : :attr:`ParamTypes.Param`
        The object to check.

    typeof : Type[:attr:`ParamTypes.Param`]
        The parameter type to check.

    gameval_check : :class:`bool`, optional
        If any DFGameValue instances specified should be checked to ensure they have the same Return Type as the
        specified parameter type. Defaults to ``True``.

    error_on_gameval : :class:`bool`, optional
        If DFGameValue instances found to not correspond to the given type should raise a TypeError instead of
        causing the function to return ``False``. Defaults to ``False``.

    Returns
    -------
    :class:`bool`
        If the object matches the given type, then this is ``True``. Otherwise, ``False``.

    Raises
    ------
    :exc:`TypeError`
        If ``error_on_gameval`` is set to ``True`` and a DFGameValue instance of incompatible type is given.

    See Also
    --------
    :func:`p_check`
    """
    class _Check:  # kinda hacky solution, but...
        _val: typeof

    p_typeof = typing.get_type_hints(_Check, globalns=None, localns=None)['_val']  # resolve forward refs

    valid_types: typing.List[type] = flatten(
        [getattr(type_, "__args__", type_) for type_ in getattr(p_typeof, "__args__", [p_typeof])]
    )

    if not isinstance(obj, tuple(valid_types)):
        return False

    if gameval_check and GVAL_TYPES.get(typeof) and isinstance(obj, DFGameValue) and obj not in GVAL_TYPES[typeof]:
        if error_on_gameval:
            try:
                valid_names = (
                    "Param", "Numeric", "Textable", "Locatable", "Potionable", "ItemParam",
                    "Union[Numeric, Locatable]", "Union[Textable, ItemParam]"
                )
                corresponding_values = (
                    Param, Numeric, Textable, Locatable, Potionable, ItemParam,
                    typing.Union[Numeric, Locatable], typing.Union[Textable, ItemParam]
                )
                corresp_class_ind = corresponding_values.index(typeof)
                name = valid_names[corresp_class_ind]
                msg = f"The DFGameValue type specified does not evaluate to a valid {repr(name)} parameter. (Check \
documentation to see valid 'GameValueType' attrs for this parameter type.)"

            except (IndexError, ValueError):
                msg = f"The DFGameValue type specified does not evaluate to a valid parameter of the required type. \
(Check documentation to see valid 'GameValueType' attrs for this parameter type.)"

            raise TypeError(msg)

        else:
            return False

    return True
