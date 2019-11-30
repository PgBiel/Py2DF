"""
Collections required by Minecraft Type classes. This is used to avoid cyclic imports.
"""
import collections
import errors
import typing
from constants import MAX_LORE_LINES  # 100


class Lore(collections.UserList[typing.Optional[str]]):
    __slots__ = ()

    def __init__(self, iter: collections.Iterable[typing.Optional[str]] = None):
        """
        Init a Lore collection.

        :param iter: List of lines as an Iterable. (Optional)
        """
        if type(iter) == Lore:
            self.data = iter.data[:]  # allow easy and efficient use of Lore(Lore(...))
            super().__init__()
        else:
            super().__init__(map(str, iter))

        if self.data:
            curr_data_len = len(self.data)
            
            if curr_data_len > MAX_LORE_LINES:
                raise errors.LimitReachedError(
                    f"Attempted to add more than the limit of lore lines ({MAX_LORE_LINES})."
                )

    def append(self, text: str) -> None:
        """
        Append a line after the last written line.

        :param text: Text to be written. Can not be None.
        :raises LimitReachedError: If there was an attempt to surpass the limit of lore lines (100).
        :raises TypeError: If None was given.
        """
        if len(self.data) == MAX_LORE_LINES:
            raise errors.LimitReachedError(
                f"Attempted to add more than the limit of lore lines ({MAX_LORE_LINES})."
            )

        if text is None:
            raise TypeError("Line to append must not be None.")

        self.data.append(text)

    def extend(self, other: collections.Iterable[typing.Optional[str]]) -> None:
        """
        Extends the lore line list.

        :param other: Iterable to be added into the line list.
        :raises LimitReachedError: If there was an attempt to surpass the limit of lore lines (100).
        """
        for item in other:
            if len(self.data) == MAX_LORE_LINES:
                raise errors.LimitReachedError(
                    f"Could not finish extending due to reaching the limit of lore lines ({MAX_LORE_LINES})."
                )

            self.data.append(item)

    def as_json_data(self) -> list:
        """
        Returns this Lore item as valid json data (list).

        :return: List of lines as strings (None becomes "")
        """
        return list(map(lambda t: str(t) if t else "", self.data))

    def __setitem__(self, key: typing.Union[int, slice], value: typing.Optional[str]):
        if type(key) == int:
            val_to_check = key
        else:
            val_to_check = key.stop  # check if exceeds max / should extend list
            
        if val_to_check > MAX_LORE_LINES - 1:
            raise errors.LimitReachedError(
                f"Attempted to add more than the limit of lore lines ({MAX_LORE_LINES})."
            )
        
        curr_data_len = len(self.data)
        if val_to_check > curr_data_len - 1:
            if value is None:
                return  # better not extend the list just to add more None...

            self.data.extend([None] * (val_to_check - curr_data_len + 1))
            
        super().__setitem__(key, value)



