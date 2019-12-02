"""
General utility classes.
"""
import typing
import collections
from .. import constants, errors
from .mc_types import Item, DFType
from .abcs import Itemable
from ..utils import remove_u200b_from_doc


class Arguments:
    """A container for arguments. In general, only holds the "items" attribute. This class is used in case any other
    properties are added in the future.

    Attributes
    ----------\u200b
        items : :class:`ItemCollection`
            The ItemCollection held by this Arguments instance.
    """
    items: "ItemCollection"

    def __init__(self, items: "ItemCollection"):
        """
        Init arguments.
        :param items: Items to set.
        """
        self.items = items

    def as_json_data(self) -> dict:
        return dict(items=self.items.as_json_data() if self.items else dict())


class ItemCollection(collections.UserList):  # [DFType]
    """A container for items or other DF types (text variables, number variables...)
    
    Subclasses `collections.UserList`. Supports, as a consequence, most list operations. Do note that it does not allow
    changing the actual size of the list - it's always at the max length, with empty slots of items filled with `None`.
    However, `len()` returns the amount of FILLED slots (amount of items). Also, attempting to `del` or `remove()` will
    only turn the item into an empty slot (None).
    
    Also, `append()` will add to the empty slot with lowest index, erroring if there are not any. `extend()` will
    execute in a similar condition to `append()` for every element in the iterable.
    
    Attributes
    -------------\u200b
        data : List[DFType]
            The internal item list; this should not be modified by the user.
        
        max_len : :class:`int`
            Maximum length of the item collection, defaults to 27 (small chest).

    """
    __slots__ = ("max_len",)

    max_len: int

    def __init__(
        self, data: typing.Optional[typing.Union[typing.Iterable[DFType], DFType]] = constants.DEFAULT_VAL,
        *items: typing.Optional[DFType],  # any other items/empty slots
        max_len: typing.Optional[int] = constants.DEFAULT_ITEM_COLLECTION_MAX_LEN
    ):
        """
        Initializes an item collection.
        
        :param data: An iterable of items (list, ItemCollection, etc.) or a single :class:`Item`/DFType to be
            used with the `items` arg.
        :param items: Any other items to add. If `data` is an iterable, this is not considered.
        :param max_len: The maximum length of this collection, defaults to 27 items (small chest).
        """
        super().__init__()
        self.max_len: int = max_len or constants.DEFAULT_ITEM_COLLECTION_MAX_LEN

        if data is not constants.DEFAULT_VAL:  # if something was given...
            if isinstance(data, collections.abc.Iterable):
                if any(not isinstance(it, Itemable) and it is not None for it in data):
                    raise TypeError("There is a non-Item/DFType/None object within the given `data` arg.")
                
                self.data = list(data)
            else:
                if not isinstance(data, Itemable):
                    raise TypeError("`data` arg passed is not an Iterable nor an Item/DFType.")
                
                if any(not isinstance(it, Itemable) and it is not None for it in items):
                    raise TypeError("There is a non-Item/DFType/None object within the given `items` arg.")
                
                self.data = [data, *items]
            
            length_given = len(self.data)
            
            if length_given > max_len:  # bigger than limit
                raise errors.LimitReachedError(
                    f"Collection items given form a list bigger than max length ({max_len} items for this instance)."
                )
            
            if length_given < max_len:
                self.data.extend([None] * (max_len - length_given))  # fill out the missing empty slots.
        else:
            self.data: typing.List[typing.Optional[DFType]] = [None] * max_len

    def as_json_data(self) -> typing.List[dict]:
        """Convert this to a JSON-exportable list of dicts. (For internal use.)"""
        gen_list: typing.List[dict] = [
            dict(
                item=item.as_json_data(),
                slot=slot                 # We have to filter the enumeration in order to keep the slot indexes.
            ) for slot, item in filter(lambda i, el: el is not None, enumerate(self.data))
        ]

        return gen_list

    def append(self, val: DFType) -> None:
        """Appends an :class:`Item`/DFType to the first empty slot available (smallest None index).

        Parameters
        ----------
        val : `DFType`
            The item/DFType to append.

        Returns
        -------
        None
            None

        Raises
        ------
        TypeError
            If there was an attempt to add `None` or non-`:class:`Item``/`DFType`.
        LimitReachedError
            If there is no empty slot where to append the :class:`Item`/DFType to.

        """
        if not isinstance(val, Itemable):
            raise TypeError("Cannot append non-Item/DFType to ItemCollection.")

        first_available_slot = self.data.index(None)
        if first_available_slot == -1:
            raise errors.LimitReachedError("Cannot append to this item collection: there are no empty slots left.")

        self[first_available_slot] = typing.cast(DFType, val)

    def remove(self, x: DFType) -> None:
        """Removes an :class:`Item`/DFType, setting it to None.

        Parameters
        ----------
        x : DFType
            :class:`Item`/DFType to remove.

        Returns
        -------
        None
            None

        """
        if x is None:
            raise TypeError("Cannot remove None (empty slot) from ItemCollection.")
            
        index_at = self.data.index(x)
        if index_at == -1:
            raise ValueError("ItemCollection.remove(x): Item/DFType not in collection.")

        super().__delitem__(index_at)  # remove data
        super().insert(index_at, None)

    def clear(self) -> None:
        """Replaces the entire item collection with empty slots."""
        old_len = len(self.data)
        super().clear()  # clears data
        self.data = [None] * old_len  # sets it all to None

    def extend(self, other: typing.Iterable[DFType]) -> None:
        """Appends multiple items by replacing empty slots.

        Parameters
        ----------
        other : Iterable[DFType]
            Iterable of :class:`Item`/DFType.

        Returns
        -------
        None
            None
        """
        empty_slots = list(map(lambda t: t[0], filter(lambda i, el: el is None, enumerate(self.data))))
        if len(empty_slots) < 1:
            raise errors.LimitReachedError("Cannot extend this item collection: there are no empty slots left.")

        empty_slots.append(None)  # so we can detect if the max length has been surpassed, otherwise zip just stops.

        for item, slot in zip(other, empty_slots):
            if not isinstance(item, Itemable):
                raise TypeError("Iterable to extend with contains non-Item/DFType.")

            if slot is None:
                raise errors.LimitReachedError("Cannot extend this item collection: there are no empty slots left.")

            super().__setitem__(slot, item)

    def __repr__(self) -> str:
        return "<{0} len={1} [{2}]>".format(
            self.__class__.__name__, len(self), ", ".join(el.__repr__() for el in self.data)
        )

    def __len__(self) -> int:
        """Amount of non-None items in the collection."""
        return len(list(filter(None, self.data)))

    def __getitem__(self, ii: int) -> typing.Optional[DFType]:
        """
        Get an item at an index. Returns None if there is no item.

        :param ii: Index.
        :return: :class:`Item`, if any, otherwise None.
        """
        if (ii - 1) > self.max_len:
            raise IndexError(f"Item collection index out of range (max for this instance: {self.max_len - 1}).")

        return super().__getitem__(ii)

    def __delitem__(self, ii: int) -> None:
        """Delete an item from an index, turning it into an empty slot (None)."""

        if (ii - 1) > self.max_len:
            raise IndexError(
                f"Item collection assignment index out of range (max for this instance: {self.max_len - 1})."
            )

        super().__delitem__(ii)
        self.data.insert(ii, None)

    def __setitem__(self, ii: int, val: typing.Optional[DFType]) -> None:
        """
        Set an item somewhere in the :class:`Item` Collection/grid.

        :param ii: Index to set.
        :param val: :class:`Item`/DF type to set.
        """
        # optional: self._acl_check(val)
        if (ii - 1) > self.max_len:
            raise IndexError(
                f"Item collection assignment index out of range (max for this instance: {self.max_len - 1})."
            )

        if val is not None and not isinstance(val, Itemable):
            raise TypeError("Attempt to set non-Item/DF type and non-None value to an ItemCollection instance.")

        super().__setitem__(ii, typing.cast(DFType, val))

    def __delslice__(self, i, j) -> None:
        the_slice = self.data[i:j]
        self.data[i:j] = [None] * len(the_slice)  # replace with None


_col_classes = (Arguments, ItemCollection)
for cls in _col_classes:
    remove_u200b_from_doc(cls)
