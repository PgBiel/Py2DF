import typing
from .. import enums
from ..enums import (
    PlayerTarget, EntityTarget, BlockType, PlayerActionType, EntityActionType, GameActionType, ControlType,
    SelectionTarget
)
from ..classes import JSONData, Arguments, ActionBlock, Tag, DFNumber
from ..utils import remove_u200b_from_doc
from ..constants import BLOCK_ID, DEFAULT_VAL
from ..reading.reader import DFReader


class PlayerAction(ActionBlock, JSONData):
    """A Player Action.

    Attributes
    ----------\u200b
    block : :attr:`~py2df.enums.parameters.BlockType.PLAYER_ACTION`
        The type of this codeblock (Player Action).

    args : :class:`~py2df.classes.collections.Arguments`
        The arguments of this Player Action.

    action : :class:`~py2df.enums.actions.PlayerActionType`
        The type of player action this is.

    sub_action : ``None``
        (Player actions have no sub actions.)

    length : :class:`int`
        The length of each individual player action. This is always equal to 2.

    data : ``None``
        (Player actions have no extra codeblock data.)

    target : :class:`~py2df.enums.targets.PlayerTarget`
        The target of this Player Action.
    """
    __slots__ = ("args", "action", "target")

    block: BlockType = BlockType.PLAYER_ACTION
    args: Arguments
    action: PlayerActionType
    sub_action: None = None
    length: int = 2
    data: None = None
    target: PlayerTarget
    
    def __init__(
        self, action: PlayerActionType, args: Arguments = Arguments(),
        target: typing.Union[PlayerTarget, SelectionTarget] = PlayerTarget.DEFAULT,
        *, append_to_reader: bool = True
    ):
        """
        Initialize this Player Action.
        
        Parameters
        ----------
        action : :class:`~py2df.enums.actions.PlayerActionType`
            The type of player action this is.
            
        args : :class:`~py2df.classes.collections.Arguments`
            The arguments of this Player Action.
        
        target : :class:`~py2df.enums.targets.PlayerTarget`, optional
            The target of this Player Action. Defaults to :attr:`~py2df.enums.targets.PlayerTarget.DEFAULT` (Default
            Player).
        
        append_to_reader : :class:`bool`, optional
            Whether or not this newly-created :class:`PlayerAction` should be already appended to the
            :class:`~py2df.reading.reader.DFReader`. Defaults to ``True``.
        """
        self.action = PlayerActionType(action)
        self.args = args
        self.target = PlayerTarget(target.value if SelectionTarget in (target, type(target)) else target)
        
        if append_to_reader:
            DFReader().append_codeblock(self)

    def as_json_data(self) -> dict:
        """
        Produces a JSON-serializable dict representing this player action.

        Returns
        -------
        :class:`dict`
        """
        return dict(
            id=BLOCK_ID,
            block=PlayerAction.block.value,
            args=self.args.as_json_data(),
            action=self.action.value,
            target=self.target.value
        )


class EntityAction(ActionBlock, JSONData):
    """An Entity Action.

    Attributes
    ----------\u200b
    block : :attr:`~py2df.enums.parameters.BlockType.ENTITY_ACTION`
        The type of this codeblock (Entity Action).

    args : :class:`~py2df.classes.collections.Arguments`
        The arguments of this Entity Action.

    action : :class:`~py2df.enums.actions.EntityActionType`
        The type of entity action this is.

    sub_action : ``None``
        (Entity actions have no sub actions.)

    length : :class:`int`
        The length of each individual entity action. This is always equal to 2.

    data : ``None``
        (Entity actions have no extra codeblock data.)

    target : :class:`~py2df.enums.targets.EntityTarget`
        The target of this Entity Action.
    """
    __slots__ = ("args", "action", "target")

    block: BlockType = BlockType.ENTITY_ACTION
    args: Arguments
    action: EntityActionType
    sub_action: None = None
    length: int = 2
    data: None = None
    target: EntityTarget

    def __init__(
        self, action: EntityActionType, args: Arguments = Arguments(),
        target: typing.Union[EntityTarget, SelectionTarget] = EntityTarget.LAST_MOB,
        *, append_to_reader: bool = True
    ):
        """
        Initialize this Entity Action.

        Parameters
        ----------
        action : :class:`~py2df.enums.actions.EntityActionType`
            The type of entity action this is.

        args : :class:`~py2df.classes.collections.Arguments`
            The arguments of this Entity Action.

        target : :class:`~py2df.enums.targets.EntityTarget`, optional
            The target of this Entity Action. Defaults to :attr:`~py2df.enums.targets.EntityTarget.LAST_MOB`.

        append_to_reader : :class:`bool`, optional
            Whether or not this newly-created :class:`EntityAction` should be already appended to the
            :class:`~py2df.reading.reader.DFReader`. Defaults to ``True``.
        """
        self.action = EntityActionType(action)
        self.args = args
        self.target = EntityTarget(target.value if SelectionTarget in (target, type(target)) else target)

        if append_to_reader:
            DFReader().append_codeblock(self)

    def as_json_data(self) -> dict:
        """
        Produces a JSON-serializable dict representing this entity action.

        Returns
        -------
        :class:`dict`
        """
        return dict(
            id=BLOCK_ID,
            block=EntityAction.block.value,
            args=self.args.as_json_data(),
            action=self.action.value,
            target=self.target.value
        )


class GameAction(ActionBlock, JSONData):
    """A Game Action.

    Attributes
    ----------\u200b
    block : :attr:`~py2df.enums.parameters.BlockType.GAME_ACTION`
        The type of this codeblock (Game Action).

    args : :class:`~py2df.classes.collections.Arguments`
        The arguments of this Game Action.

    action : :class:`~py2df.enums.actions.GameActionType`
        The type of game action this is.

    sub_action : ``None``
        (Game actions have no sub actions.)

    length : :class:`int`
        The length, in blocks, of each individual game action. This is always equal to 2.

    data : ``None``
        (Game actions have no extra codeblock data.)

    target : ``None``
        (Game actions have no target.)
    """
    __slots__ = ("args", "action")

    block: BlockType = BlockType.GAME_ACTION
    args: Arguments
    action: GameActionType
    sub_action: None = None
    length: int = 2
    data: None = None
    target: None = None

    def __init__(
        self, action: GameActionType, args: Arguments = Arguments(),
        *, append_to_reader: bool = True
    ):
        """
        Initialize this Game Action.

        Parameters
        ----------
        action : :class:`~py2df.enums.actions.GameActionType`
            The type of game action this is.

        args : :class:`~py2df.classes.collections.Arguments`
            The arguments of this Game Action.

        append_to_reader : :class:`bool`, optional
            Whether or not this newly-created :class:`GameAction` should be already appended to the
            :class:`~py2df.reading.reader.DFReader`. Defaults to ``True``.
        """
        self.action = GameActionType(action)
        self.args = args
        
        if append_to_reader:
            DFReader().append_codeblock(self)

    def as_json_data(self) -> dict:
        """
        Produces a JSON-serializable dict representing this game action.

        Returns
        -------
        :class:`dict`
        """
        return dict(
            id=BLOCK_ID,
            block=GameAction.block.value,
            args=self.args.as_json_data(),
            action=self.action.value
        )


class Control(ActionBlock, JSONData):
    """The Control block. Manages the code. See class methods for humanized methods. Example usage::

        @PlayerEvent.join
        def on_join():
            # ... do actions ...
            Control.wait(5, time_unit=CWaitTag.SECONDS)  # waits 5 seconds

    Attributes
    ----------\u200b
    block : :attr:`~py2df.enums.parameters.BlockType.ENTITY_ACTION`
        The type of this codeblock (Control).

    args : :class:`~py2df.classes.collections.Arguments`
        The arguments of this Control block.

    action : :class:`~py2df.enums.actions.ControlType`
        The type of Control block this is.

    sub_action : ``None``
        (Control blocks have no sub actions.)

    length : :class:`int`
        The length, in blocks, of each individual control blocks. This is always equal to 2.

    data : ``None``
        (Control blocks have no extra codeblock data.)

    target : ``None``
        (Control blocks have no target.)
    """
    __slots__ = ("args", "action")

    block: BlockType = BlockType.CONTROL
    args: Arguments
    action: ControlType
    sub_action: None = None
    length: int = 2
    data: None = None
    target: None = None

    def __init__(
        self, action: ControlType, args: Arguments = Arguments(),
        *, append_to_reader: bool = True
    ):
        """
        Initialize this Control block.

        Parameters
        ----------
        action : :class:`~py2df.enums.actions.ControlType`
            The type of Control block this is.

        args : :class:`~py2df.classes.collections.Arguments`
            The arguments of this Control block.

        append_to_reader : :class:`bool`, optional
            Whether or not this newly-created :class:`Control` should be already appended to the
            :class:`~py2df.reading.reader.DFReader`. Defaults to ``True``. (All classmethods will set this to ``True``)
        """
        self.action = ControlType(action)
        self.args = args

        if append_to_reader:
            DFReader().append_codeblock(self)

    def as_json_data(self) -> dict:
        """
        Produces a JSON-serializable dict representing this Control block.

        Returns
        -------
        :class:`dict`
        """
        return dict(
            id=BLOCK_ID,
            block=Control.block.value,
            args=self.args.as_json_data(),
            action=self.action.value
        )

    @classmethod
    def end(cls) -> "Control":
        """Stops reading all code after the control block.

        Returns
        -------
        :class:`Control`
            The generated :class:`Control` block.
        """
        return Control(ControlType.END, append_to_reader=True)

    @classmethod
    def line_return(cls) -> "Control":
        """Returns to the Call Function block the current Function was called from, and continues code from there.

        Returns
        -------
        :class:`Control`
            The generated :class:`Control` block.
        """
        return Control(ControlType.RETURN, append_to_reader=True)

    @classmethod
    def skip(cls) -> "Control":
        """Skips the rest of this repeat statement's code and continues to the next repetition.

        Returns
        -------
        :class:`Control`
            The generated :class:`Control` block.
        """
        return Control(ControlType.SKIP, append_to_reader=True)

    @classmethod
    def stop_repeat(cls) -> "Control":
        """Stops a repeating sequence and continues to the next code block.

        Returns
        -------
        :class:`Control`
            The generated :class:`Control` block.
        """
        return Control(ControlType.STOP_REPEAT, append_to_reader=True)

    @classmethod
    def wait(
            cls, duration: typing.Union[int, float, DFNumber] = DEFAULT_VAL,
            *, time_unit: enums.CWaitTag = enums.CWaitTag.TICKS
    ) -> "Control":
        """Pauses the current line of code for a certain amount of ticks. seconds, or minutes.

        Parameters
        ----------
        duration : Union[:class:`int`, :class:`float`, :class:`~py2df.classes.mc_types.DFNumber`]
            The duration of time to wait for, according to the time unit specified in the ``time_unit`` param.
            Defaults to ``1``

        time_unit : :class:`~py2df.enums.actions.CWaitTag`
            The time unit that the duration was specified in. Defaults to :attr:`~py2df.enums.actions.CWaitTag.TICKS`.

        Returns
        -------
        :class:`Control`
            The generated :class:`Control` block.
        """
        return Control(
            ControlType.WAIT,
            Arguments(
                items=[DFNumber(duration)] if duration != DEFAULT_VAL else None,
                tags=[Tag("Time Unit", option=enums.CWaitTag(time_unit), action=ControlType.WAIT, block=cls.block)]
            ),
            append_to_reader=True
        )


remove_u200b_from_doc((PlayerAction, EntityAction, GameAction, Control))
