import collections
import typing
from .. import enums
from ..enums import (
    PlayerTarget, EntityTarget, BlockType, PlayerActionType, EntityActionType, GameActionType, ControlType,
    SelectionTarget,
    Material)
from ..classes import JSONData, Arguments, ActionBlock, Tag, DFNumber, DFVariable, DFText
from ..utils import remove_u200b_from_doc
from ..typings import p_check, Numeric, Locatable, Textable, ParticleParam
from ..constants import BLOCK_ID, DEFAULT_VAL
from ..reading.reader import DFReader


class PlayerAction(ActionBlock, JSONData):
    """A Player Action.

    Parameters
    ----------\u200b
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

    Parameters
    ----------\u200b
    action : :class:`~py2df.enums.actions.EntityActionType`
        The type of entity action this is.

    args : :class:`~py2df.classes.collections.Arguments`
        The arguments of this Entity Action.

    target : :class:`~py2df.enums.targets.EntityTarget`, optional
        The target of this Entity Action. Defaults to :attr:`~py2df.enums.targets.EntityTarget.LAST_MOB`.

    append_to_reader : :class:`bool`, optional
        Whether or not this newly-created :class:`EntityAction` should be already appended to the
        :class:`~py2df.reading.reader.DFReader`. Defaults to ``True``.

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

    Parameters
    ----------\u200b
    action : :class:`~py2df.enums.actions.GameActionType`
        The type of game action this is.

    args : :class:`~py2df.classes.collections.Arguments`
        The arguments of this Game Action.

    append_to_reader : :class:`bool`, optional
        Whether or not this newly-created :class:`GameAction` should be already appended to the
        :class:`~py2df.reading.reader.DFReader`. Defaults to ``True``.

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

    # region:humanized-gameaction

    @classmethod  # TODO: Finish game actions
    def block_drops_off(cls) -> "GameAction":
        """Disables blocks dropping as items when broken.

        Returns
        -------
        :class:`GameAction`
            The generated Game Action codeblock.

        Examples
        --------
        ::

            GameAction.blocks_drops_off()
        """
        return GameAction(
            action=GameActionType.BLOCK_DROPS_OFF,
            args=Arguments(),
            append_to_reader=True
        )

    @classmethod
    def block_drops_on(cls) -> "GameAction":
        """Enables blocks dropping as items when broken.

        Returns
        -------
        :class:`GameAction`
            The generated Game Action codeblock.

        Examples
        --------
        ::

            GameAction.blocks_drops_on()
        """
        return GameAction(
            action=GameActionType.BLOCK_DROPS_ON,
            args=Arguments(),
            append_to_reader=True
        )

    @classmethod  # TODO: Tag default values
    def bone_meal(cls, *locs: Locatable, amount: Numeric, show_particles: bool = False) -> "GameAction":
        """Applies bone meal to a block.

        Parameters
        ----------
        locs : :attr:`~.Locatable`
            The location(s) of the block(s) that will receive the Bone Meal.

        amount : :attr:`~.Numeric`
            The amount of bone meals to apply at once to the blocks.

        show_particles : :class:`bool`, optional
            Whether or not Bone Meal particles should be shown when applied. Defaults to ``False``

        Returns
        -------
        :class:`GameAction`
            The generated Game Action codeblock.

        Examples
        --------
        ::

            loc_1 = DFLocation(1, 2, 3)
            loc_2 = DFVariable("my_loc")
            GameAction.bone_meal(loc_1, loc_2, amount=5, show_particles=True)  # 5 bone meals, with particles.
        """
        args = Arguments(
            [
                *[p_check(loc, Locatable, f"locs[{i}]") for i, loc in enumerate(locs)],
                p_check(amount, Numeric, "amount")
            ],
            tags=[Tag(
                "Show Particles", option=bool(show_particles),
                action=GameActionType.BONE_MEAL, block=BlockType.GAME_ACTION
            )]
        )
        return GameAction(
            action=GameActionType.BONE_MEAL,
            args=args,
            append_to_reader=True
        )

    @classmethod
    def break_block(cls, *locs: Locatable) -> "GameAction":
        """Breaks a block at a certain location as if it was broken by a player.

        Parameters
        ----------
        locs : :attr:`~.Locatable`
            The location(s) of the block(s) that will be broken.

        Returns
        -------
        :class:`GameAction`
            The generated Game Action codeblock.
        """
        return GameAction(
            action=GameActionType.BREAK_BLOCK,
            args=Arguments([p_check(loc, Locatable, f"locs[{i}]") for i, loc in enumerate(locs)]),
            append_to_reader=True
        )

    @classmethod
    def cancel_event(cls) -> "GameAction":
        """Cancels the initial event that triggered this line of code.

        Returns
        -------
        :class:`GameAction`
            The generated Game Action codeblock.

        Examples
        --------
        ::

            GameAction.cancel_event()
        """
        return GameAction(
            action=GameActionType.CANCEL_EVENT,
            args=Arguments(),
            append_to_reader=True
        )

    @classmethod
    def change_sign(cls, loc: Locatable, line: Numeric, new_text: typing.Optional[Textable] = None) -> "GameAction":
        """Changes a line of text on a sign.

        Parameters
        ----------
        loc : :attr:`~.Locatable`
            The location of the sign to have its text changed.

        line : :attr:`~.Numeric`
            The number of the line to be changed.

        new_text : Optional[:attr:`~.Textable`], optional
            The new text that this line should have, or ``None`` to make it empty. Defaults to ``None``.

        Returns
        -------
        :class:`GameAction`
            The generated Game Action codeblock.

        Examples
        --------
        ::

            loc = DFLocation(1, 2, 3)  # location of the sign, or variable
            GameAction.change_sign(loc, 3, "haha")  # change line 3 to "haha"
            GameAction.change_sign(loc, 4)          # change line 4 to nothing (empty)
        """
        if isinstance(line, (int, float, DFNumber)):
            if not (1 <= int(line) <= 4):
                raise ValueError("Sign line number must be between 1 and 4.")

            line = DFNumber(int(line))  # floor; line numbers can only be ints

        return GameAction(
            action=GameActionType.CHANGE_SIGN,
            args=Arguments([
                p_check(loc, Locatable, "loc"),
                p_check(line, Numeric, "line"),
                *([p_check(new_text, Textable, "new_text")] if new_text is not None else [])  # empty line if None
            ]),
            append_to_reader=True
        )

    @classmethod
    def clear_scoreboard(cls) -> "GameAction":
        """Removes all scores from the scoreboard.

        Returns
        -------
        :class:`GameAction`
            The generated Game Action codeblock.

        Examples
        --------
        ::

            GameAction.clear_scoreboard()
        """
        return GameAction(
            action=GameActionType.CLEAR_SC_BOARD,
            args=Arguments(),
            append_to_reader=True
        )

    @classmethod
    def copy_blocks(cls, loc_1: Locatable, loc_2: Locatable, copy_pos: Locatable, paste_pos: Locatable) -> "GameAction":
        """Copies a region of blocks to another region, including air blocks.

        Parameters
        ----------
        loc_1 : :attr:`~.Locatable`
            The first corner of the region to be copied.

        loc_2 : :attr:`~.Locatable`
            The second corner of the region to be copied.

        copy_pos : :attr:`~.Locatable`
            The position from which the region is copied.

        paste_pos : :attr:`~.Locatable`
            The position from which the region is pasted.

            .. note::

                For optimal results, this position should be the same as copy_pos **in relation to the region**
                (i.e., have same distance or angle from center, for example).

        Returns
        -------
        :class:`GameAction`
            The generated Game Action codeblock.

        Warnings
        --------
        - 'Copy Blocks' has a limit of 50 000 blocks per operation.
        - 'Copy Blocks' has a cooldown of 5 000 blocks per second. For example, copying 15k blocks would have a 3 \
second cooldown."

        Examples
        --------
        ::

            loc_1 = DFLocation(1, 2, 3)  # some location
            loc_2 = DFVariable("%default other_loc")  # some variable containing a location
            copy_pos = DFGameValue(GameValueType.LOCATION, target=PlayerTarget.DEFAULT)  # default player's pos
            paste_pos = DFVariable("%default paste_pos")  # some variable containing a location
            GameAction.copy_blocks(loc_1, loc_2, copy_pos, paste_pos)
        """
        return GameAction(
            action=GameActionType.COPY_BLOCKS,
            args=Arguments([
                p_check(loc_1, Locatable, "loc_1"),
                p_check(loc_2, Locatable, "loc_2"),
                p_check(copy_pos, Locatable, "copy_pos"),
                p_check(paste_pos, Locatable, "paste_pos")
            ]),
            append_to_reader=True
        )

    @classmethod
    def create_animated_particle_circle(
        cls, particle: ParticleParam, center: Locatable,
        diameter: typing.Optional[Numeric] = None, duration: typing.Optional[Numeric] = None
    ) -> "GameAction":
        """Creates an animated circle of particles at a certain location.

        Parameters
        ----------
        particle : :attr:`~.ParticleParam`
            The particle to spawn.

        center : :attr:`~.Locatable`
            The center of the circle.

            .. note::

                The rotation of the circle is determined by this location's pitch and yaw.

        diameter : Optional[:attr:`~.Numeric`], optional
            The diameter of the circle, in blocks, or ``None`` for the default value (2 blocks).

        duration : Optional[:attr:`~.Numeric`], optional
            The duration of the animation, **in ticks**\\ , or ``None`` for the default value.


        Returns
        -------
        :class:`GameAction`
            The generated Game Action codeblock.

        Examples
        --------
        ::

            particle = DFParticle(ParticleType.CLOUD)
            center = DFLocation(1, 2, 3, 45, 60)  # 45, 60 are pitch and yaw, to determine the rotation of the circle
            GameAction.create_animated_particle_circle(particle, center, 5, 40)  # diameter: 5 blocks; duration: 2 s \
(40 ticks)
        """
        return GameAction(
            action=GameActionType.CREATE_ANIMATED_PARTICLE_CIRCLE,
            args=Arguments([
                p_check(particle, ParticleParam, "particle"),
                p_check(center, Locatable, "center"),
                p_check(diameter, Numeric, "diameter") if diameter is not None else None,
                p_check(duration, Numeric, "duration") if duration is not None else None
            ]),
            append_to_reader=True
        )

    @classmethod
    def create_animated_particle_line(
        cls, particle: ParticleParam, loc_1: Locatable, loc_2: Locatable,
        duration: typing.Optional[Numeric] = None
    ) -> "GameAction":
        """Creates a line of particles between two locations.

        Parameters
        ----------
        particle : :attr:`~.ParticleParam`
            The particle to spawn.

        loc_1 : :attr:`~.Locatable`
            The first location (first point of the particle line).

        loc_2 : :attr:`~.Locatable`
            The second location (second point of the particle line).

        duration : Optional[:attr:`~.Numeric`], optional
            The duration of the animation, **in ticks**\\ , or ``None`` for the default value.

        Returns
        -------
        :class:`GameAction`
            The generated Game Action codeblock.

        Examples
        --------
        ::

            particle = DFParticle(ParticleType.CLOUD)
            loc_1 = DFLocation(1, 2, 3)
            loc_2 = DFLocation(4, 2, 3)  # 4-block-long line
            GameAction.create_animated_particle_line(particle, loc_1, loc_2, 40)  # duration: 2 s (40 ticks)
        """
        return GameAction(
            action=GameActionType.CREATE_ANIMATED_PARTICLE_LINE,
            args=Arguments([
                p_check(particle, ParticleParam, "particle"),
                p_check(loc_1, Locatable, "loc_1"),
                p_check(loc_2, Locatable, "loc_2"),
                p_check(duration, Numeric, "duration") if duration is not None else None
            ]),
            append_to_reader=True
        )

    @classmethod
    def create_animated_particle_spiral(
        cls, particle: ParticleParam, base: Locatable,
        length: typing.Optional[Numeric] = None, diameter: typing.Optional[Numeric] = None,
        duration: typing.Optional[Numeric] = None
    ) -> "GameAction":
        """Creates an animated spiral of particles at a certain location.

        Parameters
        ----------
        particle : :attr:`~.ParticleParam`
            The particle to spawn.

        base : :attr:`~.Locatable`
            The base location of the spiral.

            .. note::

                The rotation of the spiral is determined by this location's pitch and yaw.

        length : Optional[:attr:`~.Numeric`], optional
            The length of the spiral, in blocks, or ``None`` for the default value (10 blocks).

        diameter : Optional[:attr:`~.Numeric`], optional
            The diameter of the spiral, in blocks, or ``None`` for the default value (2 blocks).

        duration : Optional[:attr:`~.Numeric`], optional
            The duration of the animation, **in ticks**\\ , or ``None`` for the default value.

        Returns
        -------
        :class:`GameAction`
            The generated Game Action codeblock.

        Examples
        --------
        ::

            particle = DFParticle(ParticleType.BARRIER)  # Type of particle.
            base = DFLocation(1, 2, 3, 45, 60)  # 45, 60 are pitch and yaw, to determine the rotation of the spiral
            GameAction.create_animated_particle_circle(particle, base, 15, 3, 40)
            # length: 15 blocks; diameter: 3 blocks; duration: 2 s (40 ticks)
        """
        return GameAction(
            action=GameActionType.CREATE_ANIMATED_PARTICLE_SPIRAL,
            args=Arguments([
                p_check(particle, ParticleParam, "particle"),
                p_check(base, Locatable, "base"),
                p_check(length, Numeric, "length") if length is not None else None,
                p_check(diameter, Numeric, "diameter") if diameter is not None else None,
                p_check(duration, Numeric, "duration") if duration is not None else None
            ]),
            append_to_reader=True
        )

    @classmethod
    def create_hologram(cls, loc: Locatable, text: Textable) -> "GameAction":
        """Creates a hologram (floating text) at a certain location.

        Parameters
        ----------
        loc : :attr:`~.Locatable`
            The location at which to place the hologram.

        text : :attr`~.Textable`
            The text that this hologram will display.

        Returns
        -------
        :class:`GameAction`
            The generated Game Action codeblock.

        Examples
        --------
        ::

            loc = DFVariable("some location")
            GameAction.create_hologram(loc, "Hey guys!")  # displays "Hey guys!" at the specified location
        """
        return GameAction(
            action=GameActionType.CREATE_HOLOGRAM,
            args=Arguments(),
            append_to_reader=True
        )

    @classmethod
    def create_particle_circle(
        cls, particle: ParticleParam, center: Locatable,
        diameter: typing.Optional[Numeric] = None
    ) -> "GameAction":
        """Creates a circle of particles at a certain location.

        Parameters
        ----------
        particle : :attr:`~.ParticleParam`
            The particle to spawn.

        center : :attr:`~.Locatable`
            The center of the circle.

            .. note::

                The rotation of the circle is determined by this location's pitch and yaw.

        diameter : Optional[:attr:`~.Numeric`], optional
            The diameter of the circle, in blocks, or ``None`` for the default value (2 blocks).

        Returns
        -------
        :class:`GameAction`
            The generated Game Action codeblock.

        Examples
        --------
        ::

            particle = DFParticle(ParticleType.CLOUD)
            center = DFLocation(1, 2, 3, 45, 60)  # 45, 60 are pitch and yaw, to determine the rotation of the circle
            GameAction.create_particle_circle(particle, center, 5)  # diameter: 5 blocks
        """
        return GameAction(
            action=GameActionType.CREATE_PARTICLE_CIRCLE,
            args=Arguments([
                p_check(particle, ParticleParam, "particle"),
                p_check(center, Locatable, "center"),
                p_check(diameter, Numeric, "diameter") if diameter is not None else None
            ]),
            append_to_reader=True
        )

    @classmethod
    def create_particle_cluster(cls) -> "GameAction":  # TODO: other particle stuff
        """Randomly spawns particles around a certain location.

        Returns
        -------
        :class:`GameAction`
            The generated Game Action codeblock.
        """
        return GameAction(
            action=GameActionType.CREATE_PARTICLE_CLUSTER,
            args=Arguments(),
            append_to_reader=True
        )

    @classmethod
    def create_particle_line(cls) -> "GameAction":
        """Creates a line of particles between two locations.

        Returns
        -------
        :class:`GameAction`
            The generated Game Action codeblock.
        """
        return GameAction(
            action=GameActionType.CREATE_PARTICLE_LINE,
            args=Arguments(),
            append_to_reader=True
        )

    @classmethod
    def create_particle_path(cls) -> "GameAction":
        """Creates a path of particles that goes through each location in the chest from first to last.

        Returns
        -------
        :class:`GameAction`
            The generated Game Action codeblock.
        """
        return GameAction(
            action=GameActionType.CREATE_PARTICLE_PATH,
            args=Arguments(),
            append_to_reader=True
        )

    @classmethod
    def create_particle_ray(cls) -> "GameAction":
        """Creates a ray of particles starting at a certain location.

        Returns
        -------
        :class:`GameAction`
            The generated Game Action codeblock.
        """
        return GameAction(
            action=GameActionType.CREATE_PARTICLE_RAY,
            args=Arguments(),
            append_to_reader=True
        )

    @classmethod
    def create_particle_sphere(cls) -> "GameAction":
        """Creates a sphere of particles at a certain location.

        Returns
        -------
        :class:`GameAction`
            The generated Game Action codeblock.
        """
        return GameAction(
            action=GameActionType.CREATE_PARTICLE_SPHERE,
            args=Arguments(),
            append_to_reader=True
        )

    @classmethod
    def create_particle_spiral(cls) -> "GameAction":
        """Creates a spiral of particles at a certain location.

        Returns
        -------
        :class:`GameAction`
            The generated Game Action codeblock.
        """
        return GameAction(
            action=GameActionType.CREATE_PARTICLE_SPIRAL,
            args=Arguments(),
            append_to_reader=True
        )

    @classmethod
    def drop_block(
        cls, loc: Locatable, block_type: typing.Optional[Material] = None,
        metadata: typing.Optional[typing.Union[
            typing.Dict[str, typing.Optional[typing.Union[str, int, bool, DFVariable]]],
            typing.Iterable[Textable]
        ]] = None,
        *, reform_on_impact: bool = True, hurt_hit_entities: bool = False
    ) -> "GameAction":
        """Spawns a falling block at the specified location.

        Parameters
        ----------
        loc : :attr:`~.Locatable`
            The location where to drop a block.

        block_type : Optional[:class:`~.Material`]
            The type of block to drop. Defaults to ``None``.

            .. note::

                If this is ``None``, then the block at the given location is turned into a falling block.

        metadata : Optional[Union[:class:`dict`, List[:attr:`~.Textable`]]]
            Optionally, the metadata of the falling block (``None`` for none). If not ``None``, can be in two forms:

            1. **As a dictionary:** If this is specified, then:
                - The keys must be strings;
                - The values can be one of:
                    - :class:`str` (the written out option);
                    - :class:`int` (is converted into a string accordingly);
                    - :class:`bool` (is turned into "true"/"false" accordingly);
                    - ``None`` (is turned into "none");
                    - :class:`~.DFVariable` (is turned into "%var(name)" accordingly).
                    - Any other types not mentioned will simply be ``str()``\\ ed.
                - Example::

                    {
                        "facing": "east",
                        "drag": True,
                        "west": None,
                        "rotation": 8,
                        "powered": DFVariable("my_var")

                    }

            2. **As a list/iterable:** If this is specified, then it must be a list of valid Textable parameters, \
whose values DF expects to be formatted in one of the following ways:
                - ``"tag=value"``
                - ``"tag:value"``
                - ``"tag,value"``

        reform_on_impact : :class:`bool`, optional
            Whether or not the block should be placed when it hits the ground. Defaults to ``True``.

        hurt_hit_entities ::class:`bool`, optional
            Whether or not entities hit by the falling block should receive damage. Defaults to ``False``.

        Returns
        -------
        :class:`GameAction`
            The generated Game Action codeblock.

        Raises
        ------
        :exc:`TypeError`
            If `metadata` is not a dict, an Iterable or None.

        Warnings
        --------
        Falling blocks automatically disappear after 30 seconds.

        Examples
        --------
        ::

            loc = DFLocation(1, 10, 3)   # where to spawn the falling block
            block_type = Material.BIRCH_STAIRS  # spawn Birch Stairs, for example
            metadata = { "facing": "east" }  # facing east; block metadata
            # OR
            metadata = ["facing=east"]  # also possible, as long as you follow the format

            GameAction.drop_block(loc, block_type, metadata, reform_on_impact=True, hurt_hit_entities=False)
            # Drops a falling Birch Stairs block, facing east, while not hurting any hit entities, and placing when it \
lands.
        """
        block_type = Material(block_type).value if block_type is not None else None
        true_metadata: typing.List[Textable] = []
        if isinstance(metadata, dict):
            for k, v in metadata.items():
                val_str: str
                if isinstance(v, bool):
                    val_str = "true" if v else "false"
                else:
                    val_str = str(v)

                separator: str = "="
                if "=" in val_str:
                    separator = "," if ":" in val_str else ":"

                true_metadata.append(DFText(f"{k}{separator}{val_str}"))

        elif isinstance(metadata, collections.Iterable):
            true_metadata = list(metadata)

        elif metadata is not None:
            raise TypeError("Metadata must either be a dictionary or an iterable of Textables.")

        return GameAction(
            action=GameActionType.DROP_BLOCK,
            args=Arguments(
                [
                    p_check(loc, Locatable, "loc"),
                    p_check(block_type, Textable, "block_type"),
                    *([p_check(text, Textable, f"metadata[{i}]") for i, text in true_metadata])
                ], tags=[
                    Tag(
                        "Reform on Impact", option=bool(reform_on_impact),
                        action=GameActionType.DROP_BLOCK, block=BlockType.GAME_ACTION
                    ),
                    Tag(
                        "Hurt Hit Entities", option=bool(hurt_hit_entities),
                        action=GameActionType.DROP_BLOCK, block=BlockType.GAME_ACTION
                    )
                ]
            ),
            append_to_reader=True
        )

    spawn_falling_block = drop_block  # alias

    @classmethod
    def empty_container(cls) -> "GameAction":
        """Empties a container.

        Returns
        -------
        :class:`GameAction`
            The generated Game Action codeblock.
        """
        return GameAction(
            action=GameActionType.EMPTY_CONTAINER,
            args=Arguments(),
            append_to_reader=True
        )

    @classmethod
    def explosion(cls) -> "GameAction":
        """Creates an explosion at a certain location.

        Returns
        -------
        :class:`GameAction`
            The generated Game Action codeblock.
        """
        return GameAction(
            action=GameActionType.EXPLOSION,
            args=Arguments(),
            append_to_reader=True
        )

    @classmethod
    def fill_container(cls) -> "GameAction":
        """Fills a container with items.

        Returns
        -------
        :class:`GameAction`
            The generated Game Action codeblock.
        """
        return GameAction(
            action=GameActionType.FILL_CONTAINER,
            args=Arguments(),
            append_to_reader=True
        )

    @classmethod
    def firework(cls) -> "GameAction":
        """Launches a firework at a certain location.

        Returns
        -------
        :class:`GameAction`
            The generated Game Action codeblock.
        """
        return GameAction(
            action=GameActionType.FIREWORK,
            args=Arguments(),
            append_to_reader=True
        )

    @classmethod
    def firework_effect(cls) -> "GameAction":
        """Creates a firework explosion at a certain location.

        Returns
        -------
        :class:`GameAction`
            The generated Game Action codeblock.
        """
        return GameAction(
            action=GameActionType.FIREWORK_EFFECT,
            args=Arguments(),
            append_to_reader=True
        )

    @classmethod
    def hide_sidebar(cls) -> "GameAction":
        """Disables the scoreboard sidebar on the plot.

        Returns
        -------
        :class:`GameAction`
            The generated Game Action codeblock.
        """
        return GameAction(
            action=GameActionType.HIDE_SIDEBAR,
            args=Arguments(),
            append_to_reader=True
        )

    @classmethod
    def launch_proj(cls) -> "GameAction":
        """Launches a projectile.

        Returns
        -------
        :class:`GameAction`
            The generated Game Action codeblock.
        """
        return GameAction(
            action=GameActionType.LAUNCH_PROJ,
            args=Arguments(),
            append_to_reader=True
        )

    @classmethod
    def lock_container(cls) -> "GameAction":
        """Sets a container's lock key.

        Returns
        -------
        :class:`GameAction`
            The generated Game Action codeblock.
        """
        return GameAction(
            action=GameActionType.LOCK_CONTAINER,
            args=Arguments(),
            append_to_reader=True
        )

    @classmethod
    def play_particle_effect(cls) -> "GameAction":
        """Plays a particle effect at a certain location.

        Returns
        -------
        :class:`GameAction`
            The generated Game Action codeblock.
        """
        return GameAction(
            action=GameActionType.PLAY_PARTICLE_EFFECT,
            args=Arguments(),
            append_to_reader=True
        )

    @classmethod
    def remove_hologram(cls) -> "GameAction":
        """Removes a hologram.

        Returns
        -------
        :class:`GameAction`
            The generated Game Action codeblock.
        """
        return GameAction(
            action=GameActionType.REMOVE_HOLOGRAM,
            args=Arguments(),
            append_to_reader=True
        )

    @classmethod
    def remove_score(cls) -> "GameAction":
        """Removes a score from the scoreboard.

        Returns
        -------
        :class:`GameAction`
            The generated Game Action codeblock.
        """
        return GameAction(
            action=GameActionType.REMOVE_SCORE,
            args=Arguments(),
            append_to_reader=True
        )

    @classmethod
    def set_block(cls) -> "GameAction":
        """Sets the block at a certain location or region.

        Returns
        -------
        :class:`GameAction`
            The generated Game Action codeblock.
        """
        return GameAction(
            action=GameActionType.SET_BLOCK,
            args=Arguments(),
            append_to_reader=True
        )

    @classmethod
    def set_block_data(cls) -> "GameAction":
        """Sets a metadata tag for a certain block.

        Returns
        -------
        :class:`GameAction`
            The generated Game Action codeblock.
        """
        return GameAction(
            action=GameActionType.SET_BLOCK_DATA,
            args=Arguments(),
            append_to_reader=True
        )

    @classmethod
    def set_container_name(cls) -> "GameAction":
        """Sets the custom name of a container (e.g. chests).

        Returns
        -------
        :class:`GameAction`
            The generated Game Action codeblock.
        """
        return GameAction(
            action=GameActionType.SET_CONTAINER_NAME,
            args=Arguments(),
            append_to_reader=True
        )

    @classmethod
    def set_furnace_speed(cls) -> "GameAction":
        """Sets the cook time multiplier of a furnace.

        Returns
        -------
        :class:`GameAction`
            The generated Game Action codeblock.
        """
        return GameAction(
            action=GameActionType.SET_FURNACE_SPEED,
            args=Arguments(),
            append_to_reader=True
        )

    @classmethod
    def set_sc_obj(cls) -> "GameAction":
        """Sets the objective name of the scoreboard on your plot.

        Returns
        -------
        :class:`GameAction`
            The generated Game Action codeblock.
        """
        return GameAction(
            action=GameActionType.SET_SC_OBJ,
            args=Arguments(),
            append_to_reader=True
        )

    @classmethod
    def set_score(cls) -> "GameAction":
        """Sets a score on the scoreboard.

        Returns
        -------
        :class:`GameAction`
            The generated Game Action codeblock.
        """
        return GameAction(
            action=GameActionType.SET_SCORE,
            args=Arguments(),
            append_to_reader=True
        )

    @classmethod
    def show_sidebar(cls) -> "GameAction":
        """Enables the scoreboard sidebar on the plot.

        Returns
        -------
        :class:`GameAction`
            The generated Game Action codeblock.
        """
        return GameAction(
            action=GameActionType.SHOW_SIDEBAR,
            args=Arguments(),
            append_to_reader=True
        )

    @classmethod
    def spawn_armor_stand(cls) -> "GameAction":
        """Creates an armor stand at a certain location.

        Returns
        -------
        :class:`GameAction`
            The generated Game Action codeblock.
        """
        return GameAction(
            action=GameActionType.SPAWN_ARMOR_STAND,
            args=Arguments(),
            append_to_reader=True
        )

    @classmethod
    def spawn_crystal(cls) -> "GameAction":
        """Spawns an End Crystal at a certain location.

        Returns
        -------
        :class:`GameAction`
            The generated Game Action codeblock.
        """
        return GameAction(
            action=GameActionType.SPAWN_CRYSTAL,
            args=Arguments(),
            append_to_reader=True
        )

    @classmethod
    def spawn_exp_orb(cls) -> "GameAction":
        """Spawns an experience orb at a certain location.

        Returns
        -------
        :class:`GameAction`
            The generated Game Action codeblock.
        """
        return GameAction(
            action=GameActionType.SPAWN_EXP_ORB,
            args=Arguments(),
            append_to_reader=True
        )

    @classmethod
    def spawn_fangs(cls) -> "GameAction":
        """Spawns Evoker Fangs at a certain location.

        Returns
        -------
        :class:`GameAction`
            The generated Game Action codeblock.
        """
        return GameAction(
            action=GameActionType.SPAWN_FANGS,
            args=Arguments(),
            append_to_reader=True
        )

    @classmethod
    def spawn_item(cls) -> "GameAction":
        """Spawns an item at a certain location.

        Returns
        -------
        :class:`GameAction`
            The generated Game Action codeblock.
        """
        return GameAction(
            action=GameActionType.SPAWN_ITEM,
            args=Arguments(),
            append_to_reader=True
        )

    @classmethod
    def spawn_mob(cls) -> "GameAction":
        """Spawns a mob at a certain location.

        Returns
        -------
        :class:`GameAction`
            The generated Game Action codeblock.
        """
        return GameAction(
            action=GameActionType.SPAWN_MOB,
            args=Arguments(),
            append_to_reader=True
        )

    @classmethod
    def spawn_rng_item(cls) -> "GameAction":
        """Randomly spawns an item at a certain location.

        Returns
        -------
        :class:`GameAction`
            The generated Game Action codeblock.
        """
        return GameAction(
            action=GameActionType.SPAWN_RNG_ITEM,
            args=Arguments(),
            append_to_reader=True
        )

    @classmethod
    def spawn_tnt(cls) -> "GameAction":
        """Spawns primed TNT at a certain location.

        Returns
        -------
        :class:`GameAction`
            The generated Game Action codeblock.
        """
        return GameAction(
            action=GameActionType.SPAWN_TNT,
            args=Arguments(),
            append_to_reader=True
        )

    @classmethod
    def spawn_vehicle(cls) -> "GameAction":
        """Spawns a vehicle at a certain location.

        Returns
        -------
        :class:`GameAction`
            The generated Game Action codeblock.
        """
        return GameAction(
            action=GameActionType.SPAWN_VEHICLE,
            args=Arguments(),
            append_to_reader=True
        )

    @classmethod
    def start_loop(cls) -> "GameAction":
        """Activates your plot's Loop Block if it has one.

        Returns
        -------
        :class:`GameAction`
            The generated Game Action codeblock.
        """
        return GameAction(
            action=GameActionType.START_LOOP,
            args=Arguments(),
            append_to_reader=True
        )

    @classmethod
    def stop_loop(cls) -> "GameAction":
        """Deactivates your plot's Loop Block if it has one.

        Returns
        -------
        :class:`GameAction`
            The generated Game Action codeblock.
        """
        return GameAction(
            action=GameActionType.STOP_LOOP,
            args=Arguments(),
            append_to_reader=True
        )

    @classmethod
    def summon_lightning(cls) -> "GameAction":
        """Strikes lightning at a certain location, damaging players in a radius.

        Returns
        -------
        :class:`GameAction`
            The generated Game Action codeblock.
        """
        return GameAction(
            action=GameActionType.SUMMON_LIGHTNING,
            args=Arguments(),
            append_to_reader=True
        )

    @classmethod
    def tick_block(cls) -> "GameAction":
        """Causes a block to get random ticked.

        Returns
        -------
        :class:`GameAction`
            The generated Game Action codeblock.
        """
        return GameAction(
            action=GameActionType.TICK_BLOCK,
            args=Arguments(),
            append_to_reader=True
        )

    @classmethod
    def uncancel_event(cls) -> "GameAction":
        """Uncancels the initial event that triggered this line of code.

        Returns
        -------
        :class:`GameAction`
            The generated Game Action codeblock.
        """
        return GameAction(
            action=GameActionType.UNCANCEL_EVENT,
            args=Arguments(),
            append_to_reader=True
        )

    # endregion:humanized-gameaction


class Control(ActionBlock, JSONData):
    """The Control block. Manages the code. See class methods for humanized methods. Example usage::

        @PlayerEvent.join
        def on_join():
            # ... do actions ...
            Control.wait(5, time_unit=CWaitTag.SECONDS)  # waits 5 seconds
            Control.line_return()  # returns

    Parameters
    ----------\u200b
    action : :class:`~py2df.enums.actions.ControlType`
        The type of Control block this is.

    args : :class:`~py2df.classes.collections.Arguments`
        The arguments of this Control block.

    append_to_reader : :class:`bool`, optional
        Whether or not this newly-created :class:`Control` should be already appended to the
        :class:`~py2df.reading.reader.DFReader`. Defaults to ``True``. (All classmethods will set this to ``True``)

    Attributes
    ----------\u200b
    block : :attr:`~py2df.enums.parameters.BlockType.CONTROL`
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
        """Produces a JSON-serializable dict representing this Control block.

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
            *, time_unit: enums.CWaitTag = DEFAULT_VAL,
            ticks: bool = True, seconds: bool = False, minutes: bool = False
    ) -> "Control":
        """Pauses the current line of code for a certain amount of ticks. seconds, or minutes.

        Examples of usage::

            @PlayerEvent.join
            def on_join():
                # ... actions ...
                Control.wait(40)  # TICKS by default; = 2 seconds
                Control.wait(40, ticks=True)  # same as above
                Control.wait(10, seconds=True)  # 10 seconds
                Control.wait(2, minutes=True)  # 2 minutes
                Control.wait(10, time_unit=CWaitTag.SECONDS)  # 10 seconds
                Control.wait(20, time_unit=TimeUnit.SECONDS)  # 20 seconds

        Parameters
        ----------
        duration : :attr:`~.Numeric`, optional
            The duration of time to wait for, according to the time unit specified in the ``time_unit`` param.
            Defaults to ``1``

        time_unit : :class:`~.CWaitTag`, optional
            The time unit that the duration was specified in. Defaults to :attr:`~py2df.enums.actions.CWaitTag.TICKS`.

        ticks : :class:`bool`, optional
            Alternatively, setting this to True sets time_unit to :attr:`~py2df.enums.actions.CWaitTag.TICKS`.
            Defaults to ``True`` .

        seconds : :class:`bool`, optional
            Alternatively, setting this to True sets time_unit to :attr:`~py2df.enums.actions.CWaitTag.SECONDS`.
            Defaults to ``False`` .

        minutes : :class:`bool`, optional
            Alternatively, setting this to True sets time_unit to :attr:`~py2df.enums.actions.CWaitTag.MINUTES`.
            Defaults to ``False`` .

        Returns
        -------
        :class:`Control`
            The generated :class:`Control` block.

        Warnings
        --------
        Setting ``time_unit`` to anything will override the ``ticks`` , ``seconds`` and ``minutes`` params. Also,
        note that **you cannot set more than one of them** to ``True``. If that happens, the first of the following line
        ``[seconds, minutes, ticks]`` that is ``True`` is chosen as the unit.
        """
        if time_unit == DEFAULT_VAL:
            if seconds:
                time_unit = enums.CWaitTag.SECONDS
            elif minutes:
                time_unit = enums.CWaitTag.MINUTES
            else:
                time_unit = enums.CWaitTag.TICKS

        return Control(
            ControlType.WAIT,
            Arguments(
                items=[p_check(duration, Numeric, "duration")] if duration != DEFAULT_VAL else None,
                tags=[Tag(
                    "Time Unit",
                    option=enums.CWaitTag(time_unit),
                    action=ControlType.WAIT, block=cls.block
                )]
            ),
            append_to_reader=True
        )


remove_u200b_from_doc((PlayerAction, EntityAction, GameAction, Control))
