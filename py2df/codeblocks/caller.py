from ..classes import CallerBlock
from ..enums import BlockType
from ..reading.reader import DFReader
from ..utils import remove_u200b_from_doc


class CallFunction(CallerBlock):
    """Represents a Call Function block. Calls, in DiamondFire, a pre-determined :class:`~.Function`.

    Parameters\u200b
    ----------
    name : :class:`str`
        The name of the function to call.

    append_to_reader : :class:`bool`, optional
        Whether or not this CallFunction should already be appended to the Reader (i.e., added to the code line);
        defaults to True.

    Attributes\u200b
    ------------
    block : :attr:`~py2df.enums.parameters.BlockType.CALL_FUNC`
        The type of the codeblock (Call Function).

    args : ``None``
        (Call Function codeblocks have no arguments.)

    action : ``None``
        (Call Function codeblocks have no action.)

    sub_action : ``None``
        (Call Function codeblocks have no sub-actions.)

    length : :class:`int`
        The length of a Call Function codeblock, in blocks. This is always 2.

    name : :class:`str`
        The name of the function to call.

    data : :class:`str`
        The name of the function to call (same as :attr:`name`).

    target : ``None``
        (Call Function codeblocks have no targets.)
    """
    __slots__ = ("data",)
    block: BlockType = BlockType.CALL_FUNC
    args: None = None
    action: None = None
    sub_action: None = None
    length: int = 2
    data: str
    target: None = None

    def __init__(self, name: str, *, append_to_reader: bool = True):
        self.data = ''
        self.name = str(name)  # run checks

        if append_to_reader:
            DFReader().append_codeblock(self)


class StartProcess(CallerBlock):
    """Represents a Start Process block. Calls, in DiamondFire, a pre-determined :class:`~.Process`.

    Parameters\u200b
    ----------
    name : :class:`str`
        The name of the process to call.

    append_to_reader : :class:`bool`, optional
        Whether or not this StartProcess should already be appended to the Reader (i.e., added to the code line);
        defaults to True.

    Attributes\u200b
    ------------
    block : :attr:`~py2df.enums.parameters.BlockType.START_PROCESS`
        The type of the codeblock (`Start Process`).

    args : ``None``
        (Start Process codeblocks have no arguments.)

    action : ``None``
        (Start Process codeblocks have no action.)

    sub_action : ``None``
        (Start Process codeblocks have no sub-actions.)

    length : :class:`int`
        The length of a Start Process codeblock, in blocks. This is always 2.

    name : :class:`str`
        The name of the process to call.

    data : :class:`str`
        The name of the process to call (same as :attr:`name`).

    target : ``None``
        (Start Process codeblocks have no targets.)
    """
    __slots__ = ("data",)
    block: BlockType = BlockType.START_PROCESS
    args: None = None
    action: None = None
    sub_action: None = None
    length: int = 2
    data: str
    target: None = None

    def __init__(self, name: str, *, append_to_reader: bool = True):
        self.data = ''
        self.name = str(name)  # run checks

        if append_to_reader:
            DFReader().append_codeblock(self)


remove_u200b_from_doc(CallFunction, StartProcess)
