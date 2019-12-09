import collections
import inspect
import typing

from ..classes import CallableBlock, Tag, JSONData, Arguments, Item
from ..enums import BlockType, CallableAction
from ..utils import remove_u200b_from_doc
from .reader import DFReader


class Function(CallableBlock):
    """Used to define a line of code that can be called with a Call Function block. Decorator. Example usage::

        @Function(name="My Function")  # 'hidden' is False by default
        def my_function():
            # code

        @Function(name="Other Function", hidden=False)
        def other_function():
            # code

        @Function  # default name is the function's name as Capitalized Words.
        def cool_function():  # in this case, the name will be 'Cool Function'
            # code

    Parameters
    ----------\u200b
    name_or_func : Union[:class:`str`, Callable]
        Can be either the proper Python function containing the code to be run when this Function/Process is called,
        or the name of this Function/Process (its :attr:`data`).

    hidden : :class:`bool`, optional
        Whether or not this Function is hidden in the Call Function menu. Defaults to ``False``.

    item_icon : Optional[:class:`~py2df.classes.mc_types.Item`], optional
        An optional item that represents this Function in the Call Function menu.

    Attributes
    ----------\u200b
    block : :attr:`~py2df.enums.parameters.BlockType.FUNCTION`
        The type of this codeblock (Function).

    args : :attr:`~py2df.classes.collections.Arguments`
        The arguments of the Function (containing the item icon, if specified, and the Hidden tag, i.e.,
        whether or not the Function is hidden in the Call Function menu).

    action : ``None``
        ('Function' codeblocks have no action.)

    sub_action : ``None``
        ('Function' codeblocks have no sub-actions.)

    function : Callable
        The Python function containing this Function's code.

    item_icon : Optional[:class:`~py2df.classes.mc_types.Item`]
        An optional item that represents this Function in the Call Function menu.

    length : :class:`int`
        The length of a Function codeblock, in blocks. This is always 2.

    name : :class:`str`
        The name of this function.

    data : :class:`str`
        The name of this function (same as :attr:`Function.name`).

    hidden : :class:`bool`
        Whether or not this function is hidden in the Call Function menu. Defaults to ``False``.

    target : ``None``
        ('Function' codeblocks have no targets.)
    """
    __slots__ = ("data", "hidden", "item_icon", "function")
    block: BlockType = BlockType.FUNCTION
    args: Arguments
    action: None = None
    sub_action: None = None
    function: typing.Callable
    length: int = 2
    data: str  # Name
    item_icon: typing.Optional[Item]
    hidden: bool
    target: None = None

    @property
    def args(self) -> Arguments:
        """The arguments of the Function (containing the item icon, if specified, and the Hidden tag, i.e., whether \
or not the Function is hidden in the Call Function menu)."""
        return Arguments(
            *([(self.item_icon.to_item(),)] if self.item_icon else []),
            tags=[Tag("Is Hidden", option=self.hidden, action=CallableAction.DYNAMIC, block=BlockType.FUNCTION)]
        )

    def __call__(self, func: typing.Callable) -> "Function":  # decorate
        """Decorator for storing this Function and its line of code.

        Parameters
        ----------
        func : Callable
            The Python function containing the code that will be run when this function is invoked
            by a Call Function block.

        Returns
        -------
        :class:`Function`
            self

        Notes
        -----
        This appends the Function to the list of lines in the :class:`~py2df.reading.reader.DFReader` singleton.
        """
        self.function = func

        DFReader().append_function(self)

        return self


class Process(CallableBlock):
    """Used to define a line of code that can be called with a Call Process block. Decorator. Example usage::

        @Process(name="My Process")  # 'hidden' is False by default
        def my_process():
            # code

        @Process(name="Other Process", hidden=False)
        def other_process():
            # code

        @Process  # default name is the process name as Capitalized Words.
        def cool_process():  # in this case, the name will be 'Cool Process'
            # code

    Parameters
    ----------\u200b
    name_or_func : Union[:class:`str`, Callable]
        Can be either the proper Python function containing the code to be run when this Process is started,
        or the name of this Process (its :attr:`data`).

    hidden : :class:`bool`, optional
        Whether or not this Process is hidden in the Start Process menu. Defaults to ``False``.

    item_icon : Optional[:class:`~py2df.classes.mc_types.Item`], optional
        An optional item that represents this Process in the Start Process menu.

    Attributes
    ----------\u200b
    block : :attr:`~py2df.enums.parameters.BlockType.PROCESS`
        The type of this codeblock (Process).

    args : :attr:`~py2df.classes.collections.Arguments`
        The arguments of the Process (containing the Hidden tag, i.e., whether or not the Process is hidden in
        the Start Process menu).

    action : ``None``
        ('Process' codeblocks have no action.)

    sub_action : ``None``
        ('Process' codeblocks have no sub-actions.)

    function : Callable
        The Python function containing this Process's code.

    item_icon : Optional[:class:`~py2df.classes.mc_types.Item`]
        An optional item that represents this Process in the Start Process menu.

    length : :class:`int`
        The length of a Process codeblock, in blocks. This is always 2.

    name : :class:`str`
        The name of this function.

    data : :class:`str`
        The name of this function (same as :attr:`Process.name`).

    hidden : :class:`bool`
        Whether or not this function is hidden in the Call Process menu. Defaults to ``False``.

    target : ``None``
        ('Process' codeblocks have no targets.)
    """
    __slots__ = ("data", "hidden", "item_icon", "function")
    block: BlockType = BlockType.PROCESS
    args: Arguments
    action: None = None
    sub_action: None = None
    function: typing.Callable
    length: int = 2
    data: str  # Name
    item_icon: typing.Optional[Item]
    hidden: bool
    target: None = None

    @property
    def args(self) -> Arguments:
        """The arguments of the Function (containing the item icon, if specified, and the Hidden tag, i.e., whether \
or not the Function is hidden in the Call Function menu)."""
        return Arguments(
            *([(self.item_icon.to_item(),)] if self.item_icon else []),
            tags=[Tag("Is Hidden", option=self.hidden, action=CallableAction.DYNAMIC, block=BlockType.FUNCTION)]
        )

    def __call__(self, func: typing.Callable) -> "Process":  # decorate
        """Decorator for storing this Process and its line of code.

        Parameters
        ----------
        func : Callable
            The Python function containing the code that will be run when this Process is invoked
            by a Start Process block.

        Returns
        -------
        :class:`Process`
            self

        Notes
        -----
        This appends the Process to the list of lines in the :class:`~py2df.reading.reader.DFReader` singleton.
        """
        self.function = func

        DFReader().append_function(self)

        return self


remove_u200b_from_doc(Function, Process)
