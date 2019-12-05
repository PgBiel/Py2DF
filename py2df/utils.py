import typing
import collections
from dataclasses import dataclass


class NBTWrapper(collections.UserString):
    """Wraps SNBT (NBT string) to be input literally by :meth:`nbt_dict_to_str`.

    Attributes\u200b
    -----------
        data : :class:`str`
            The SBNT value that this instance represents.
    """
    __slots__ = ()


def nbt_dict_to_str(nbt_dict: dict) -> str:
    pass  # TODO: NBT Dict to str


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
    if isinstance(obj, collections.Iterable):
        for clz in obj:
            remove_u200b_from_doc(clz)
    else:
        the_doc = obj.__doc__
        if "\u200b" in the_doc:
            obj.__doc__ = the_doc.replace("\u200b", "")

    for o in other_objs:
        remove_u200b_from_doc(o)


def flatten(*args: typing.Any, allow_iterables: bool = True) -> list:
    """
    Flatten a list or iterable (if ``allow_iterables = True`` of arbitrary length

        >>> from py2df import flatten
        >>> flatten(1, 2, ['b', 'a' , ['c', 'd']], 3)
        [1, 2, 'b', 'a', 'c', 'd', 3]

    Parameters
    ----------
    args : Any
        Items and lists to be combined into a single list.

    allow_iterables : :class:`bool`, optional
        Whether or not to flatten any kind of Iterable, and not just :class:`list` or :class:`tuple`; defaults to True.

    Returns
    -------
    :class:`list`
        Resulting list.

    Warnings
    --------
    If ``allow_iterables`` is set to ``True``, then ANY iterable will be flattened into the list, including, for
    example, instances of :class:`dict` . Therefore, use this option wisely. The default is True for the purposes
    of this library.

    Notes
    -----
    Credits to NLTK authors for this function's original code.
    """

    x = []
    for el in args:
        is_iterable = isinstance(el, collections.Iterable)
        if (
            not isinstance(el, (list, tuple))
            and (not is_iterable if allow_iterables else True)
        ):
            el = [el]

        for item in el:
            if isinstance(item, (list, tuple)) or (allow_iterables and is_iterable):
                x.extend(flatten(item))
            else:
                x.append(item)
    return x


remove_u200b_from_doc(NBTWrapper)
