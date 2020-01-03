import collections
import typing
from enum import Enum

from .enums import GVAL_TEXTABLE, GVAL_NUMERIC, GVAL_LOCATABLE, GVAL_LISTABLE, GVAL_ITEM, ParticleType, SoundType, \
    Material
from .classes.abc import Itemable
from .classes.mc_types import DFNumber, DFText, DFLocation, DFPotion, Item, DFCustomSpawnEgg, DFParticle, DFSound
from .classes.variable import (
    DFVariable, DFGameValue, NumberVar, TextVar, ListVar, LocationVar, PotionVar, ParticleVar,
    SoundVar, ItemVar
)
from .utils import flatten


class ParamTypes:
    """Custom type annotations for parameters in humanized methods."""
    Numeric = typing.Union[int, float, DFNumber, DFGameValue, DFVariable, NumberVar]
    """Union[:class:`int`, :class:`float`, :class:`~.DFNumber`, :class:`~.DFGameValue`, :class:`~.DFVariable`, \
:class:`~.NumberVar`] : The possible types of a numeric parameter."""

    Textable = typing.Union[str, DFText, DFGameValue, DFVariable, TextVar]
    """Union[:class:`str`, :class:`~.DFText`, :class:`~.DFGameValue`, :class:`~.DFVariable`, :class:`~.TextVar`] : The \
possible types of a text parameter."""

    Listable = typing.Union[DFGameValue, DFVariable, ListVar]
    """Union[:class:`~.DFGameValue`, :class:`~.DFVariable`, :class:`~.ListVar`] : The possible types of a List (in \
DiamondFire) parameter."""

    Locatable = typing.Union[DFLocation, DFGameValue, DFVariable, LocationVar]
    """Union[:class:`~.DFLocation`, :class:`~.DFGameValue`, :class:`~.DFVariable`, :class:`~.LocationVar`] : The \
possible types of a Location parameter."""

    Potionable = typing.Union[DFPotion, DFVariable, PotionVar]  # there is no Game Value representing a potion effect.
    """Union[:class:`~.DFPotion`, :class:`~.DFVariable`, :class:`~.PotionVar`] : The possible types of a Potion Effect \
parameter."""

    ParticleParam = typing.Union[DFParticle, ParticleType, DFVariable, ParticleVar]  # no particle game value
    """Union[:class:`~.DFParticle`, :class:`~.ParticleType`, :class:`~.DFVariable`, :class:`~.ParticleVar`] : The \
possible types of a Particle parameter."""

    SoundParam = typing.Union[DFSound, SoundType, DFVariable, SoundVar]  # no sound game value
    """Union[:class:`~.DFSound`, :class:`~.SoundType`, :class:`~.DFVariable`, :class:`~.SoundVar`] : The possible \
types of a Sound param."""

    ItemParam = typing.Union[Item, Material, DFGameValue, DFVariable, ItemVar]
    """Union[:class:`~.Item`, :class:`~.Material`, :class:`~.DFGameValue`, :class:`~.DFVariable`, :class:`~.ItemVar`] \
: The possible types of an Item parameter."""

    SpawnEggable = typing.Union[DFCustomSpawnEgg, ItemParam]
    """Union[:class:`~.DFCustomSpawnEgg`, :attr:`ItemParam`] : The possible types of a Spawn Egg parameter."""

    Param = typing.Union[
        "ParamTypes.Numeric", "ParamTypes.Textable", "ParamTypes.Listable", "ParamTypes.Potionable",
        "ParamTypes.ParticleParam", "ParamTypes.SoundParam", "ParamTypes.ItemParam", "ParamTypes.SpawnEggable"
    ]
    """Union[:attr:`Numeric`, :attr:`Textable`, :attr:`Listable`, :attr:`Potionable`, :attr:`ParticleParam`, \
:attr:`SoundParam`, :attr:`ItemParam`, :attr:`SpawnEggable`] : All the possible parameter types."""


Numeric = ParamTypes.Numeric

Textable = ParamTypes.Textable

Listable = ParamTypes.Listable

Locatable = ParamTypes.Locatable

Potionable = ParamTypes.Potionable

ParticleParam = ParamTypes.ParticleParam

SoundParam = ParamTypes.SoundParam

ItemParam = ParamTypes.ItemParam

SpawnEggable = ParamTypes.SpawnEggable

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

    Examples
    --------
    >>> convert_numeric(5)
    <DFNumber value=5.0>

    >>> convert_numeric(6.54)
    <DFNumber value=6.54>
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

    Examples
    --------
    >>> convert_text("test")
    <DFText data='test'>
    """
    if isinstance(param, (str, collections.UserString)):
        return DFText(str(param))

    return param


def convert_particle(param: ParticleParam) -> ParticleParam:
    """Converts :class:`~.ParticleType` from a ParticleParam parameter to the appropriate DFParticle, while leaving
    Game Values and Variables untouched.

    Parameters
    ----------
    param : :attr:`~.ParticleParam`
        The particle parameter to convert.

    Returns
    -------
    :attr:`~.ParticleParam`
        Resulting conversion, or the parameter itself if nothing required change.

    Examples
    --------
    >>> convert_particle(ParticleType.ANGRY_VILLAGER)
    <DFParticle particle_type='Angry Villager'>
    """
    if isinstance(param, ParticleType):
        return DFParticle(param)

    return param


def convert_sound(param: SoundParam) -> SoundParam:
    """Converts :class:`~.SoundType` from a SoundParam parameter to the appropriate DFSound, while leaving
    Game Values and Variables untouched.

    Parameters
    ----------
    param : :attr:`~.SoundParam`
        The sound parameter to convert.

    Returns
    -------
    :attr:`~.SoundParam`
        Resulting conversion, or the parameter itself if nothing required change.
    """
    if isinstance(param, SoundType):
        return DFSound(param)

    return param


def convert_material(param: typing.Union[Param, Material]) -> Param:
    """Converts :class:`~.Material` into :class:`~.Item`.

    Parameters
    ----------
    param : Union[:attr:`~.Param`, :class:`~.Material`]
        The parameter/material to convert.

    Returns
    -------
    :attr:`~.Param`
        The generated item, or the param specified.

    Examples
    --------
    >>> convert_material(Material.DIAMOND_SWORD)
    <Item minecraft:diamond_sword x 1>
    """
    if isinstance(param, Material):
        return Item(param)

    return param


def convert_all(param: Param) -> Param:
    """Converts anything from a Param parameter to the appropriate DF(something) class, while leaving
    Game Values and Variables untouched. (Calls all other converting methods)

    Parameters
    ----------
    param : :attr:`~.Param`
        The parameter to convert.

    Returns
    -------
    :attr:`~.Param`
        Resulting conversion, or the parameter itself if nothing required change.

    See Also
    --------
    :meth:`convert_particle`, :meth:`convert_sound`, :meth:`convert_numeric`, :meth:`convert_text`, \
:meth:`convert_material`
    """
    return convert_particle(convert_sound(convert_numeric(convert_text(convert_material(param)))))


_P = typing.TypeVar(
    "_P",
    Param, Numeric, Textable, Listable, Locatable, Potionable, ItemParam, DFVariable, SpawnEggable
)
_A = typing.TypeVar("_A",
    Param, Numeric, Textable, Listable, Locatable, Potionable, ItemParam, DFVariable, SpawnEggable
)
_B = typing.TypeVar("_B",
    Param, Numeric, Textable, Listable, Locatable, Potionable, ItemParam, DFVariable, SpawnEggable
)


@typing.overload
def p_check(
    obj: typing.Optional[_P], typeof: typing.Type[typing.Optional[_P]], arg_name: typing.Optional[str] = None,
    *, convert: bool = True
) -> _P: ...

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
    obj: ParticleParam, typeof: typing.Type[ParticleParam], arg_name: typing.Optional[str] = None,
    *, convert: bool = True
) -> ParticleParam: ...


@typing.overload
def p_check(
    obj: SoundParam, typeof: typing.Type[SoundParam], arg_name: typing.Optional[str] = None, *, convert: bool = True
) -> SoundParam: ...


@typing.overload
def p_check(
    obj: DFVariable, typeof: typing.Type[DFVariable], arg_name: typing.Optional[str] = None, *, convert: bool = True
) -> DFVariable: ...


@typing.overload
def p_check(
    obj: SpawnEggable, typeof: typing.Type[SpawnEggable], arg_name: typing.Optional[str] = None, *, convert: bool = True
) -> DFVariable: ...


@typing.overload
def p_check(
    obj: Param, typeof: typing.Type[Param], arg_name: typing.Optional[str] = None, *, convert: bool = True
) -> Param: ...


def p_check(
    obj: _P, typeof: typing.Type[_P], arg_name: typing.Optional[str] = None, *, convert: bool = True
) -> _P:
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
        "Param", "Numeric", "Textable", "Locatable", "Potionable", "ItemParam", "ParticleParam", "SoundParam",
        "SpawnEggable",
        "Union[Numeric, Locatable]", "Union[Textable, ItemParam]", "Union[Locatable, Textable]"
    )
    corresponding_values = (
        Param, Numeric, Textable, Locatable, Potionable, ItemParam, ParticleParam, SoundParam, SpawnEggable,
        typing.Union[Numeric, Locatable], typing.Union[Textable, ItemParam], typing.Union[Locatable, Textable]
    )
    if not isinstance(obj, tuple(filter(lambda t: t is not None, valid_types))):  # remove 'None'

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
        obj = convert_all(typing.cast(_P, obj))

    if typeof == SpawnEggable and isinstance(obj, Item) and "spawn_egg" not in obj.material.value:
        raise TypeError(
            f"Object must be a valid spawn egg item, not a(n) '{obj.material.value}'."
            + (f" (Arg '{arg_name}')" if arg_name else "")
        )

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

    Examples
    --------
    >>> p_bool_check(5, Numeric)
    True

    >>> p_bool_check(5, Locatable)
    False
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
                    "Param", "Numeric", "Textable", "Locatable", "Potionable", "ItemParam", "ParticleParam",
                    "SoundParam", "SpawnEggable",
                    "Union[Numeric, Locatable]", "Union[Textable, ItemParam]"
                )
                corresponding_values = (
                    Param, Numeric, Textable, Locatable, Potionable, ItemParam, ParticleParam, SoundParam,
                    SpawnEggable,
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
