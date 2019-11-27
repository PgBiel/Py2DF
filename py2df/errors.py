"""
Custom errors used by py2df.
"""


class Py2DfError(Exception):
    pass


class Py2DfCollectionError(Py2DfError):
    pass


class LimitReachedError(Py2DfCollectionError):
    """
    Indicates that the limit of elements in this collection (Lore, ItemCollection etc.) has been reached.
    """
    pass  #

