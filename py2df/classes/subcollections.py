"""
Collections required by Minecraft Type classes. This is used to avoid cyclic imports.
"""
import collections
import constants
import errors


class Lore(collections.UserList):
    __slots__ = ()

    def __init__(self, iter: collections.Iterable = None):
        super().__init__(map(str, iter))
        if self.data:
            if len(self.data) > constants.MAX_LORE_LINES:
                raise errors.LimitReachedError(
                    f"Attempted to add more than the limit of lore lines ({constants.MAX_LORE_LINES})."
                )

# TODO: Finish Lore class
