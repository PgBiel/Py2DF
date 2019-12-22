import json
import typing
import collections
import nbtlib as nbt
from array import array

if typing.TYPE_CHECKING:  # avoid cyclic import
    from .typings import Numeric

Docable = typing.Union[typing.Callable, type]
IterOrSingleDocable = typing.Union[Docable, typing.Iterable[Docable]]


def remove_u200b_from_doc(obj: IterOrSingleDocable, *other_objs: IterOrSingleDocable) -> None:
    """
    Remove ``\\u200b`` from a class/method's docstring.

    Parameters
    ----------
    obj : Union[Union[Callable, :class:`type`], Iterable[Union[Callable, :class:`type`]]]
        Can be either a class/method or an iterable of classes/methods from whose documentation ``\\u200b`` will be
        removed.

    other_objs: Union[Union[Callable, :class:`type`], Iterable[Union[Callable, :class:`type`]]]
        Any other objects (or iterables thereof) to follow the same procedure.

    Returns
    -------
    None
        None
    """
    if isinstance(obj, collections.Iterable) and not isinstance(obj, type):
        for clz in obj:
            remove_u200b_from_doc(clz)
    else:
        the_doc = obj.__doc__
        if "\u200b" in the_doc:
            obj.__doc__ = the_doc.replace("\u200b", "")

    for o in other_objs:
        remove_u200b_from_doc(o)


class _DoNotFlatten:
    def __init__(self, val):
        self.val = val


def flatten(
    *args: typing.Any, allow_iterables: typing.Iterable[typing.Type[typing.Iterable]] = tuple(),
    except_iterables: typing.Iterable[typing.Type[typing.Iterable]] = tuple(), max_depth: typing.Optional[int] = None,
    keep_iterables: typing.Iterable[typing.Type[typing.Iterable]] = tuple(), curr_depth: int = 0
) -> list:
    """
    Flatten a list or iterable of arbitrary length.

        >>> from py2df.utils import flatten
        >>> flatten(1, 2, ['b', 'a' , ['c', 'd']], 3)
        [1, 2, 'b', 'a', 'c', 'd', 3]

    Parameters
    ----------
    args : Any
        Items and lists to be combined into a single list.

    allow_iterables : Iterable[:class:`type`], optional
        An iterable (list, etc.) which specifies the types (classes) of Iterables to flatten,
        besides :class:`list` and :class:`tuple` (which are always checked by default) - they will be
        checked with an ``isinstance()`` call. Defaults to ``tuple()`` (empty tuple - none).

    except_iterables : Iterable[:class:`type`], optional
        An iterable (list, etc.) which specifies the types (classes) of Iterables to NOT be flattened; i.e.,
        all will be flattened except the given ones. This could have serious side-effects, so choose wisely.
        Defaults to ``tuple()`` (empty tuple - none). If using this, **it is recommended to set `max_depth` ** .
        **This parameter overrides `allow_iterables`. **

    max_depth : Optional[int], optional
        An integer that represents the maximum depth until which the list is flattened, or None for no limit.
        Defaults to None.

    keep_iterables : Iterable[:class:`type`], optional
        List of iterable types to keep; i.e., flatten them, but keep them there regardless (one position before). E.g.::

            >>> flatten(1, (1, 2), keep_iterables=[tuple])
            [1, (1, 2), 1, 2]

    Returns
    -------
    :class:`list`
        Resulting list.

    Warnings
    --------
    Pick the iterables in the ``allow_iterables`` list wisely, because **any instance of it will be flattened**. This
    can produce unexpected results when accepting, for example, :class:`str` as a valid Iterable to be flattened.
    This warning also applies (even more so) to ``except_iterables``: If it is specified, make sure to set ``max_depth``
    in order to avoid further problems.

    Notes
    -----
    Credits to NLTK authors for this function's original code.
    """

    x = []
    if except_iterables and allow_iterables:
        allow_iterables = tuple()

    for el in args:
        is_iterable = isinstance(el, collections.Iterable)

        do_keep = keep_iterables and isinstance(el, tuple(keep_iterables)) and curr_depth == 0  # prevent dupes

        if do_keep:  # if we should keep it in the list
            x.append(el)

        if (
            (is_iterable and except_iterables and isinstance(el, tuple(except_iterables)))  # if iterable in "except",
            or (not except_iterables and not isinstance(el, (list, tuple, *(allow_iterables or []))))  # !"accept"...
        ):
            el = [el]  # make it an one-element iterable for the for loop to work.

        for item in el:
            if do_keep and item == el:
                continue

            item_is_iter = isinstance(item, collections.Iterable)
            if (  # if this is a valid iterable according to the given parameters, then flatten it
                (curr_depth < max_depth if max_depth else True)  # do not flatten any further than max depth.
                and (  # if this is a valid iterable (not in "except" or in "accept"), flatten it!
                    (item_is_iter and except_iterables and not isinstance(item, tuple(except_iterables)))
                    or (not except_iterables and isinstance(item, (list, tuple, *(allow_iterables or tuple()))))
                )
            ):
                if keep_iterables and isinstance(item, tuple(keep_iterables)):
                    x.append(item)

                x.extend(
                    flatten(  # flatten
                        item,
                        allow_iterables=allow_iterables, except_iterables=except_iterables,
                        max_depth=max_depth, curr_depth=curr_depth + 1, keep_iterables=keep_iterables
                    )
                )
            else:  # don't flatten
                x.append(item)

    # if keep_iterables and curr_depth == 0 and False:
    #     # print(f"bruh moment {curr_depth=} {len(list(filter(lambda t: type(t) == _DoNotFlatten, x)))}")
    #     return [el.val if type(el) == _DoNotFlatten else el for el in x]

    return x


AnyNumber = typing.Union[int, float]


@typing.overload
def clamp(num: int, min_: int, max_: int) -> int: ...


@typing.overload
def clamp(num: float, min_: float, max_: float) -> float: ...


@typing.overload
def clamp(num: AnyNumber, min_: AnyNumber, max_: AnyNumber) -> AnyNumber: ...


def clamp(num: AnyNumber, min_: AnyNumber, max_: AnyNumber) -> AnyNumber:
    """Clamps a number (int, float) between two bounds, inclusively.

    Parameters
    ----------
    num : Union[:class:`int`, :class:`float`]
        Number to be clamped.

    min_ : Union[:class:`int`, :class:`float`]
        Lower bound; the minimum value that this number can be, and is returned if ``distance <= min_`` holds.

    max_ : Union[:class:`int`, :class:`float`]
        Upper bound; the maximum value that this number can be, and is returned if ``distance => max_`` holds.

    Returns
    -------
    Union[:class:`int`, :class:`float`]
        The clamped number.
    """
    return min(max(min_, num), max_)


T = typing.TypeVar("T")


def all_attr_eq(a: T, b: T) -> bool:
    """
    Checks if two objects are equal by comparing their types and each of their attributes.

    Parameters
    ----------
    a : Any
        An object to compare.

    b : Any
        Another object to compare equality.

    Returns
    -------
    :class:`bool`
        Whether or not the objects are equal (if their types and attributes are all equal).
    """
    return type(a) == type(b) and all(
        getattr(a, attr) == getattr(b, attr) for attr in getattr(
            a.__class__, "__slots__", a.__dict__
        ) or a.__class__.__dict__
    )


K = typing.TypeVar("K")
V = typing.TypeVar("V")


def select_dict(
        obj: typing.Dict[K, V], *keys: typing.Union[str, typing.Iterable[str]],
        ignore_missing: bool = False
) -> typing.Dict[K, V]:
    """
    Selects certain keys from a dict.

    Parameters
    ----------
    obj : :class:`dict`
        The dictionary from which to select keys.

    keys : Union[:class:`str`, Iterable[:class:`str`]]
        Key, keys or iterables of keys to select.

    ignore_missing : :class:`bool`, optional
        Whether or not to ignore missing attributes in the dictionary (i.e., accept trying to select a key that is not
        there). This defaults to False. (If False, it will raise a KeyError.)

    Returns
    -------
    :class:`dict`
        A dictionary with only the given keys.
    """
    flattened_keys = flatten(keys, except_iterables=(str,), max_depth=2)

    def select_key(k: K) -> typing.Tuple[K, V]:
        return (k, obj[k])

    if ignore_missing:
        def filter_key(k: K) -> bool:
            return k in obj

        gen = map(select_key, filter(filter_key, flattened_keys))
    else:
        gen = map(select_key, flattened_keys)

    return {k: v for k, v in gen}


@typing.overload  # String => str
def nbt_to_python(obj: nbt.String, convert_items: bool = True) -> str: ...


@typing.overload  # Int/Long/Short/Byte => int
def nbt_to_python(obj: typing.Union[nbt.Int, nbt.Long, nbt.Short, nbt.Byte], convert_items: bool = True) -> int: ...


@typing.overload  # Float/Double => float
def nbt_to_python(obj: typing.Union[nbt.Float, nbt.Double], convert_items: bool = True) -> float: ...


@typing.overload  # Compound => dict
def nbt_to_python(obj: nbt.Compound, convert_items: bool = True) -> dict: ...


ItemType = typing.TypeVar("ItemType")


if hasattr(typing, "Literal"):  # py 3.8
    TrueLiteral: "typing.Literal[True]" = typing.Literal[True]
    FalseLiteral: "typing.Literal[False]" = typing.Literal[False]
else:  # support for py <3.8  - just accept any bool
    TrueLiteral = FalseLiteral = typing.cast(typing.Any, bool)  # type: typing.Type[bool]


@typing.overload  # convert_items is False; List
def nbt_to_python(obj: nbt.List[ItemType], convert_items: FalseLiteral) -> typing.List[ItemType]: ...


@typing.overload  # convert_items is True; List
def nbt_to_python(
    obj: nbt.List, convert_items: TrueLiteral = True
) -> typing.List[typing.Union[str, dict, list, array, int, float]]: ...


@typing.overload  # arrays
def nbt_to_python(
    obj: typing.Union[nbt.ByteArray, nbt.LongArray, nbt.IntArray], convert_items: bool = True
) -> array: ...


@typing.overload  # general case
def nbt_to_python(
    obj: nbt.tag.Base, convert_items: bool = True
) -> typing.Union[str, dict, list, array, int, float]: ...


def nbt_to_python(obj: nbt.tag.Base, convert_items: bool = True) -> typing.Union[str, dict, list, array, int, float]:
    """
    Converts a NBT object (instance of :class:`nbtlib.tag.Base`, i.e., any NBT-related class) into its Python raw
    type equivalent. Example::

        >>> from py2df.utils import nbt_to_python
        >>> import nbtlib
        >>> converted = nbt_to_python(nbtlib.Byte(5))
        >>> converted
        5
        >>> type(converted)
        <class 'int'>

    The full relation is:
    
    +-------------------------+----------------------------------------------------------------------------------------+
    | Equivalent raw type     | NBT Type                                                                               |
    +=========================+========================================================================================+
    | :class:`str`            | :class:`nbtlib.String`                                                                 |
    +-------------------------+----------------------------------------------------------------------------------------+
    | :class:`int`            | :class:`nbtlib.Int`, :class:`nbtlib.Long`, :class:`nbtlib.Short`, :class:`nbtlib.Byte` |
    +-------------------------+----------------------------------------------------------------------------------------+
    | :class:`float`          | :class:`nbtlib.Float`, :class:`nbtlib.Double`                                          |
    +-------------------------+----------------------------------------------------------------------------------------+
    | :class:`dict`           | :class:`nbtlib.Compound`                                                               |
    +-------------------------+----------------------------------------------------------------------------------------+
    | :class:`list`           | :class:`nbtlib.List`                                                                   |
    +-------------------------+----------------------------------------------------------------------------------------+
    | :class:`~array.array`   | :class:`nbtlib.ByteArray`, :class:`nbtlib.IntArray`, :class:`nbtlib.LongArray`         |
    +-------------------------+----------------------------------------------------------------------------------------+

    Parameters
    ----------
    obj : :class:`nbtlib.tag.Base`
        The NBT object to convert.

    convert_items : :class:`bool`, optional
        Whether or not should convert all items of list, array and dict-related types to python raw types as well.
        Defaults to ``True`` .

    Returns
    -------
    Union[:class:`str`, :class:`dict`, :class:`list`, :class:`~array.array`, :class:`int`, :class:`float`]
        The resulting raw type.

    Warnings
    --------
    Types that convert to a list or dict have each of their values converted as well. To disable this behavior,
    specify ``convert_items=False`` .
    """
    relation_nbt = (
        nbt.String,

        nbt.Int, nbt.Long, nbt.Short, nbt.Byte,

        nbt.Float, nbt.Double,

        nbt.Compound,

        nbt.List,

        nbt.ByteArray, nbt.IntArray, nbt.LongArray
    )

    if obj not in relation_nbt:
        return obj

    relation_types = (
        str,

        int, int, int, int,

        float, float,

        dict,

        list,

        array, array, array
    )

    new_obj = None

    if isinstance(obj, nbt.Compound) and convert_items:
        new_obj = {k: nbt_to_python(v) for k, v in obj.items()}  # convert everything inside
    else:
        for nbt_, type_ in zip(relation_nbt, relation_types):
            if isinstance(obj, nbt_):
                if type_ in (list, array) and convert_items:
                    new_obj = type_(map(lambda v: nbt_to_python(v), obj))
                elif type_ == str:
                    new_obj = type_(obj)
                    new_obj = new_obj.strip(new_obj[0]) if new_obj[0] in ("\"", "'") else new_obj
                else:
                    new_obj = type_(obj)
                break

    return new_obj


def snake_to_capitalized_words(snake_case: str) -> str:
    """Converts a snake_case or SNAKE_CASE string to Capitalized Words format.

    Parameters
    ----------
    snake_case : :class:`str`
        The snake_case string.

    Returns
    -------
    :class:`str`
        The resulting Capitalized Words string.
    """
    return " ".join(map(lambda s: s.capitalize(), snake_case.split("_")))


class DFSerializer(nbt.Serializer):  # override nbt.Serializer to fix numeric tags.
    def serialize_numeric(self, tag: nbt.tag.Base):
        """Return the literal representation of a numeric tag."""
        class_func = int if isinstance(tag, int) else float
        return str(class_func(tag)) + tag.suffix


def serialize_tag(tag, *, indent=None, compact=False, quote=None):
    """Serialize an nbt tag to its literal representation."""
    serializer = DFSerializer(indent=indent, compact=compact, quote=quote)
    return serializer.serialize(tag)


_TT = typing.TypeVar("_TT")


def identity(obj: _TT) -> _TT:
    """Returns the specified object.

    Parameters
    ----------
    obj : Any
        An object.

    Returns
    -------
    Any
        The given object.
    """
    return obj


def dumps_json(obj, *args, **kwargs) -> str:
    """Dumps an object into JSON format, using predefined parameters.

    Parameters
    ----------
    obj : Any
        Object to turn into JSON.

    args : Any
        Arguments to pass to :meth:`json.dumps`.

    kwargs : Any
        Keyword args to pass to :meth:`json.dumps`.

    Returns
    -------
    :class:`str`
        Dumped json.
    """
    ensure_ascii = kwargs.pop("ensure_ascii", False)
    return json.dumps(obj, *args, ensure_ascii=ensure_ascii, **kwargs)
