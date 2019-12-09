"""
Events and their decorators.
"""
import typing
from .reader import DFReader
from ..classes import FunctionHolder, Codeblock, JSONData
from ..enums import PlayerEventType, EntityEventType, BlockType
from ..utils import remove_u200b_from_doc
from ..constants import BLOCK_ID, EMPTY_ARGS


class PlayerEvent(FunctionHolder, Codeblock, JSONData):
    """
    Describes a Player Event on DiamondFire. Implements :class:`~py2df.classes.abc.Codeblock` and
    :class:`~py2df.classes.abc.FunctionHolder`.

    Check out this class's classmethods for the decorators.

    Example usage::

        @PlayerEvent.join
        def on_join(self):
            ...

    In that example, all DF-relevant code inside ``on_join`` will be executed whenever a player joins the plot.

    Attributes
    ----------\u200b
        block : :attr:`~py2df.enums.parameters.BlockType.PLAYER_EVENT`
            Constant class var; type of event.

        args : ``None``
            There are no arguments to be passed to an event, so this will always remain as None.

        action : :class:`~py2df.enums.events.PlayerEventType`
            The kind of Player Event this is.

        length : :class:`int`
            The space, in Minecraft blocks, that this codeblock occupies. For a Player Event, this is equal to ``2``.

        function : :class:`Callable`
            The function representing the line of code that is preceded by this Player Event block.
    """
    __slots__ = ("args", "action", "function")

    block: BlockType = BlockType.PLAYER_EVENT

    length: int = 2

    args: None

    action: PlayerEventType

    data: None = None

    function: typing.Optional[typing.Callable]

    sub_action: None = None
    target: None = None

    def __init__(
        self, action: PlayerEventType, func: typing.Optional[typing.Callable] = None,
        append_to_reader: bool = False
    ):
        """
        Initialize the Player Event.

        Parameters
        ----------
        action : :class:`~py2df.enums.events.PlayerEventType`
            The kind of Player Event this is.

        func : :class:`Callable`
            The function that contains the code that will be executed when this event is triggered.

        append_to_reader : :class:`bool`
            Whether or not should already add this event as one of the :class:`DFReader` singleton's function holders.
            Defaults to ``False``; this will always be ``True`` when using decorators.
        """
        self.action = PlayerEventType(action)

        if not callable(func):
            raise TypeError("'func' parameter must be a callable (preferably, a function).")

        self.function = func
        self.args = None
        if append_to_reader:
            DFReader().append_function(typing.cast(FunctionHolder, self))

    def as_json_data(self) -> dict:
        """
        Obtains a valid json-serializable :class:`dict` representing this player event.

        Returns
        -------
        :class:`dict`
            A valid JSON-serializable dict.
        """
        return dict(
            id=BLOCK_ID,
            block=PlayerEvent.block.value,
            args=EMPTY_ARGS,
            action=self.action.value
        )

    @classmethod
    def from_json_data(cls, data: dict) -> "PlayerEvent":
        """
        Obtains a :class:`PlayerEvent` instance from valid, **pre-parsed** JSON dict, with the following structure
        (at least the following key and value)::

            { "action": str }

        where ``str`` is a valid **value** (not attr) of :class:`~py2df.enums.events.PlayerEventType`.

        Parameters
        ----------
        data : :class:`dict`
            Already parsed JSON dict containing valid Player Event data.

        Returns
        -------
        :class:`PlayerEvent`
            The corresponding Player Event instance.

        Raises
        ------
        :exc:`TypeError`
            If the data dict provided is malformed (does not follow the given structure).
        """
        if (
            not isinstance(data, dict)
            # or "id" not in data  # not really required
            or "action" not in data
            or not type(data["action"]) == str
            or not data["action"] in PlayerEventType.__members__
        ):
            raise TypeError(
                "Malformed PlayerEvent parsed JSON data! Must be a dict with, at least, an 'action' str value that is a"
                "valid 'PlayerEventType' value."
            )

        return cls(PlayerEventType(data["action"]))

    # region:PlayerEvent_methods

    @classmethod
    def break_block(cls, func: typing.Callable) -> "PlayerEvent":
        """Executes code when a player breaks a block. Decorator.

        Parameters
        ----------
        func : :class:`Callable`
            Function containing the code to be run when this event is triggered.

        Returns
        -------
        :class:`PlayerEvent`
            The corresponding :class:`PlayerEvent` instance object.
        """

        return cls(PlayerEventType.BREAK_BLOCK, func, append_to_reader=True)

    @classmethod
    def break_item(cls, func: typing.Callable) -> "PlayerEvent":
        """Executes code when a player breaks an item. Decorator.

        Parameters
        ----------
        func : :class:`Callable`
            Function containing the code to be run when this event is triggered.

        Returns
        -------
        :class:`PlayerEvent`
            The corresponding :class:`PlayerEvent` instance object.
        """

        return cls(PlayerEventType.BREAK_ITEM, func, append_to_reader=True)

    @classmethod
    def change_slot(cls, func: typing.Callable) -> "PlayerEvent":
        """Executes code when a player changes their hotbar slot. Decorator.

        Parameters
        ----------
        func : :class:`Callable`
            Function containing the code to be run when this event is triggered.

        Returns
        -------
        :class:`PlayerEvent`
            The corresponding :class:`PlayerEvent` instance object.
        """

        return cls(PlayerEventType.CHANGE_SLOT, func, append_to_reader=True)

    @classmethod
    def click_entity(cls, func: typing.Callable) -> "PlayerEvent":
        """Executes code when a player right clicks an entity. Decorator.

        Parameters
        ----------
        func : :class:`Callable`
            Function containing the code to be run when this event is triggered.

        Returns
        -------
        :class:`PlayerEvent`
            The corresponding :class:`PlayerEvent` instance object.
        """

        return cls(PlayerEventType.CLICK_ENTITY, func, append_to_reader=True)

    @classmethod
    def click_item(cls, func: typing.Callable) -> "PlayerEvent":
        """Executes code when a player clicks an item in an inventory menu. Decorator.

        Parameters
        ----------
        func : :class:`Callable`
            Function containing the code to be run when this event is triggered.

        Returns
        -------
        :class:`PlayerEvent`
            The corresponding :class:`PlayerEvent` instance object.
        """

        return cls(PlayerEventType.CLICK_ITEM, func, append_to_reader=True)

    @classmethod
    def click_own_inv(cls, func: typing.Callable) -> "PlayerEvent":
        """Executes code when a player clicks an item inside their inventory. Decorator.

        Parameters
        ----------
        func : :class:`Callable`
            Function containing the code to be run when this event is triggered.

        Returns
        -------
        :class:`PlayerEvent`
            The corresponding :class:`PlayerEvent` instance object.
        """

        return cls(PlayerEventType.CLICK_OWN_INV, func, append_to_reader=True)

    @classmethod
    def click_player(cls, func: typing.Callable) -> "PlayerEvent":
        """Executes code when a player clicks another player. Decorator.

        Parameters
        ----------
        func : :class:`Callable`
            Function containing the code to be run when this event is triggered.

        Returns
        -------
        :class:`PlayerEvent`
            The corresponding :class:`PlayerEvent` instance object.
        """

        return cls(PlayerEventType.CLICK_PLAYER, func, append_to_reader=True)

    @classmethod
    def close_inv(cls, func: typing.Callable) -> "PlayerEvent":
        """Executes code when a player closes an inventory. Decorator.

        Parameters
        ----------
        func : :class:`Callable`
            Function containing the code to be run when this event is triggered.

        Returns
        -------
        :class:`PlayerEvent`
            The corresponding :class:`PlayerEvent` instance object.
        """

        return cls(PlayerEventType.CLOSE_INV, func, append_to_reader=True)

    @classmethod
    def command(cls, func: typing.Callable) -> "PlayerEvent":
        """Executes code when a player types a command on the plot. Decorator.

        Parameters
        ----------
        func : :class:`Callable`
            Function containing the code to be run when this event is triggered.

        Returns
        -------
        :class:`PlayerEvent`
            The corresponding :class:`PlayerEvent` instance object.
        """

        return cls(PlayerEventType.COMMAND, func, append_to_reader=True)

    @classmethod
    def consume(cls, func: typing.Callable) -> "PlayerEvent":
        """Executes code when a player eats or drinks an item. Decorator.

        Parameters
        ----------
        func : :class:`Callable`
            Function containing the code to be run when this event is triggered.

        Returns
        -------
        :class:`PlayerEvent`
            The corresponding :class:`PlayerEvent` instance object.
        """

        return cls(PlayerEventType.CONSUME, func, append_to_reader=True)

    @classmethod
    def damage_entity(cls, func: typing.Callable) -> "PlayerEvent":
        """Executes code when a player damages an entity. Decorator.

        Parameters
        ----------
        func : :class:`Callable`
            Function containing the code to be run when this event is triggered.

        Returns
        -------
        :class:`PlayerEvent`
            The corresponding :class:`PlayerEvent` instance object.
        """

        return cls(PlayerEventType.DAMAGE_ENTITY, func, append_to_reader=True)

    @classmethod
    def death(cls, func: typing.Callable) -> "PlayerEvent":
        """Executes code when a player dies, not as a result of another player or entity. Decorator.

        Parameters
        ----------
        func : :class:`Callable`
            Function containing the code to be run when this event is triggered.

        Returns
        -------
        :class:`PlayerEvent`
            The corresponding :class:`PlayerEvent` instance object.
        """

        return cls(PlayerEventType.DEATH, func, append_to_reader=True)

    @classmethod
    def dismount(cls, func: typing.Callable) -> "PlayerEvent":
        """Executes code when a player dismounts a vehicle or other entity. Decorator.

        Parameters
        ----------
        func : :class:`Callable`
            Function containing the code to be run when this event is triggered.

        Returns
        -------
        :class:`PlayerEvent`
            The corresponding :class:`PlayerEvent` instance object.
        """

        return cls(PlayerEventType.DISMOUNT, func, append_to_reader=True)

    @classmethod
    def drop_item(cls, func: typing.Callable) -> "PlayerEvent":
        """Executes code when a player drops an item. Decorator.

        Parameters
        ----------
        func : :class:`Callable`
            Function containing the code to be run when this event is triggered.

        Returns
        -------
        :class:`PlayerEvent`
            The corresponding :class:`PlayerEvent` instance object.
        """

        return cls(PlayerEventType.DROP_ITEM, func, append_to_reader=True)

    @classmethod
    def entity_dmg_player(cls, func: typing.Callable) -> "PlayerEvent":
        """Executes code when an entity damages a player. Decorator.

        Parameters
        ----------
        func : :class:`Callable`
            Function containing the code to be run when this event is triggered.

        Returns
        -------
        :class:`PlayerEvent`
            The corresponding :class:`PlayerEvent` instance object.
        """

        return cls(PlayerEventType.ENTITY_DMG_PLAYER, func, append_to_reader=True)

    @classmethod
    def fall_damage(cls, func: typing.Callable) -> "PlayerEvent":
        """"Decorator.

        Parameters
        ----------
        func : :class:`Callable`
            Function containing the code to be run when this event is triggered.

        Returns
        -------
        :class:`PlayerEvent`
            The corresponding :class:`PlayerEvent` instance object.
        """

        return cls(PlayerEventType.FALL_DAMAGE, func, append_to_reader=True)

    @classmethod
    def join(cls, func: typing.Callable) -> "PlayerEvent":
        """Executes code when a player joins the plot. Decorator.

        Parameters
        ----------
        func : :class:`Callable`
            Function containing the code to be run when this event is triggered.

        Returns
        -------
        :class:`PlayerEvent`
            The corresponding :class:`PlayerEvent` instance object.
        """

        return cls(PlayerEventType.JOIN, func, append_to_reader=True)

    @classmethod
    def jump(cls, func: typing.Callable) -> "PlayerEvent":
        """Executes code when a player jumps. Decorator.

        Parameters
        ----------
        func : :class:`Callable`
            Function containing the code to be run when this event is triggered.

        Returns
        -------
        :class:`PlayerEvent`
            The corresponding :class:`PlayerEvent` instance object.
        """

        return cls(PlayerEventType.JUMP, func, append_to_reader=True)

    @classmethod
    def kill_mob(cls, func: typing.Callable) -> "PlayerEvent":
        """Executes code when a player kills a mob. Decorator.

        Parameters
        ----------
        func : :class:`Callable`
            Function containing the code to be run when this event is triggered.

        Returns
        -------
        :class:`PlayerEvent`
            The corresponding :class:`PlayerEvent` instance object.
        """

        return cls(PlayerEventType.KILL_MOB, func, append_to_reader=True)

    @classmethod
    def kill_player(cls, func: typing.Callable) -> "PlayerEvent":
        """Executes code when a player kills another player. Decorator.

        Parameters
        ----------
        func : :class:`Callable`
            Function containing the code to be run when this event is triggered.

        Returns
        -------
        :class:`PlayerEvent`
            The corresponding :class:`PlayerEvent` instance object.
        """

        return cls(PlayerEventType.KILL_PLAYER, func, append_to_reader=True)

    @classmethod
    def left_click(cls, func: typing.Callable) -> "PlayerEvent":
        """Executes code when a player left clicks. Decorator.

        Parameters
        ----------
        func : :class:`Callable`
            Function containing the code to be run when this event is triggered.

        Returns
        -------
        :class:`PlayerEvent`
            The corresponding :class:`PlayerEvent` instance object.
        """

        return cls(PlayerEventType.LEFT_CLICK, func, append_to_reader=True)

    @classmethod
    def mob_kill_player(cls, func: typing.Callable) -> "PlayerEvent":
        """Executes code when a mob kills a player. Decorator.

        Parameters
        ----------
        func : :class:`Callable`
            Function containing the code to be run when this event is triggered.

        Returns
        -------
        :class:`PlayerEvent`
            The corresponding :class:`PlayerEvent` instance object.
        """

        return cls(PlayerEventType.MOB_KILL_PLAYER, func, append_to_reader=True)

    @classmethod
    def pickup_item(cls, func: typing.Callable) -> "PlayerEvent":
        """Executes code when a player picks up an item. Decorator.

        Parameters
        ----------
        func : :class:`Callable`
            Function containing the code to be run when this event is triggered.

        Returns
        -------
        :class:`PlayerEvent`
            The corresponding :class:`PlayerEvent` instance object.
        """

        return cls(PlayerEventType.PICKUP_ITEM, func, append_to_reader=True)

    @classmethod
    def place_block(cls, func: typing.Callable) -> "PlayerEvent":
        """Executes code when a player places a block. Decorator.

        Parameters
        ----------
        func : :class:`Callable`
            Function containing the code to be run when this event is triggered.

        Returns
        -------
        :class:`PlayerEvent`
            The corresponding :class:`PlayerEvent` instance object.
        """

        return cls(PlayerEventType.PLACE_BLOCK, func, append_to_reader=True)

    @classmethod
    def player_dmg_player(cls, func: typing.Callable) -> "PlayerEvent":
        """Executes code when a player damages another player. Decorator.

        Parameters
        ----------
        func : :class:`Callable`
            Function containing the code to be run when this event is triggered.

        Returns
        -------
        :class:`PlayerEvent`
            The corresponding :class:`PlayerEvent` instance object.
        """

        return cls(PlayerEventType.PLAYER_DMG_PLAYER, func, append_to_reader=True)

    @classmethod
    def player_take_dmg(cls, func: typing.Callable) -> "PlayerEvent":
        """Executes code when a player takes damage. Decorator.

        Parameters
        ----------
        func : :class:`Callable`
            Function containing the code to be run when this event is triggered.

        Returns
        -------
        :class:`PlayerEvent`
            The corresponding :class:`PlayerEvent` instance object.
        """

        return cls(PlayerEventType.PLAYER_TAKE_DMG, func, append_to_reader=True)

    @classmethod
    def proj_dmg_player(cls, func: typing.Callable) -> "PlayerEvent":
        """Executes code when a projectile damages a player. Decorator.

        Parameters
        ----------
        func : :class:`Callable`
            Function containing the code to be run when this event is triggered.

        Returns
        -------
        :class:`PlayerEvent`
            The corresponding :class:`PlayerEvent` instance object.
        """

        return cls(PlayerEventType.PROJ_DMG_PLAYER, func, append_to_reader=True)

    @classmethod
    def proj_hit(cls, func: typing.Callable) -> "PlayerEvent":
        """Executes code when a projectile launched by a player hits a block/an entity/another player. Decorator.

        Parameters
        ----------
        func : :class:`Callable`
            Function containing the code to be run when this event is triggered.

        Returns
        -------
        :class:`PlayerEvent`
            The corresponding :class:`PlayerEvent` instance object.
        """

        return cls(PlayerEventType.PROJ_HIT, func, append_to_reader=True)

    @classmethod
    def quit(cls, func: typing.Callable) -> "PlayerEvent":
        """Executes code when a player leaves the plot. Decorator.

        Parameters
        ----------
        func : :class:`Callable`
            Function containing the code to be run when this event is triggered.

        Returns
        -------
        :class:`PlayerEvent`
            The corresponding :class:`PlayerEvent` instance object.
        """

        return cls(PlayerEventType.QUIT, func, append_to_reader=True)

    @classmethod
    def respawn(cls, func: typing.Callable) -> "PlayerEvent":
        """Executes code when a player respawns. Decorator.

        Parameters
        ----------
        func : :class:`Callable`
            Function containing the code to be run when this event is triggered.

        Returns
        -------
        :class:`PlayerEvent`
            The corresponding :class:`PlayerEvent` instance object.
        """

        return cls(PlayerEventType.RESPAWN, func, append_to_reader=True)

    @classmethod
    def right_click(cls, func: typing.Callable) -> "PlayerEvent":
        """Executes code when a player right clicks while looking at a block or holding an item. Decorator.

        Parameters
        ----------
        func : :class:`Callable`
            Function containing the code to be run when this event is triggered.

        Returns
        -------
        :class:`PlayerEvent`
            The corresponding :class:`PlayerEvent` instance object.
        """

        return cls(PlayerEventType.RIGHT_CLICK, func, append_to_reader=True)

    @classmethod
    def riptide(cls, func: typing.Callable) -> "PlayerEvent":
        """Executes code when a player throws a riptide trident. Decorator.

        Parameters
        ----------
        func : :class:`Callable`
            Function containing the code to be run when this event is triggered.

        Returns
        -------
        :class:`PlayerEvent`
            The corresponding :class:`PlayerEvent` instance object.
        """

        return cls(PlayerEventType.RIPTIDE, func, append_to_reader=True)

    @classmethod
    def shoot_bow(cls, func: typing.Callable) -> "PlayerEvent":
        """Executes code when a player fires an arrow with a bow. Decorator.

        Parameters
        ----------
        func : :class:`Callable`
            Function containing the code to be run when this event is triggered.

        Returns
        -------
        :class:`PlayerEvent`
            The corresponding :class:`PlayerEvent` instance object.
        """

        return cls(PlayerEventType.SHOOT_BOW, func, append_to_reader=True)

    @classmethod
    def sneak(cls, func: typing.Callable) -> "PlayerEvent":
        """Executes code when a player sneaks. Decorator.

        Parameters
        ----------
        func : :class:`Callable`
            Function containing the code to be run when this event is triggered.

        Returns
        -------
        :class:`PlayerEvent`
            The corresponding :class:`PlayerEvent` instance object.
        """

        return cls(PlayerEventType.SNEAK, func, append_to_reader=True)

    @classmethod
    def start_fly(cls, func: typing.Callable) -> "PlayerEvent":
        """Executes code when a player starts flying. Decorator.

        Parameters
        ----------
        func : :class:`Callable`
            Function containing the code to be run when this event is triggered.

        Returns
        -------
        :class:`PlayerEvent`
            The corresponding :class:`PlayerEvent` instance object.
        """

        return cls(PlayerEventType.START_FLY, func, append_to_reader=True)

    @classmethod
    def start_sprint(cls, func: typing.Callable) -> "PlayerEvent":
        """Executes code when a player starts sprinting. Decorator.

        Parameters
        ----------
        func : :class:`Callable`
            Function containing the code to be run when this event is triggered.

        Returns
        -------
        :class:`PlayerEvent`
            The corresponding :class:`PlayerEvent` instance object.
        """

        return cls(PlayerEventType.START_SPRINT, func, append_to_reader=True)

    @classmethod
    def stop_fly(cls, func: typing.Callable) -> "PlayerEvent":
        """Executes code when a player stops flying. Decorator.

        Parameters
        ----------
        func : :class:`Callable`
            Function containing the code to be run when this event is triggered.

        Returns
        -------
        :class:`PlayerEvent`
            The corresponding :class:`PlayerEvent` instance object.
        """

        return cls(PlayerEventType.STOP_FLY, func, append_to_reader=True)

    @classmethod
    def stop_sprint(cls, func: typing.Callable) -> "PlayerEvent":
        """Executes code when a player stops sprinting. Decorator.

        Parameters
        ----------
        func : :class:`Callable`
            Function containing the code to be run when this event is triggered.

        Returns
        -------
        :class:`PlayerEvent`
            The corresponding :class:`PlayerEvent` instance object.
        """

        return cls(PlayerEventType.STOP_SPRINT, func, append_to_reader=True)

    @classmethod
    def swap_hands(cls, func: typing.Callable) -> "PlayerEvent":
        """Executes code when a player swaps an item or items between their main hand and off hand. Decorator.

        Parameters
        ----------
        func : :class:`Callable`
            Function containing the code to be run when this event is triggered.

        Returns
        -------
        :class:`PlayerEvent`
            The corresponding :class:`PlayerEvent` instance object.
        """

        return cls(PlayerEventType.SWAP_HANDS, func, append_to_reader=True)

    @classmethod
    def unsneak(cls, func: typing.Callable) -> "PlayerEvent":
        """Executes code when a player stops sneaking. Decorator.

        Parameters
        ----------
        func : :class:`Callable`
            Function containing the code to be run when this event is triggered.

        Returns
        -------
        :class:`PlayerEvent`
            The corresponding :class:`PlayerEvent` instance object.
        """

        return cls(PlayerEventType.UNSNEAK, func, append_to_reader=True)

    @classmethod
    def walk(cls, func: typing.Callable) -> "PlayerEvent":
        """Executes code while a player is walking. Decorator.

        Parameters
        ----------
        func : :class:`Callable`
            Function containing the code to be run when this event is triggered.

        Returns
        -------
        :class:`PlayerEvent`
            The corresponding :class:`PlayerEvent` instance object.
        """

        return cls(PlayerEventType.WALK, func, append_to_reader=True)

    # endregion:PlayerEvent_methods


class EntityEvent(FunctionHolder):
    """
    Describes an Entity Event on DiamondFire. Implements :class:`~py2df.classes.abc.Codeblock` and
    :class:`~py2df.classes.abc.FunctionHolder`.

    Check out this class's classmethods for the decorators.

    Example usage::

        @EntityEvent.entity_death
        def on_entity_death(self):
            ...

    In that example, all DF-relevant code inside ``on_entity_death`` will be executed whenever an entity dies in the
    plot.

    Attributes
    ----------\u200b
        block : :attr:`~py2df.enums.parameters.BlockType.ENTITY_EVENT`
            Constant class var; type of event.

        args : ``None``
            There are no arguments to be passed to an event, so this will always remain as None.

        action : :class:`~py2df.enums.events.EntityEventType`
            The kind of Entity Event this is.

        length : :class:`int`
            The space, in Minecraft blocks, that this codeblock occupies. For an Entity Event, this is equal to ``2``.

        function : :class:`Callable`
            The function representing the line of code that is preceded by this Entity Event block.
    """
    __slots__ = ("args", "action", "function")

    block: BlockType = BlockType.ENTITY_EVENT

    length: int = 2

    args: None

    action: EntityEventType

    data: None = None

    function: typing.Optional[typing.Callable]

    sub_action: None = None
    target: None = None

    def __init__(
        self, action: EntityEventType, func: typing.Optional[typing.Callable] = None,
        append_to_reader: bool = False
    ):
        """
        Initialize the Entity Event.

        Parameters
        ----------
        action : :class:`~py2df.enums.events.EntityEventType`
            The kind of Entity Event this is.

        func : :class:`Callable`
            The function that contains the code that will be executed when this event is triggered.

        append_to_reader : :class:`bool`
            Whether or not should already add, on ``__init__``, this event as one of the :class:`DFReader`
            singleton's function holders. Defaults to ``False``; this will always be ``True`` when using decorators.
        """
        self.action = EntityEventType(action)

        if not callable(func):
            raise TypeError("'func' parameter must be a callable (preferably, a function).")

        self.function = func
        self.args = None
        if append_to_reader:
            DFReader().append_function(typing.cast(FunctionHolder, self))

    def as_json_data(self) -> dict:
        """
        Obtains a valid json-serializable :class:`dict` representing this entity event.

        Returns
        -------
        :class:`dict`
            A valid JSON-serializable dict.
        """
        return dict(
            id=BLOCK_ID,
            block=EntityEvent.block.value,
            args=EMPTY_ARGS,
            action=self.action.value
        )

    @classmethod
    def from_json_data(cls, data: dict) -> "EntityEvent":
        """
        Obtains a :class:`EntityEvent` instance from valid, **pre-parsed** JSON dict, with the following structure
        (at least the following key and value)::

            { "action": str }

        where ``str`` is a valid **value** (not attr) of :class:`~py2df.enums.events.EntityEventType`.

        Parameters
        ----------
        data : :class:`dict`
            Already parsed JSON dict containing valid Entity Event data.

        Returns
        -------
        :class:`EntityEvent`
            The corresponding Entity Event instance.

        Raises
        ------
        :exc:`TypeError`
            If the data dict provided is malformed (does not follow the given structure).
        """
        if (
                not isinstance(data, dict)
                # or "id" not in data  # not really required
                or "action" not in data
                or not type(data["action"]) == str
                or not data["action"] in EntityEventType.__members__
        ):
            raise TypeError(
                "Malformed EntityEvent parsed JSON data! Must be a dict with, at least, an 'action' str value that is a"
                "valid 'EntityEventType' value."
            )

        return cls(EntityEventType(data["action"]))

    # region:EntityEvent_methods

    @classmethod
    def block_fall(cls, func: typing.Callable) -> "EntityEvent":
        """Executes code when a block affected by gravity turns into a falling block. Decorator.

        Parameters
        ----------
        func : :class:`Callable`
            Function containing the code to be run when this event is triggered.

        Returns
        -------
        :class:`EntityEvent`
            The corresponding :class:`EntityEvent` instance object.
        """
        return cls(EntityEventType.BLOCK_FALL, func, append_to_reader=True)

    @classmethod
    def entity_death(cls, func: typing.Callable) -> "EntityEvent":
        """Executes code when an entity dies by natural causes. Decorator.

        Parameters
        ----------
        func : :class:`Callable`
            Function containing the code to be run when this event is triggered.

        Returns
        -------
        :class:`EntityEvent`
            The corresponding :class:`EntityEvent` instance object.
        """
        return cls(EntityEventType.ENTITY_DEATH, func, append_to_reader=True)

    @classmethod
    def entity_dmg(cls, func: typing.Callable) -> "EntityEvent":
        """Executes code when an entity takes damage. Decorator.

        Parameters
        ----------
        func : :class:`Callable`
            Function containing the code to be run when this event is triggered.

        Returns
        -------
        :class:`EntityEvent`
            The corresponding :class:`EntityEvent` instance object.
        """
        return cls(EntityEventType.ENTITY_DMG, func, append_to_reader=True)

    @classmethod
    def entity_dmg_entity(cls, func: typing.Callable) -> "EntityEvent":
        """Executes code when an entity damages another entity. Decorator.

        Parameters
        ----------
        func : :class:`Callable`
            Function containing the code to be run when this event is triggered.

        Returns
        -------
        :class:`EntityEvent`
            The corresponding :class:`EntityEvent` instance object.
        """
        return cls(EntityEventType.ENTITY_DMG_ENTITY, func, append_to_reader=True)

    @classmethod
    def entity_kill_entity(cls, func: typing.Callable) -> "EntityEvent":
        """Executes code when an entity kills another entity. Decorator.

        Parameters
        ----------
        func : :class:`Callable`
            Function containing the code to be run when this event is triggered.

        Returns
        -------
        :class:`EntityEvent`
            The corresponding :class:`EntityEvent` instance object.
        """
        return cls(EntityEventType.ENTITY_KILL_ENTITY, func, append_to_reader=True)

    @classmethod
    def falling_block_land(cls, func: typing.Callable) -> "EntityEvent":
        """Executes code when a falling block lands on the ground. Decorator.

        Parameters
        ----------
        func : :class:`Callable`
            Function containing the code to be run when this event is triggered.

        Returns
        -------
        :class:`EntityEvent`
            The corresponding :class:`EntityEvent` instance object.
        """
        return cls(EntityEventType.FALLING_BLOCK_LAND, func, append_to_reader=True)

    @classmethod
    def proj_dmg_entity(cls, func: typing.Callable) -> "EntityEvent":
        """Executes code when a projectile damages an entity. Decorator.

        Parameters
        ----------
        func : :class:`Callable`
            Function containing the code to be run when this event is triggered.

        Returns
        -------
        :class:`EntityEvent`
            The corresponding :class:`EntityEvent` instance object.
        """
        return cls(EntityEventType.PROJ_DMG_ENTITY, func, append_to_reader=True)

    @classmethod
    def proj_kill_entity(cls, func: typing.Callable) -> "EntityEvent":
        """Executes code when a projectile kills an entity. Decorator.

        Parameters
        ----------
        func : :class:`Callable`
            Function containing the code to be run when this event is triggered.

        Returns
        -------
        :class:`EntityEvent`
            The corresponding :class:`EntityEvent` instance object.
        """
        return cls(EntityEventType.PROJ_KILL_ENTITY, func, append_to_reader=True)

    @classmethod
    def vehicle_damage(cls, func: typing.Callable) -> "EntityEvent":
        """Executes code when a vehicle entity (minecart or boat) is damaged. Decorator.

        Parameters
        ----------
        func : :class:`Callable`
            Function containing the code to be run when this event is triggered.

        Returns
        -------
        :class:`EntityEvent`
            The corresponding :class:`EntityEvent` instance object.
        """
        return cls(EntityEventType.VEHICLE_DAMAGE, func, append_to_reader=True)

    # endregion:EntityEvent_methods


remove_u200b_from_doc((PlayerEvent, EntityEvent))
