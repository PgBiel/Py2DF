import itertools
import typing

from ._block_utils import _load_btype, BlockParam, _load_btypes
from .actions import PlayerAction, EntityAction
from .ifs import IfPlayer, IfEntity
from ..classes import Arguments, ItemCollection, Tag
from ..enums import PlayerTarget, EntityTarget, PlayerActionType, EntityActionType, IfPlayerType, IfEntityType, \
    BlockType
from ..typings import Textable, Numeric, Locatable, ItemParam, Potionable, ParticleParam, p_check, SpawnEggable, \
    p_bool_check
from ..utils import remove_u200b_from_doc


class Player:
    """Represents a DiamondFire Player. Used for Player Action and If Player humanized methods.

    Parameters
    ----------\u200b
    target : Optional[:class:`~.PlayerTarget`], optional
        The target that this instance represents (Default Player, Killer, Victim etc.) or None for default. Defaults
        to ``None``

    Attributes
    ----------\u200b
    target : Optional[:class:`~.PlayerTarget`]
        The target that this instance represents (Default Player, Killer, Victim etc.) or None for default.
    """
    __slots__ = ("target",)
    target: typing.Optional[PlayerTarget]

    def __init__(self, target: typing.Optional[PlayerTarget]):
        self.target: typing.Optional[PlayerTarget] = PlayerTarget(target) if target else None
    
    def _digest_target(self, target: typing.Optional[PlayerTarget]) -> typing.Optional[PlayerTarget]:
        """Checks a given player target for validity.
        
        Parameters
        ----------
        target : Optional[:class:`~.PlayerTarget`]
            The target to check.

        Returns
        -------
        Optional[:class:`~.PlayerTarget`]
            Returns the given target as a valid PlayerTarget, or None.
        """
        return PlayerTarget(target) if target else None
    
    # region:playeractions
    
    # endregion:playeractions
    
    # region:ifplayer
    
    # endregion:ifplayer


class Entity:
    """Represents a DiamondFire Entity. Used for Entity Action and If Entity humanized methods.

    Parameters
    ----------\u200b
    target : Optional[:class:`~.EntityTarget`], optional
        The target that this instance represents (Default Entity, Last Mob, Victim etc.) or None for default. Defaults
        to ``None``

    Attributes
    ----------\u200b
    target : Optional[:class:`~.EntityTarget`]
        The target that this instance represents (Default Entity, Last Mob, Victim etc.) or None for default.
    """
    __slots__ = ("target",)
    target: typing.Optional[EntityTarget]

    def __init__(self, target: typing.Optional[EntityTarget]):
        self.target: typing.Optional[EntityTarget] = EntityTarget(target) if target else None

    def _digest_target(self, target: typing.Optional[EntityTarget]) -> typing.Optional[EntityTarget]:
        """Checks a given entity target for validity.

        Parameters
        ----------
        target : Optional[:class:`~.EntityTarget`]
            The target to check.

        Returns
        -------
        Optional[:class:`~.EntityTarget`]
            Returns the given target as a valid EntityTarget, or None.
        """
        return EntityTarget(target) if target else None

    # region:entityactions

    # endregion:entityactions

    # region:ifentity

    def is_vehicle(self, *, target: typing.Optional[EntityTarget] = None) -> IfEntity:
        """Checks if an entity is a vehicle.

        Parameters
        ----------
        target : Optional[:class:`~.EntityTarget`], optional
            The target of this :class:`~.IfEntity`, or None for the current :class:`Entity` instance's target.
            Defaults to ``None``.

        Returns
        -------
        :class:`~.IfEntity`
            The generated IfEntity instance.

        Examples
        --------
        ::

            with last_entity.is_vehicle():
            # OR
            with Entity(EntityTarget.LAST_ENTITY).is_vehicle():
                # ... code to execute if the Last Spawned Entity is a vehicle ...
        """
        return IfEntity(
            action=IfEntityType.IS_VEHICLE,
            args=Arguments(),
            target=self._digest_target(target),
            append_to_reader=False,
            invert=False
        )

    def is_item(self, *, target: typing.Optional[EntityTarget] = None):
        """Checks if an entity is an item.

        Parameters
        ----------
        target : Optional[:class:`~.EntityTarget`], optional
            The target of this :class:`~.IfEntity`, or None for the current :class:`Entity` instance's target.
            Defaults to ``None``.

        Returns
        -------
        :class:`IfEntity`
            The generated IfEntity instance.

        Examples
        --------
        ::

            with last_entity.is_item():
            # OR
            with Entity(EntityTarget.LAST_ENTITY).is_item():
                # ... code to be executed if the Last Spawned Entity is an item ...
        """
        return IfEntity(
            action=IfEntityType.IS_ITEM,
            args=Arguments(),
            target=self._digest_target(target),
            append_to_reader=False,
            invert=False
        )

    def exists(self, *, target: typing.Optional[EntityTarget] = None):
        """Checks if an entity still exists in the world.

        Parameters
        ----------
        target : Optional[:class:`~.EntityTarget`], optional
            The target of this :class:`~.IfEntity`, or None for the current :class:`Entity` instance's target.
            Defaults to ``None``.

        Returns
        -------
        :class:`IfEntity`
            The generated IfEntity instance.

        Notes
        -----
        Entities which have been removed still remain in selections.


        Examples
        --------
        ::

            with last_entity.exists():
            # OR
            with Entity(EntityTarget.LAST_ENTITY).exists():
                # ... code to be executed if code to be executed if the Last Spawned Entity still exists ...
        """
        return IfEntity(
            action=IfEntityType.EXISTS,
            args=Arguments(),
            target=self._digest_target(target),
            append_to_reader=False,
            invert=False
        )

    def is_near(
        self, center: Locatable, range: typing.Optional[Numeric] = None,
        *, ignore_y_axis: bool = False,
        target: typing.Optional[EntityTarget] = None
    ):
        """Checks if an entity is within a certain range of a location.

        Parameters
        ----------
        center : :attr:`~.Locatable`
            Center location with which to check how near the entity is to it.

        range : Optional[:attr:`~.Numeric`], optional
            Maximum range permitted from the location, or ``None`` for the default (5 blocks). Default is ``None``.

        ignore_y_axis : :class:`bool`, optional
            Whether the Y-axis should be ignored when calculating distance. Defaults to ``False`` (no).

        target : Optional[:class:`~.EntityTarget`], optional
            The target of this :class:`~.IfEntity`, or None for the current :class:`Entity` instance's target.
            Defaults to ``None``.

        Returns
        -------
        :class:`IfEntity`
            The generated IfEntity instance.

        Examples
        --------
        ::

            center = DFLocation(1, 2, 3)  # where the entity should be near to
            range = 10  # 10 blocks max distance
            with last_entity.is_near(center, range, ignore_y_axis=False):
            # OR
            with Entity(EntityTarget.LAST_ENTITY).is_near(center, range, ignore_y_axis=False):
                # ... code to be executed if the Last Spawned Entity is at most 10 blocks away from 'center' ...
        """
        args = Arguments([
            p_check(center, Locatable, "center"),
            p_check(range, Numeric, "range") if range is not None else None
        ], tags=[
            Tag(
                "Ignore Y-Axis", option=bool(ignore_y_axis),  # default is False
                action=IfEntityType.IS_NEAR, block=BlockType.IF_GAME
            )
        ])
        return IfEntity(
            action=IfEntityType.IS_NEAR,
            args=args,
            target=self._digest_target(target),
            append_to_reader=False,
            invert=False
        )

    def is_type(
        self, *entity_types: typing.Union[SpawnEggable, ItemParam, Textable],
        target: typing.Optional[EntityTarget] = None
    ):
        """Checks if an entity is of a certain type.

        Parameters
        ----------
        entity_types : Union[:attr:`~.SpawnEggable`, :attr:`~.ItemParam`, :attr:`~.Textable`]
            Spawn egg (to check if it is a certain mob), projectile, or vehicle.
            The code is executed if the entity matches the type/one of the types specified.

            .. note:: 'Textable' type would be for specifying the item material as text.

        target : Optional[:class:`~.EntityTarget`], optional
            The target of this :class:`~.IfEntity`, or None for the current :class:`Entity` instance's target.
            Defaults to ``None``.

        Returns
        -------
        :class:`IfEntity`
            The generated IfEntity instance.

        Examples
        --------
        ::

            type_1 = Material.ENDERMAN_SPAWN_EGG  # either an enderman,
            type_2 = Material.SNOWBALL            # a snowball,
            type_3 = Material.MINECART            # or a minecart.

            with last_entity.is_type(type_1, type_2, type_3):
            # OR
            with Entity(EntityTarget.LAST_ENTITY).is_type(type_1, type_2, type_3):
                # ... code to be executed if the Last Spawned Entity is either an Enderman, a snowball, or a minecart \
...
        """
        args = Arguments([
            p_check(_load_btype(entity_type), typing.Union[SpawnEggable, ItemParam, Textable], f"entity_types[{i}]") for
            i, entity_type in enumerate(entity_types)
        ])
        return IfEntity(
            action=IfEntityType.IS_TYPE,
            args=args,
            target=self._digest_target(target),
            append_to_reader=False,
            invert=False
        )

    def standing_on(
            self, *block_types_or_locs: typing.Union[BlockParam, Locatable],
            target: typing.Optional[EntityTarget] = None
    ):
        """Checks if an entity is standing on a block of a certain type or at a certain location.

        Parameters
        ----------
        block_types_or_locs : Union[:class:`Material`, :attr:`~.ItemParam`, :attr:`~.Textable`, :attr:`~.Locatable`]
            The type of Block(s) to check for, or the location(s) to check (if the entity is standing on them).

            The block types can be specified either as:

            - an instance of :class:`~.Material` (the material of the block to set);
            - an item (:attr:`~.ItemParam` - the item representing the block to set);
            - text (:attr:`~.Textable` - the material of the block to set as text).

        target : Optional[:class:`~.EntityTarget`], optional
            The target of this :class:`~.IfEntity`, or None for the current :class:`Entity` instance's target.
            Defaults to ``None``.

        Returns
        -------
        :class:`IfEntity`
            The generated IfEntity instance.

        Warnings
        --------
        Any :class:`~.DFVariable` instances are assumed to refer to block type. In order to specify that it refers
        to the location the entity should be standing on, use :class:`~.LocVar`.

        Examples
        --------
        ::

            gold_block = Material.GOLD_BLOCK  # Must either be standing on any gold block, or...
            loc = DFLocation(1, 2, 3)         # ...on some specific location.
            with last_entity.standing_on(gold_block, loc):
            # OR
            with Entity(EntityTarget.LAST_ENTITY).standing_on(gold_block, loc):  # TODO: Example
                # ... code to be executed if the Last Spawned Entity is either standing on a gold block or on the \
given location ...
        """
        loaded_btypes = _load_btypes(block_types_or_locs)
        true_btypes = list(
            filter(
                lambda t: p_bool_check(t, typing.Union[ItemParam, Textable]),
                loaded_btypes
            )
        )
        locs = filter(
            lambda t: p_bool_check(t, Locatable) and t not in true_btypes, block_types_or_locs
        )
        _ = [p_check(el, typing.Union[ItemParam, Textable, Locatable]) for el in loaded_btypes]
        # error on unknown type

        args = Arguments([
            *true_btypes,
            *locs
        ])
        return IfEntity(
            action=IfEntityType.STANDING_ON,
            args=args,
            target=self._digest_target(target),
            append_to_reader=False,
            invert=False
        )

    def name_equals(
        self, *names: Textable,
        target: typing.Optional[EntityTarget] = None
    ):
        """Checks if an entity's name is equal to the text given/any of the texts given.

        Parameters
        ----------
        names : :attr:`~.Textable`
            Name(s) to check for.

        target : Optional[:class:`~.EntityTarget`], optional
            The target of this :class:`~.IfEntity`, or None for the current :class:`Entity` instance's target.
            Defaults to ``None``.

        Returns
        -------
        :class:`IfEntity`
            The generated IfEntity instance.

        Notes
        -----
        - 'Name Equals' also works with entities with custom names.
        - Works with UUID's.


        Examples
        --------
        ::
            
            with last_entity.name_equals("John", "Salad"):
            # OR
            with Entity(EntityTarget.LAST_ENTITY).name_equals("John", "Salad"):
                # ... code to be executed if the Last Spawned Entity's name is equal to either "John" or "Salad" ...
        """
        args = Arguments([
            p_check(name, Textable, f"names[{i}]") for i, name in enumerate(names)
        ])
        return IfEntity(
            action=IfEntityType.NAME_EQUALS,
            args=args,
            target=self._digest_target(target),
            append_to_reader=False,
            invert=False
        )

    def is_proj(self, *, target: typing.Optional[EntityTarget] = None):
        """Checks if an entity is a projectile.

        Parameters
        ----------
        target : Optional[:class:`~.EntityTarget`], optional
            The target of this :class:`~.IfEntity`, or None for the current :class:`Entity` instance's target.
            Defaults to ``None``.

        Returns
        -------
        :class:`IfEntity`
            The generated IfEntity instance.

        Examples
        --------
        ::

            with last_entity.is_proj():
            # OR
            with Entity(EntityTarget.LAST_ENTITY).is_proj():
                # ... code to be executed if the Last Spawned Entity is a projectile ...
        """
        return IfEntity(
            action=IfEntityType.IS_PROJ,
            args=Arguments(),
            target=self._digest_target(target),
            append_to_reader=False,
            invert=False
        )

    def is_mob(self, *, target: typing.Optional[EntityTarget] = None):
        """Checks if an entity is a mob.

        Parameters
        ----------
        target : Optional[:class:`~.EntityTarget`], optional
            The target of this :class:`~.IfEntity`, or None for the current :class:`Entity` instance's target.
            Defaults to ``None``.

        Returns
        -------
        :class:`IfEntity`
            The generated IfEntity instance.

        Examples
        --------
        ::

            with last_entity.is_mob():
            # OR
            with Entity(EntityTarget.LAST_ENTITY).is_mob():
                # ... code to be executed if if the Last Spawned Entity is a mob ...
        """
        return IfEntity(
            action=IfEntityType.IS_MOB,
            args=Arguments(),
            target=self._digest_target(target),
            append_to_reader=False,
            invert=False
        )

    # endregion:ifentity


remove_u200b_from_doc(Entity, Player)
