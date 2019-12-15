import typing
from collections import deque
from abc import abstractmethod

from ..errors import DFSyntaxError
from ..enums import (
    PlayerTarget, EntityTarget, BlockType, IfPlayerType, IfEntityType, IfGameType, IfVariableType,
    SelectionTarget,
    BracketDirection, BracketType, IfType)
from ..classes import JSONData, Arguments, BracketedBlock, Block, Bracket, DFVariable, DFGameValue
from ..utils import remove_u200b_from_doc
from ..constants import BLOCK_ID, DEFAULT_VAL
from ..reading.reader import DFReader


class IfBlock(BracketedBlock, JSONData):
    """An ABC representing an If Block. Executes code if a certain condition is met.

    Parameters
    ----------\u200b
    action : :class:`~py2df.enums.actions.IfType`
        The condition to check.

    args : :class:`~py2df.classes.collections.Arguments`
        The arguments of this If block.

    target : Optional[:class:`~py2df.enums.targets.Target`], optional
        The target of this If, if there exists. If this is None, DiamondFire will default to the current selection
        (if exists) or it will be ignored (if it doesn't, as occurs in 'If Game' and 'If Var')

    append_to_reader : :class:`bool`, optional
        Whether or not this newly-created If should be already appended to the
        :class:`~py2df.reading.reader.DFReader`. Defaults to ``True``.

    invert : :class:`bool`, optional
        If ``True`` , then this If's code will only execute when the condition is false (i.e., applies NOT).
        Default: ``False``

    codeblocks : Iterable[:class:`~py2df.classes.abc.Block`], optional
        The blocks, including Brackets, inside this If. Defaults to empty deque (None).

    Attributes
    ----------\u200b
    block : Union[:attr:`~py2df.enums.parameters.IF_PLAYER`, :attr:`~py2df.enums.parameters.IF_ENTITY`, \
:attr:`~py2df.enums.parameters.IF_GAME`, :attr:`~py2df.enums.parameters.IF_VAR`]
        The type of this codeblock.

    args : :class:`~py2df.classes.collections.Arguments`
        The arguments of this If block.

    action : :class:`~py2df.enums.actions.IfType`
        The condition to check.

    codeblocks : Deque[:class:`~py2df.classes.abc.Block`]
        The blocks, including Brackets, inside this If.

    invert : :class:`bool`
        If ``True`` , then this If's code will only execute when the condition is false (i.e., applies NOT).
        Default: ``False``

    sub_action : ``None``
        ('If' has no sub actions.)

    length : :class:`int`
        The length of each individual If (excluding brackets). This is always equal to 1.

    total_length : :class:`int`
        The sum of all lengths of all codeblocks inside this If, including If itself and brackets (so 3 + inner length).

    data : ``None``
        ('If' has no extra codeblock data.)

    target : Optional[:class:`~py2df.enums.targets.Target`]
        The target of this If, or ``None`` for current selection (if there exists) or in case of there not being
        any target (e.g. 'If Game').
    """
    __slots__ = ()

    block: BlockType = NotImplemented
    args: Arguments
    action: IfType
    codeblocks: typing.Deque[Block]
    invert: bool
    sub_action: None = None
    length: int = 1
    data: None = None
    target: typing.Optional[PlayerTarget]

    def __enter__(self) -> "IfBlock":
        """
        Triggers the creation of an opening bracket and the addition of all codeblocks into this If block.

        Returns
        -------
        :class:`IfBlock`
            self (The current instance)
        """
        self.codeblocks.appendleft(Bracket(BracketDirection.OPEN, BracketType.NORM))
        reader = DFReader()

        if reader.curr_code_loc and self not in reader.curr_code_loc:
            reader.append_codeblock(self)

        reader.curr_code_loc = self
        return self

    def __exit__(self, _exc_type, _exc_val, _exc_tb) -> None:
        """
        Closes the Bracket, and resets the location of codeblocks (i.e., they now go outside the brackets).

        Returns
        -------
        ``None``
            ``None``
        """
        self.codeblocks.append(Bracket(BracketDirection.CLOSE, BracketType.NORM))
        DFReader().close_code_loc()

    def as_json_data(self) -> dict:
        """
        Produces a JSON-serializable dict representing this If.

        Returns
        -------
        :class:`dict`
        """
        return dict(
            id=BLOCK_ID,
            block=self.block.value,
            args=self.args.as_json_data(),
            action=self.action.value,
            **(dict(target=self.target.value) if self.target else dict()),
            **(dict(inverted="NOT") if self.invert else dict())
        )

    @abstractmethod
    def __neg__(self):
        raise NotImplementedError

    def __invert__(self):
        return self.__neg__()


class IfPlayer(IfBlock):
    """An If Player block. Executes code if a certain condition related to a player is met.

    Parameters
    ----------\u200b
    action : :class:`~py2df.enums.actions.IfPlayerType`
        The condition to check on the player.

    args : :class:`~py2df.classes.collections.Arguments`
        The arguments of this If Player.

    target : Optional[:class:`~py2df.enums.targets.PlayerTarget`], optional
        The target of this If Player. If this is None, DiamondFire will default to the current selection.

    append_to_reader : :class:`bool`, optional
        Whether or not this newly-created :class:`IfPlayer` should be already appended to the
        :class:`~py2df.reading.reader.DFReader`. Defaults to ``True``.

    invert : :class:`bool`, optional
        If ``True`` , then this If Player's code will only execute when the condition is false (i.e., applies NOT).
        Default: ``False``

    codeblocks : Iterable[:class:`~py2df.classes.abc.Block`], optional
        The blocks, including Brackets, inside this If Player. Defaults to empty deque (None).

    Attributes
    ----------\u200b
    block : :attr:`~py2df.enums.parameters.BlockType.IF_PLAYER`
        The type of this codeblock (If Player).

    args : :class:`~py2df.classes.collections.Arguments`
        The arguments of this If Player.

    action : :class:`~py2df.enums.actions.IfPlayerType`
        The condition to check.

    codeblocks : Deque[:class:`~py2df.classes.abc.Block`]
        The blocks, including Brackets, inside this If Player.

    invert : :class:`bool`
        If ``True`` , then this If Player's code will only execute when the condition is false (i.e., applies NOT).
        Default: ``False``

    sub_action : ``None``
        (If Player has no sub actions.)

    length : :class:`int`
        The length of each individual If Player (excluding brackets). This is always equal to 1.

    data : ``None``
        (If Player has no extra codeblock data.)

    target : Optional[:class:`~py2df.enums.targets.PlayerTarget`]
        The target of this If Player, or ``None`` for current selection.
    """
    __slots__ = ("args", "action", "target", "invert", "codeblocks")

    block: BlockType = BlockType.IF_PLAYER
    args: Arguments
    action: IfPlayerType
    codeblocks: typing.Deque[Block]
    invert: bool
    sub_action: None = None
    length: int = 1
    data: None = None
    target: typing.Optional[PlayerTarget]

    def __init__(
        self, action: IfPlayerType, args: Arguments = Arguments(),
        target: typing.Union[PlayerTarget, SelectionTarget] = DEFAULT_VAL,
        *, append_to_reader: bool = False, invert: bool = False, codeblocks: typing.Iterable[Block] = None
    ):
        """
        Initialize this If Player.

        Parameters
        ----------
        action : :class:`~py2df.enums.actions.IfPlayerType`
            The type of If Player this is.

        args : :class:`~py2df.classes.collections.Arguments`
            The arguments of this If Player.

        target : :class:`~py2df.enums.targets.PlayerTarget`, optional
            The target of this If Player. Defaults to :attr:`~py2df.enums.targets.PlayerTarget.DEFAULT` (Default
            Player).

        append_to_reader : :class:`bool`, optional
            Whether or not this newly-created :class:`IfPlayer` should already be appended to the
            :class:`~py2df.reading.reader.DFReader`. Defaults to ``False`` (because it is already appended
            when :meth:`~IfPlayer.__enter__` is called).

        invert : :class:`bool`, optional
            If ``True`` , then this If Player's code will only execute when the condition is false (i.e., applies NOT).
            Default: ``False``

        codeblocks : Iterable[:class:`~py2df.classes.abc.Block`], optional
            The blocks, including Brackets, inside this If Player. Defaults to empty deque (None).
        """
        self.action = IfPlayerType(action)
        self.args = args
        self.target = PlayerTarget(
            target.value if SelectionTarget in (target, type(target)) else target
        ) if target else None

        self.codeblocks = deque(codeblocks) if codeblocks else deque()
        self.invert = invert

        if append_to_reader:
            DFReader().append_codeblock(self)

    def __neg__(self):
        return IfPlayer(
            self.action, self.args, self.target, append_to_reader=False, invert=-self.invert,
            codeblocks=self.codeblocks
        )


class IfEntity(IfBlock):
    """An If Entity block. Executes code if a certain condition related to a entity is met.

    Parameters
    ----------\u200b
    action : :class:`~py2df.enums.actions.IfEntityType`
        The condition to check on the entity.

    args : :class:`~py2df.classes.collections.Arguments`
        The arguments of this If Entity.

    target : Optional[:class:`~py2df.enums.targets.EntityTarget`], optional
        The target of this If Entity. If this is None, DiamondFire will default to the current selection.

    append_to_reader : :class:`bool`, optional
        Whether or not this newly-created :class:`IfEntity` should be already appended to the
        :class:`~py2df.reading.reader.DFReader`. Defaults to ``True``.

    invert : :class:`bool`, optional
        If ``True`` , then this If Entity's code will only execute when the condition is false (i.e., applies NOT).
        Default: ``False``

    codeblocks : Iterable[:class:`~py2df.classes.abc.Block`], optional
        The blocks, including Brackets, inside this If Entity. Defaults to empty deque (None).

    Attributes
    ----------\u200b
    block : :attr:`~py2df.enums.parameters.BlockType.IF_ENTITY`
        The type of this codeblock (If Entity).

    args : :class:`~py2df.classes.collections.Arguments`
        The arguments of this If Entity.

    action : :class:`~py2df.enums.actions.IfEntityType`
        The condition to check.

    codeblocks : Deque[:class:`~py2df.classes.abc.Block`]
        The blocks, including Brackets, inside this If Entity.

    invert : :class:`bool`
        If ``True`` , then this If Entity's code will only execute when the condition is false (i.e., applies NOT).
        Default: ``False``

    sub_action : ``None``
        (If Entity has no sub actions.)

    length : :class:`int`
        The length of each individual If Entity (excluding brackets). This is always equal to 1.

    data : ``None``
        (If Entity has no extra codeblock data.)

    target : Optional[:class:`~py2df.enums.targets.EntityTarget`]
        The target of this If Entity, or ``None`` for current selection.
    """
    __slots__ = ("args", "action", "target", "invert", "codeblocks")

    block: BlockType = BlockType.IF_ENTITY
    args: Arguments
    action: IfEntityType
    codeblocks: typing.Deque[Block]
    invert: bool
    sub_action: None = None
    length: int = 1
    data: None = None
    target: typing.Optional[EntityTarget]

    def __init__(
        self, action: IfEntityType, args: Arguments = Arguments(),
        target: typing.Union[EntityTarget, SelectionTarget] = DEFAULT_VAL,
        *, append_to_reader: bool = False, invert: bool = False, codeblocks: typing.Iterable[Block] = None
    ):
        """
        Initialize this If Entity.

        Parameters
        ----------
        action : :class:`~py2df.enums.actions.IfEntityType`
            The type of If Entity this is.

        args : :class:`~py2df.classes.collections.Arguments`
            The arguments of this If Entity.

        target : :class:`~py2df.enums.targets.EntityTarget`, optional
            The target of this If Entity. Defaults to :attr:`~py2df.enums.targets.EntityTarget.DEFAULT` (Default
            Entity).

        append_to_reader : :class:`bool`, optional
            Whether or not this newly-created :class:`IfEntity` should already be appended to the
            :class:`~py2df.reading.reader.DFReader`. Defaults to ``False`` (because it is already appended
            when :meth:`~IfEntity.__enter__` is called).

        invert : :class:`bool`, optional
            If ``True`` , then this If Entity's code will only execute when the condition is false (i.e., applies NOT).
            Default: ``False``

        codeblocks : Deque[:class:`~py2df.classes.abc.Block`], optional
            The blocks, including Brackets, inside this If Entity. Defaults to empty deque (None).
        """
        self.action = IfEntityType(action)
        self.args = args
        self.target = EntityTarget(
            target.value if SelectionTarget in (target, type(target)) else target
        ) if target else None

        self.codeblocks = deque(codeblocks) if codeblocks else deque()
        self.invert = invert

        if append_to_reader:
            DFReader().append_codeblock(self)

    def __neg__(self):
        return IfEntity(
            self.action, self.args, self.target, append_to_reader=False, invert=-self.invert,
            codeblocks=self.codeblocks
        )


class IfGame(IfBlock):
    """An If Game block. Executes code if a certain condition related to the game (state of the plot, a block etc.)
    is met.

    Parameters
    ----------\u200b
    action : :class:`~py2df.enums.actions.IfGameType`
        The condition to check.

    args : :class:`~py2df.classes.collections.Arguments`
        The arguments of this If Game.

    append_to_reader : :class:`bool`, optional
        Whether or not this newly-created :class:`IfGame` should be already appended to the
        :class:`~py2df.reading.reader.DFReader`. Defaults to ``True``.

    invert : :class:`bool`, optional
        If ``True`` , then this If Game's code will only execute when the condition is false (i.e., applies NOT).
        Default: ``False``

    codeblocks : Iterable[:class:`~py2df.classes.abc.Block`], optional
        The blocks, including Brackets, inside this If Game. Defaults to empty deque (None).

    Attributes
    ----------\u200b
    block : :attr:`~py2df.enums.parameters.BlockType.IF_GAME`
        The type of this codeblock (If Game).

    args : :class:`~py2df.classes.collections.Arguments`
        The arguments of this If Game.

    action : :class:`~py2df.enums.actions.IfGameType`
        The condition to check.

    codeblocks : Deque[:class:`~py2df.classes.abc.Block`]
        The blocks, including Brackets, inside this If Game.

    invert : :class:`bool`
        If ``True`` , then this If Game's code will only execute when the condition is false (i.e., applies NOT).
        Default: ``False``

    sub_action : ``None``
        (If Game has no sub actions.)

    length : :class:`int`
        The length of each individual If Game (excluding brackets). This is always equal to 1.

    data : ``None``
        (If Game has no extra codeblock data.)

    target : ``None``
        (If Game has no target.)
    """
    __slots__ = ("args", "action", "invert", "codeblocks")

    block: BlockType = BlockType.IF_GAME
    args: Arguments
    action: IfGameType
    codeblocks: typing.Deque[Block]
    invert: bool
    sub_action: None = None
    length: int = 1
    data: None = None
    target: None = None

    def __init__(
        self, action: IfGameType, args: Arguments = Arguments(),
        *, append_to_reader: bool = False, invert: bool = False, codeblocks: typing.Iterable[Block] = None
    ):
        """
        Initialize this If Game.

        Parameters
        ----------
        action : :class:`~py2df.enums.actions.IfGameType`
            The condition to check.

        args : :class:`~py2df.classes.collections.Arguments`
            The arguments of this If Game.

        append_to_reader : :class:`bool`, optional
            Whether or not this newly-created :class:`IfGame` should already be appended to the
            :class:`~py2df.reading.reader.DFReader`. Defaults to ``False`` (because it is already appended
            when :meth:`~IfGame.__enter__` is called).

        invert : :class:`bool`, optional
            If ``True`` , then this If Game's code will only execute when the condition is false (i.e., applies NOT).
            Default: ``False``

        codeblocks : Deque[:class:`~py2df.classes.abc.Block`], optional
            The blocks, including Brackets, inside this If Game. Defaults to empty deque (None).
        """
        self.action = IfGameType(action)
        self.args = args

        self.codeblocks = deque(codeblocks) if codeblocks else deque()
        self.invert = invert

        if append_to_reader:
            DFReader().append_codeblock(self)

    def __neg__(self):
        return IfGame(
            self.action, self.args, append_to_reader=False, invert=-self.invert,
            codeblocks=self.codeblocks
        )


class IfVariable(IfBlock):
    """An If Variable block. Executes code if a certain condition related to a variable is met.

    Parameters
    ----------\u200b
    action : :class:`~py2df.enums.actions.IfVariableType`
        The condition to check.

    args : :class:`~py2df.classes.collections.Arguments`
        The arguments of this If Variable.

    append_to_reader : :class:`bool`, optional
        Whether or not this newly-created :class:`IfVariable` should be already appended to the
        :class:`~py2df.reading.reader.DFReader`. Defaults to ``True``.

    invert : :class:`bool`, optional
        If ``True`` , then this If Variable's code will only execute when the condition is false (i.e., applies NOT).
        Default: ``False``

    codeblocks : Iterable[:class:`~py2df.classes.abc.Block`], optional
        The blocks, including Brackets, inside this If Variable. Defaults to empty deque (None).

    Attributes
    ----------\u200b
    block : :attr:`~py2df.enums.parameters.BlockType.IF_VAR`
        The type of this codeblock (If Variable).

    args : :class:`~py2df.classes.collections.Arguments`
        The arguments of this If Variable.

    action : :class:`~py2df.enums.actions.IfVariableType`
        The condition to check.

    codeblocks : Deque[:class:`~py2df.classes.abc.Block`]
        The blocks, including Brackets, inside this If Variable.

    invert : :class:`bool`
        If ``True`` , then this If Variable's code will only execute when the condition is false (i.e., applies NOT).
        Default: ``False``

    sub_action : ``None``
        (If Variable has no sub actions.)

    length : :class:`int`
        The length of each individual If Variable (excluding brackets). This is always equal to 1.

    data : ``None``
        (If Variable has no extra codeblock data.)

    target : ``None``
        (If Variable has no target.)
    """
    __slots__ = ("args", "action", "invert", "codeblocks", "_called_by_var")

    block: BlockType = BlockType.IF_VAR
    args: Arguments
    action: IfVariableType
    codeblocks: typing.Deque[Block]
    invert: bool
    sub_action: None = None
    length: int = 1
    data: None = None
    target: None = None

    def __init__(
        self, action: IfVariableType, args: Arguments = Arguments(),
        *, append_to_reader: bool = False, invert: bool = False, codeblocks: typing.Iterable[Block] = None
    ):
        """
        Initialize this If Variable.

        Parameters
        ----------
        action : :class:`~py2df.enums.actions.IfVariableType`
            The condition to check.

        args : :class:`~py2df.classes.collections.Arguments`
            The arguments of this If Variable.

        append_to_reader : :class:`bool`, optional
            Whether or not this newly-created :class:`IfVariable` should already be appended to the
            :class:`~py2df.reading.reader.DFReader`. Defaults to ``False`` (because it is already appended
            when :meth:`~IfVariable.__enter__` is called).

        invert : :class:`bool`, optional
            If ``True`` , then this If Variable's code will only execute when the condition is false (i.e., applies NOT).
            Default: ``False``

        codeblocks : Deque[:class:`~py2df.classes.abc.Block`], optional
            The blocks, including Brackets, inside this If Variable. Defaults to empty deque (None).
        """
        self.action = IfVariableType(action)
        self.args = args

        self.codeblocks = deque(codeblocks) if codeblocks else deque()
        self.invert = invert

        if append_to_reader:
            DFReader().append_codeblock(self)

        self._called_by_var: bool = False

    def __neg__(self):
        return IfVariable(
            self.action, self.args, append_to_reader=False, invert=-self.invert,
            codeblocks=self.codeblocks
        )

    def __bool__(self):
        """Allows for bool() calls on IfVariableType.EQUALS and IfVariableType.NOT_EQUALS, making the use of `If`s
        possible.

        Otherwise, returns True.
        """
        if self._called_by_var:
            if self.action in (IfVariableType.EQUALS, IfVariableType.NOT_EQUALS):
                arg_1 = self.args.items[0]
                arg_2 = self.args.items[1]
                res = False
                if isinstance(arg_1, DFVariable) or isinstance(arg_2, DFVariable):
                    res = arg_1.name == arg_2.name and arg_1.scope == arg_2.scope if isinstance(arg_1, DFVariable) \
                        and isinstance(arg_2, DFVariable) else False
                elif isinstance(arg_1, DFGameValue) or isinstance(arg_2, DFGameValue):
                    res = arg_1.gval_type == arg_2.gval_type if isinstance(arg_1, DFGameValue) \
                        and isinstance(arg_2, DFGameValue) else False
                else:
                    res = arg_1 == arg_2

                return not res if self.action == IfVariableType.NOT_EQUALS else res

        return True


class Else(BracketedBlock):
    """An Else block. Executes code when a condition checked by an If block is not met. **Has to be preceded by
    an If Block.

    Parameters
    ----------\u200b
    append_to_reader : :class:`bool`, optional
        Whether or not this newly-created :class:`IfVariable` should be already appended to the
        :class:`~py2df.reading.reader.DFReader`. Defaults to ``True``.

    codeblocks : Iterable[:class:`~py2df.classes.abc.Block`], optional
        The blocks, including Brackets, inside this Else. Defaults to empty deque (None).

    Attributes
    ----------\u200b
    block : :attr:`~py2df.enums.parameters.BlockType.IF_VAR`
        The type of this codeblock (Else).

    args : ``None``
        (Else has no arguments.)

    action : ``None``
        (Else has no actions.)

    codeblocks : Deque[:class:`~py2df.classes.abc.Block`]
        The blocks, including Brackets, inside this Else.

    sub_action : ``None``
        (Else has no sub actions.)

    length : :class:`int`
        The length of each individual Else (excluding brackets). This is always equal to 1.

    data : ``None``
        (Else has no extra codeblock data.)

    target : ``None``
        (Else has no target.)
        """
    __slots__ = ("codeblocks",)

    block: BlockType = BlockType.ELSE
    args: None = None
    action: None = None
    codeblocks: typing.Deque[Block]
    sub_action: None = None
    length: int = 1
    data: None = None
    target: None = None

    def __init__(
        self, *, append_to_reader: bool = False,
        codeblocks: typing.Optional[typing.Iterable[Block]] = None
    ):
        if append_to_reader:
            self._append_codeblock()

        self.codeblocks: typing.Deque[Block] = deque(codeblocks or [])

    def __enter__(self) -> "Else":
        """
        Triggers the creation of an opening bracket and the addition of all codeblocks into this If Player.

        Returns
        -------
        :class:`IfPlayer`
            self (The current instance)
        """
        self.codeblocks.appendleft(Bracket(BracketDirection.OPEN, BracketType.NORM))
        reader = DFReader()

        if reader.curr_code_loc and self not in reader.curr_code_loc:
            self._append_codeblock()

        reader.curr_code_loc = self
        return self

    def __exit__(self, _exc_type, _exc_val, _exc_tb) -> None:
        """
        Closes the Bracket, and resets the location of codeblocks (i.e., they now go outside the brackets).

        Returns
        -------
        ``None``
            ``None``
        """
        self.codeblocks.append(Bracket(BracketDirection.CLOSE, BracketType.NORM))

    def _append_codeblock(self):
        """Checks if there is an If before this Else in order to allow its placement."""
        reader = DFReader()
        curr_loc = reader.curr_code_loc
        if curr_loc and not isinstance(curr_loc[-1], IfBlock):
            raise DFSyntaxError("'Else' block must come directly after an If block at the same bracket level.")

        reader.append_codeblock(self)


remove_u200b_from_doc(IfBlock, IfPlayer, IfEntity, IfGame, IfVariable, Else)
