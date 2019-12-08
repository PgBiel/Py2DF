"""
Collections required by Minecraft Type classes. This is used to avoid cyclic imports.
"""
import typing
import collections
from .. import errors
from ..constants import MAX_LORE_LINES  # 100
from ..utils import remove_u200b_from_doc


class Lore(collections.UserList):  # [typing.Optional[str]]
    """
    Represents an :class:`~py2df.classes.mc_types.Item` 's lore.

    Subclasses :class:`collections.UserList`, so supports all :class:`list` -related operations.

    Parameters
    ----------\u200b
    iter : Optional[Iterable[:class:`str`]], optional
        List of lines as an Iterable. (Optional)

    Attributes\u200b
    -----------
        data : List[:class:`str`]
            Internal list containing lore lines.
    """
    __slots__ = ()

    def __init__(self, iter: typing.Optional[typing.Iterable[str]] = None):
        """
        Init a Lore collection.

        Parameters
        ----------
        iter : Optional[Iterable[:class:`str`]], optional
            List of lines as an Iterable. (Optional)
        """
        if type(iter) == Lore:
            self.data = iter.data[:]  # allow easy and efficient use of Lore(Lore(...))
            super().__init__()
        else:
            if iter:
                super().__init__(map(str, iter))
            else:
                super().__init__()

        if self.data:
            curr_data_len = len(self.data)
            
            if curr_data_len > MAX_LORE_LINES:
                raise errors.LimitReachedError(
                    f"Attempted to add more than the limit of lore lines ({MAX_LORE_LINES})."
                )

    def append(self, text: str) -> None:
        """Append a line after the last written line.

        Parameters
        ----------
        text : str
            Text to be written. Can not be None.

        Raises
        ------
        :exc:`LimitReachedError`
            If there was an attempt to surpass the limit of lore lines (100).
        :exc:`TypeError`
            If None was given.

        """
        if len(self.data) == MAX_LORE_LINES:
            raise errors.LimitReachedError(
                f"Attempted to add more than the limit of lore lines ({MAX_LORE_LINES})."
            )

        if text is None:
            raise TypeError("Line to append must not be None.")

        self.data.append(text)

    def extend(self, other: typing.Optional[typing.Iterable[str]]) -> None:
        f"""Extends the lore line list.

        Parameters
        ----------
        other : Optional[Iterable[str]
            Iterable to be added into the line list.

        Raises
        ------
        :exc:`LimitReachedError`
            If there was an attempt to surpass the limit of lore lines ({MAX_LORE_LINES}).

        """
        for item in other:
            if len(self.data) == MAX_LORE_LINES:
                raise errors.LimitReachedError(
                    f"Could not finish extending due to reaching the limit of lore lines ({MAX_LORE_LINES})."
                )

            self.data.append(item)

    def as_json_data(self) -> list:
        """Returns this Lore item as valid json data (list).

        Returns
        -------
        List[str]
            List of lines as strings (any None become "")
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


remove_u200b_from_doc(Lore)
