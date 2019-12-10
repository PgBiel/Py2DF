"""
Custom errors used by py2df.

Exception Hierarchy
-------------------

.. exception_hierarchy::

    - :exc:`Exception`
        - :exc:`Py2DFError`
            - :exc:`Py2DFCollectionError`
                - :exc:`LimitReachedError`
"""


class Py2DfError(Exception):
    """Any custom error by this library is a subclass of this exception."""
    pass


class Py2DfCollectionError(Py2DfError):
    """Any error related to Py2DF collection classes."""
    pass


class LimitReachedError(Py2DfCollectionError):
    """Indicates that the limit of elements in this collection (Lore, ItemCollection etc.) has been reached."""
    pass

