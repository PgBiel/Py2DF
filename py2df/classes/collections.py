"""
General utility classes.
"""
import typing
import constants
import collections
from classes.mc_types import Item, DFText

class Arguments:
    """
    A container for arguments. In general, only holds the "items" attribute. This class is used in case any other
    properties are added in the future.
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


class ItemCollection(collections.MutableSequence):
    """
    A container for items or other DF types (text variables, number variables...)

    `Attributes`:
        max_len: Maximum length of the item collection, defaults to 27 (small chest).
    """
    max_len = constants.DEFAULT_ITEM_COLLECTION_MAX_LEN

    def __init__(
            self, data: typing.Union[typing.Iterable, Item] = None,
            *items, max_len: typing.Optional[int] = constants.DEFAULT_ITEM_COLLECTION_MAX_LEN
    ):
        super(ItemCollection, self).__init__()
        if data is not None and isinstance(data, collections.abc.Iterable):
            self._list = list(data)
        else:
            self._list: typing.List[typing.Optional[Item]] = [None] * max_len

    def __repr__(self):
        return "<{0} {1}>".format(self.__class__.__name__, self._list)

    def __len__(self):
        """Amount of non-None items in the list."""
        return len(list(filter(None, self._list)))

    def __getitem__(self, ii: int) -> typing.Optional[Item]:
        """
        Get an item at an index. Returns None if there is no item.
        :param ii: Index.
        :return: Item, if any, otherwise None.
        """
        if (ii - 1) > self.max_len:
            raise IndexError(f"Item collection index out of range (max for this instance: {self.max_len - 1}).")

        return self._list[ii]

    def __delitem__(self, ii: int):
        """Delete an item from an index."""
        if (ii - 1) > self.max_len:
            raise IndexError(
                f"Item collection assignment index out of range (max for this instance: {self.max_len - 1})."
            )

        del self._list[ii]

    def __setitem__(self, ii: int, val: typing.Optional[Item]):
        """
        Set an item somewhere in the Item Collection/grid.
        :param ii: Index to set.
        :param val: Item to set.
        """
        # optional: self._acl_check(val)
        if (ii - 1) > self.max_len:
            raise IndexError(
                f"Item collection assignment index out of range (max for this instance: {self.max_len - 1})."
            )

        if val is not None and not isinstance(val, Item):
            raise TypeError("Attempt to set non-Item and non-None value to an ItemCollection instance.")

        self._list[ii] = val

    def __str__(self):
        return str(self._list)

    def __iter__(self):
        for el in self._list:
            yield el

    def as_json_data(self) -> typing.List[dict]:
        """
        Convert this to a JSON-exportable list. (For internal use.)
        :return: A list.
        """
        gen_list: typing.List[dict] = []
        for slot, item in filter(lambda i, el: el is not None, enumerate(self._list)):
            gen_list.append(dict(
                item=item.as_json_data(),
                slot=slot
            ))

        return gen_list

    def insert(self, ii: int, val: Item):
        # optional: self._acl_check(val)
        self._list.insert(ii, val)

    def append(self, val: Item):
        self.insert(len(self._list), val)

    def index(self, x: Item, start: int = None, end: int = None):
        if start is None and end is None:
            return self._list.index(x)
        else:
            start = start if start is not None else 0
            end = end if end is not None else len(self._list)
            return self._list.index(x, start, end)
