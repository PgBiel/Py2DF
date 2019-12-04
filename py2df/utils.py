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


remove_u200b_from_doc(NBTWrapper)
