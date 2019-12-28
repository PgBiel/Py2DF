import collections
import itertools
import typing

from ._block_utils import _load_btype, BlockParam, _load_btypes
from .actions import PlayerAction, EntityAction
from .ifs import IfPlayer, IfEntity
from ..classes import Arguments, ItemCollection, Tag, DFNumber
from ..enums import PlayerTarget, EntityTarget, PlayerActionType, EntityActionType, IfPlayerType, IfEntityType, \
    BlockType, Hand, IfPOpenInvType, EffectParticleMode, HorseVariant, HorseColor, MooshroomVariant, \
    EntityAnimation, CatType, EntityColor, FoxType, PandaGene, ParrotVariant, ArmorStandPart
from ..typings import Textable, Numeric, Locatable, ItemParam, Potionable, ParticleParam, p_check, SpawnEggable, \
    p_bool_check, Listable
from ..utils import remove_u200b_from_doc, flatten


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

    def is_looking_at(
        self, *block_types_or_locs: typing.Union[BlockParam, Locatable, Listable],
        distance: typing.Optional[Numeric] = None,
        ignore_fluids: bool = True,
        target: typing.Optional[PlayerTarget] = None
    ):
        """Checks if a player is looking at a block of a certain type or at a certain location.

        Parameters
        ----------
        block_types_or_locs : Union[:class:`Material`, :attr:`~.ItemParam`, :attr:`~.Textable`, :attr:`~.Locatable`, \
:attr:`~.Listable`]
            The type of Block(s) to check for, or the location(s) to check (if the player is looking at them).

            Note that a :attr:`~.Listable` can also be given (i.e., the List of all block types/items/locations).

            The block types can be specified either as:

            - an instance of :class:`~.Material` (the material of the block to set);
            - an item (:attr:`~.ItemParam` - the item representing the block to set);
            - text (:attr:`~.Textable` - the material of the block to set as text);
            - a :attr:`~.Listable` (A List - in DF - variable containing either Item or Text parameters).

        distance : Optional[:attr:`~.Numeric`], optional
            Maximum distance from target block to consider. Default is ``None``.

        ignore_fluids : :class:`bool`, optional
            If ``True``, fluids are ignored when checking at which block the player is looking. If ``False``,
            they are considered. Defaults to ``True``.

        target : Optional[:class:`~.PlayerTarget`], optional
            The target of this :class:`~.IfPlayer`, or None for the current :class:`Player` instance's target.
            Defaults to ``None``.

        Returns
        -------
        :class:`~.IfPlayer`
            The generated IfPlayer instance.

        Warnings
        --------
        Any :class:`~.DFVariable` instances are assumed to refer to block type. In order to specify that it refers
        to the location the entity should be standing on, use :class:`~.LocVar`.

        Examples
        --------
        ::

            gold_block = Material.GOLD_BLOCK  # either looking at a gold block...
            loc = DFLocation(1, 2, 3)         # ...or at the given location
            with p_default.is_looking_at(gold_block, loc, distance=10):  # at most 10 blocks away
            # OR
            with Player(PlayerTarget.DEFAULT).is_looking_at(gold_block, loc, distance=10):
                # ... code to be executed if the Default Player is looking at either a gold block or at the given \
location, at most 10 blocks away ...
        """
        loaded_btypes = _load_btypes(block_types_or_locs)
        true_btypes = list(
            filter(
                lambda t: p_bool_check(t, typing.Union[ItemParam, Textable, Listable]),
                loaded_btypes
            )
        )
        locs = filter(
            lambda t: p_bool_check(t, Locatable) and t not in true_btypes, block_types_or_locs
        )
        _ = [
            p_check(el, typing.Union[ItemParam, Textable, Locatable, Listable], f"block_types_or_locs[{i}]")
            for i, el in enumerate(loaded_btypes)
        ]
        # error on unknown type

        args = Arguments([
            *true_btypes,
            *locs,
            p_check(distance, typing.Optional[Numeric], "distance") if distance is not None else None
        ], tags=[
            Tag(
                "Fluid Mode", option="Ignore Fluids" if ignore_fluids else "Detect Fluids",  # default is Ignore Fluids
                action=IfPlayerType.IS_LOOKING_AT, block=BlockType.IF_GAME
            )
        ])
        return IfPlayer(
            action=IfPlayerType.IS_LOOKING_AT,
            args=args,
            target=self._digest_target(target),
            append_to_reader=False,
            invert=False
        )

    def in_world_border(
        self, loc: typing.Optional[Locatable] = None,
        *, target: typing.Optional[PlayerTarget] = None
    ):
        """Checks if the player (or a location) is within their world border.

        .. rank:: Emperor


        Parameters
        ----------
        loc : Optional[:attr:`~.Locatable`], optional
            Location to check if is within the player's world border. Default is ``None`` (check the player itself).

        target : Optional[:class:`~.PlayerTarget`], optional
            The target of this :class:`~.IfPlayer`, or None for the current :class:`Player` instance's target.
            Defaults to ``None``.

        Returns
        -------
        :class:`~.IfPlayer`
            The generated IfPlayer instance.

        Examples
        --------
        ::

            with p_default.in_world_border():
            # OR
            with Player(PlayerTarget.DEFAULT).in_world_border():
                # ... code to be executed if the Default Player is in the world border ...

            # or specify a location to check if that location is within the player's world border.
        """
        args = Arguments([
            p_check(loc, typing.Optional[Locatable], "loc") if loc is not None else None
        ])
        return IfPlayer(
            action=IfPlayerType.IN_WORLD_BORDER,
            args=args,
            target=self._digest_target(target),
            append_to_reader=False,
            invert=False
        )

    def has_room_for_item(
        self, item: typing.Optional[ItemParam] = None,
        *, target: typing.Optional[PlayerTarget] = None
    ):
        """Checks if a player's inventory has enough room for an item to be given.

        Parameters
        ----------
        item : Optional[:attr:`~.ItemParam`], optional
            Item (stack) to check. Default is ``None`` (has room for any item).

        target : Optional[:class:`~.PlayerTarget`], optional
            The target of this :class:`~.IfPlayer`, or None for the current :class:`Player` instance's target.
            Defaults to ``None``.

        Returns
        -------
        :class:`~.IfPlayer`
            The generated IfPlayer instance.

        Examples
        --------
        ::

            item = 32 * Item(Material.STONE)
            with p_default.has_room_for_item(item):
            # OR
            with Player(PlayerTarget.DEFAULT).has_room_for_item(item):
                # ... code to be executed if the Default Player has room for 32 stones ...
        """
        args = Arguments([
            p_check(item, typing.Optional[ItemParam], "item") if item is not None else None
        ])
        return IfPlayer(
            action=IfPlayerType.HAS_ROOM_FOR_ITEM,
            args=args,
            target=self._digest_target(target),
            append_to_reader=False,
            invert=False
        )

    def no_item_cooldown(
        self, item: ItemParam,
        *, target: typing.Optional[PlayerTarget] = None
    ):
        """Checks if the player does not have a cooldown applied to an item type (material).

        Parameters
        ----------
        item : :attr:`~.ItemParam`
            Item type to check. (Note that only the Material determines the cooldown.)

        target : Optional[:class:`~.PlayerTarget`], optional
            The target of this :class:`~.IfPlayer`, or None for the current :class:`Player` instance's target.
            Defaults to ``None``.

        Returns
        -------
        :class:`~.IfPlayer`
            The generated IfPlayer instance.

        Examples
        --------
        ::

            d_sword = Material.DIAMOND_SWORD
            with p_default.no_item_cooldown(d_sword):
            # OR
            with Player(PlayerTarget.DEFAULT).no_item_cooldown(d_sword):
                # ... code to be executed if the Default Player doesn't have a cooldown on diamond swords ...
        """
        args = Arguments([
            p_check(item, ItemParam, "item")
        ])
        return IfPlayer(
            action=IfPlayerType.NO_ITEM_COOLDOWN,
            args=args,
            target=self._digest_target(target),
            append_to_reader=False,
            invert=False
        )

    def has_all_items(
        self, *items: typing.Union[ItemParam, ItemCollection, typing.Iterable[ItemParam], Listable],
        target: typing.Optional[PlayerTarget] = None
    ):
        """Checks if a player has all of the given items.

        Parameters
        ----------
        items : Optional[Union[:class:`~.ItemParam`, :class:`~.ItemCollection`, Iterable[:class:`~.ItemParam`], \
:attr:`Listable`]]
            Item(s) to check for. The items can be specified either as:

            - ``None`` for an empty slot;
            - :class:`~.ItemParam` for one item;
            - :attr:`~.Listable` for a variable list of items;
            - :class:`~.ItemCollection` or Iterable[:class:`~.ItemParam`] for a predetermined list of items.

        target : Optional[:class:`~.PlayerTarget`], optional
            The target of this :class:`~.IfPlayer`, or None for the current :class:`Player` instance's target.
            Defaults to ``None``.

        Returns
        -------
        :class:`~.IfPlayer`
            The generated IfPlayer instance.

        Examples
        --------
        ::

            item_1 = Item(Material.STONE)          # must have both a Stone (with no other propeties)...
            item_2 = Item(Material.DIAMOND_SWORD)  # ...and a diamond sword (with no other properties).
            with p_default.has_all_items(item_1, item_2):
            # OR
            with Player(PlayerTarget.DEFAULT).has_all_items(item_1, item_2):
                # ... code to be executed if the Default Player has both item 1 and item 2 ...
        """
        item_list = flatten(*items, except_iterables=[str], max_depth=1)

        args = Arguments([
            p_check(item, ItemParam, "items") for item in item_list
        ])
        return IfPlayer(
            action=IfPlayerType.HAS_ALL_ITEMS,
            args=args,
            target=self._digest_target(target),
            append_to_reader=False,
            invert=False
        )

    def is_swimming(self, *, target: typing.Optional[PlayerTarget] = None):
        """Checks if a player is in water or lava.

        Parameters
        ----------
        target : Optional[:class:`~.PlayerTarget`], optional
            The target of this :class:`~.IfPlayer`, or None for the current :class:`Player` instance's target.
            Defaults to ``None``.

        Returns
        -------
        :class:`~.IfPlayer`
            The generated IfPlayer instance.

        Notes
        -----
        Use 'Is Sprinting' to check if a player is swimming with the swimming animation.

        Examples
        --------
        ::

            with p_default.is_swimming():
            # OR
            with Player(PlayerTarget.DEFAULT).is_swimming():
                # ... code to be executed if the Default Player is swimming ...
        """
        return IfPlayer(
            action=IfPlayerType.IS_SWIMMING,
            args=Arguments(),
            target=self._digest_target(target),
            append_to_reader=False,
            invert=False
        )

    def has_item(
        self, *items: typing.Union[ItemParam, ItemCollection, typing.Iterable[ItemParam], Listable],
        target: typing.Optional[PlayerTarget] = None
    ):
        """Checks if a player has an item/any of some given items in their inventory.

        Parameters
        ----------
        items : Optional[Union[:class:`~.ItemParam`, :class:`~.ItemCollection`, Iterable[:class:`~.ItemParam`], \
:attr:`Listable`]]
            Item(s) to check for (must have at least one). The items can be specified either as:

            - ``None`` for an empty slot;
            - :class:`~.ItemParam` for one item;
            - :attr:`~.Listable` for a variable list of items;
            - :class:`~.ItemCollection` or Iterable[:class:`~.ItemParam`] for a predetermined list of items.

        target : Optional[:class:`~.PlayerTarget`], optional
            The target of this :class:`~.IfPlayer`, or None for the current :class:`Player` instance's target.
            Defaults to ``None``.

        Returns
        -------
        :class:`~.IfPlayer`
            The generated IfPlayer instance.

        Examples
        --------
        ::

            item_1 = Item(Material.STONE)          # must have either a Stone (with no other propeties)...
            item_2 = Item(Material.DIAMOND_SWORD)  # ...or a diamond sword (with no other properties).
            with p_default.has_item(item_1, item_2):
            # OR
            with Player(PlayerTarget.DEFAULT).has_item(item_1, item_2):
                # ... code to be executed if the Default Player has at least one of the given items.
        """
        item_list = flatten(*items, except_iterables=[str], max_depth=1)

        args = Arguments([
            p_check(item, ItemParam, "items") for item in item_list
        ])
        return IfPlayer(
            action=IfPlayerType.HAS_ITEM,
            args=args,
            target=self._digest_target(target),
            append_to_reader=False,
            invert=False
        )

    has_any_item = has_item
    """Alias of :meth:`has_item`"""

    # def block_equals(  # already in IfGame
    #     self, *block_types: typing.Union[BlockParam, Listable],
    #     target: typing.Optional[PlayerTarget] = None
    # ):
    #     """Checks if the block in a block interaction event is a certain block, or one of certain blocks.
    #
    #     .. rank:: Emperor
    #
    #     .. workswith:: Player Place Block Event, Player Break Block Event
    #
    #     Parameters
    #     ----------
    #     block_types : Union[:class:`Material`, :attr:`~.ItemParam`, :attr:`~.Textable`, :attr:`~.Listable`]
    #         The type of Block(s) to check for.
    #
    #         The type can be specified either as:
    #
    #         - an instance of :class:`~.Material` (the material of the block to set);
    #         - an item (:attr:`~.ItemParam` - the item representing the block to set);
    #         - text (:attr:`~.Textable` - the material of the block to set as text);
    #         - a :attr:`~.Listable` (A List - in DF - variable containing either Item or Text parameters).
    #
    #         .. note::
    #
    #             If multiple items are given, then the block can be any of them.
    #
    #     target : Optional[:class:`~.PlayerTarget`], optional
    #         The target of this :class:`~.IfPlayer`, or None for the current :class:`Player` instance's target.
    #         Defaults to ``None``.
    #
    #     Returns
    #     -------
    #     :class:`~.IfPlayer`
    #         The generated IfPlayer instance.
    #
    #     Examples
    #     --------
    #     ::
    #
    #         gold_block =
    #         with p_default.block_equals(block_types):
    #         # OR
    #         with Player(PlayerTarget.DEFAULT).block_equals(block_types):
    #             # ... code to be executed if the Default Player # TODO: Example
    #     """
    #     true_btypes = _load_btypes(block_types)
    #
    #     args = Arguments([
    #         p_check(block_type, typing.Union[ItemParam, Textable], f"block_types[{i}]") for i, block_type in
    #         enumerate(true_btypes)
    #     ])
    #     return IfPlayer(
    #         action=IfPlayerType.BLOCK_EQUALS,
    #         args=args,
    #         target=self._digest_target(target),
    #         append_to_reader=False,
    #         invert=False
    #     )

    def is_wearing(
        self, *items: typing.Union[ItemParam, ItemCollection, typing.Iterable[ItemParam], Listable],
        wearing_all: bool = False,
        target: typing.Optional[PlayerTarget] = None
    ):
        """Checks if a player is wearing an item.

        Parameters
        ----------
        items : Optional[Union[:class:`~.ItemParam`, :class:`~.ItemCollection`, Iterable[:class:`~.ItemParam`], :attr:`Listable`]]
            Item(s) to check for. The items can be specified either as:

            - ``None`` for an empty slot;
            - :class:`~.ItemParam` for one item;
            - :attr:`~.Listable` for a variable list of items;
            - :class:`~.ItemCollection` or Iterable[:class:`~.ItemParam`] for a predetermined list of items.

        wearing_all : :class:`bool`, optional
            If ``True``, the player must be wearing all given items. If ``False``, the player must be wearing
            at least one of them. Defaults to ``False``.

        target : Optional[:class:`~.PlayerTarget`], optional
            The target of this :class:`~.IfPlayer`, or None for the current :class:`Player` instance's target.
            Defaults to ``None``.

        Returns
        -------
        :class:`~.IfPlayer`
            The generated IfPlayer instance.

        Examples
        --------
        ::

            dia_helm = Item(Material.DIAMOND_HELMET, name="T")     # must be wearing either a diamond helmet named "T",
            iron_chest = Item(Material.IRON_CHESTPLATE, name="E")  # or an iron chestplate named "E".
            with p_default.is_wearing(dia_helm, iron_chest, wearing_all=False):
            # OR
            with Player(PlayerTarget.DEFAULT).is_wearing(dia_helm, iron_chest, wearing_all=False):
                # ... code to be executed if the Default Player wears at least one of the given items ...
                # (set 'wearing_all' to True to require it to be wearing all given items simultaneously)
        """
        item_list = flatten(*items, except_iterables=[str], max_depth=1)

        args = Arguments([
            p_check(item, ItemParam, "items") for item in item_list
        ], tags=[
            Tag(
                "Check Mode", option="Is Wearing All" if wearing_all else "Is Wearing Some",  # default: Is Wearing Some
                action=IfPlayerType.IS_WEARING, block=BlockType.IF_GAME
            )
        ])
        return IfPlayer(
            action=IfPlayerType.IS_WEARING,
            args=args,
            target=self._digest_target(target),
            append_to_reader=False,
            invert=False
        )

    def is_near(
        self, *locs: typing.Union[Locatable, Listable], distance: typing.Optional[Numeric] = None,
        ignore_y_axis: bool = False,
        target: typing.Optional[PlayerTarget] = None
    ):
        """Checks if a player is within a certain range of a location. (default: 5 blocks)

        Parameters
        ----------
        locs : Union[:attr:`~.Locatable`, :attr:`~.Listable`]
            Center location(s) - must be near to at least one of them by the given distance amount.
            (A variable representing a list of locations can also be specified.)

        distance : Optional[:attr:`~.Numeric`], optional
            Maximum distance allowed from at least one of the locations, or ``None`` for the default (5 blocks).
            Default is ``None``.

        ignore_y_axis : :class:`bool`, optional
            If the Y-axis should be ignored when calculating distances (i.e., only X and Z should be considered).
            Defaults to ``False``.

        target : Optional[:class:`~.PlayerTarget`], optional
            The target of this :class:`~.IfPlayer`, or None for the current :class:`Player` instance's target.
            Defaults to ``None``.

        Returns
        -------
        :class:`~.IfPlayer`
            The generated IfPlayer instance.

        Examples
        --------
        ::

            loc_1 = DFLocation(1, 2, 3)
            loc_2 = LocVar("my var")
            with p_default.is_near(loc_1, loc_2, range=10):
            # OR
            with Player(PlayerTarget.DEFAULT).is_near(loc_1, loc_2, range=10):
                # ... code to be executed if the Default Player is at most 10 blocks away from at least one of the \
given locations ...
        """
        args = Arguments([
            *[p_check(loc, typing.Union[Locatable, Listable], f"locs[{i}]") for i, loc in enumerate(locs)],
            p_check(distance, typing.Optional[Numeric], "distance") if distance is not None else None
        ], tags=[
            Tag(
                "Ignore Y-Axis", option=bool(ignore_y_axis),  # default is False
                action=IfPlayerType.IS_NEAR, block=BlockType.IF_GAME
            )
        ])
        return IfPlayer(
            action=IfPlayerType.IS_NEAR,
            args=args,
            target=self._digest_target(target),
            append_to_reader=False,
            invert=False
        )

    def standing_on(
        self, *block_types_or_locs: typing.Union[BlockParam, Locatable, Listable],
        target: typing.Optional[PlayerTarget] = None
    ):
        """Checks if a player is standing on a block of a certain type or at a certain location.

        Parameters
        ----------
        block_types_or_locs : Union[:class:`Material`, :attr:`~.ItemParam`, :attr:`~.Textable`, :attr:`~.Locatable`, :attr:`~.Listable`]
            The type of Block(s) to check for, or the location(s) to check (if the player is standing on at least
            one of them).

            Note that a :attr:`~.Listable` can also be given (i.e., the List of all block types/items/locations).

            The block types can be specified either as:

            - an instance of :class:`~.Material` (the material of the block to set);
            - an item (:attr:`~.ItemParam` - the item representing the block to set);
            - text (:attr:`~.Textable` - the material of the block to set as text);
            - a :attr:`~.Listable` (A List - in DF - variable containing either Item or Text parameters).

        target : Optional[:class:`~.PlayerTarget`], optional
            The target of this :class:`~.IfPlayer`, or None for the current :class:`Player` instance's target.
            Defaults to ``None``.

        Returns
        -------
        :class:`~.IfPlayer`
            The generated IfPlayer instance.

        Examples
        --------
        ::

            gold_block = Material.GOLD_BLOCK  # must either be standing on a gold block,
            loc = DFLocation(1, 2, 3)         # or on the given location.
            with p_default.standing_on(gold_block, loc):
            # OR
            with Player(PlayerTarget.DEFAULT).standing_on(gold_block, loc):
                # ... code to be executed if the Default Player is standing either on a gold block or on the given \
location ...
        """
        loaded_btypes = _load_btypes(block_types_or_locs)
        true_btypes = list(
            filter(
                lambda t: p_bool_check(t, typing.Union[ItemParam, Textable, Listable]),
                loaded_btypes
            )
        )
        locs = filter(
            lambda t: t not in true_btypes and p_bool_check(t, Locatable), block_types_or_locs
        )
        _ = [
            p_check(el, typing.Union[ItemParam, Textable, Locatable, Listable], f"block_types_or_locs[{i}]")
            for i, el in enumerate(loaded_btypes)
        ]
        # error on unknown type

        args = Arguments([
            *true_btypes,
            *locs
        ])
        return IfPlayer(
            action=IfPlayerType.STANDING_ON,
            args=args,
            target=self._digest_target(target),
            append_to_reader=False,
            invert=False
        )

    # def cmd_equals(
    #         self, *texts: typing.Union[Textable, Listable],
    #         check_mode="Check Entire Command", ignore_case: bool = True,
    #         target: typing.Optional[PlayerTarget] = None
    # ):
    #     """Checks if a player's command is equal to a certain text when the Player Command Event is executed.
    #
    #     .. rank:: Emperor
    #
    #     .. workswith:: Player Command Event
    #
    #     Parameters
    #     ----------
    #     texts : Union[:attr:`~.Textable`, :attr:`~.Listable`]
    #         Text(s) to check for.
    #
    #     check_mode :
    #         Check Entire Command, Check First Word
    #
    #     ignore_case : :class:`bool`, optional
    #         Defaults to ``True``.
    #
    #     target : Optional[:class:`~.PlayerTarget`], optional
    #         The target of this :class:`~.IfPlayer`, or None for the current :class:`Player` instance's target.
    #         Defaults to ``None``.
    #
    #     Returns
    #     -------
    #     :class:`~.IfPlayer`
    #         The generated IfPlayer instance.
    #
    #     Examples
    #     --------
    #     ::
    #
    #         with p_default.cmd_equals(texts):
    #         # OR
    #         with Player(PlayerTarget.DEFAULT).cmd_equals(texts):
    #             # ... code to be executed if the Default Player # TODO: Example
    #     """
    #     args = Arguments([
    #         p_check(text, typing.Union[Textable, Listable], f"texts[{i}]") for i, text in enumerate(texts)
    #     ], tags=[
    #         Tag(
    #             "Check Mode", option=check_mode,  # default is Check Entire Command
    #             action=IfPlayerType.CMD_EQUALS, block=BlockType.IF_GAME
    #         ),
    #         Tag(
    #             "Ignore Case", option=bool(ignore_case),  # default is True
    #             action=IfPlayerType.CMD_EQUALS, block=BlockType.IF_GAME
    #         )
    #     ])
    #     return IfPlayer(
    #         action=IfPlayerType.CMD_EQUALS,
    #         args=args,
    #         target=self._digest_target(target),
    #         append_to_reader=False,
    #         invert=False
    #     )

    def has_effect(
        self, *potions: typing.Union[Potionable, Listable],
        has_all_effects: bool = False,
        target: typing.Optional[PlayerTarget] = None
    ):
        """Checks if a player has a potion effect.

        Parameters
        ----------
        potions : Union[:attr:`~.Potionable`, :attr:`~.Listable`]
            Potion(s) to check for, or a list variable containing them.

        has_all_effects : :class:`bool`, optional
            If the player must have all potion effects specified, instead of just one of them. Defaults to
            ``False``.

        target : Optional[:class:`~.PlayerTarget`], optional
            The target of this :class:`~.IfPlayer`, or None for the current :class:`Player` instance's target.
            Defaults to ``None``.

        Returns
        -------
        :class:`~.IfPlayer`
            The generated IfPlayer instance.

        Notes
        -----
        Amplifiers and durations do not have to be the same as the initial potion effect(s).


        Examples
        --------
        ::

            potion_1 = DFPotion(PotionType.ABSORPTION)
            potion_2 = DFPotion(PotionType.POISON)
            with p_default.has_effect(potion_1, potion_2, has_all_effects=False):
            # OR
            with Player(PlayerTarget.DEFAULT).has_effect(potion_1, potion_2, has_all_effects=False):
                # ... code to be executed if the Default Player has either Absorption or Poison ...
                # (specify has_all_effects=True to check if the player has all of them simultaneously)
        """
        args = Arguments([
            p_check(potion, typing.Union[Potionable, Listable], f"potions[{i}]") for i, potion in enumerate(potions)
        ], tags=[
            Tag(
                "Check Mode", option="Has All Effects" if has_all_effects else "Has Any Effect",  # d: Has Any Effect
                action=IfPlayerType.HAS_EFFECT, block=BlockType.IF_GAME
            )
        ])
        return IfPlayer(
            action=IfPlayerType.HAS_EFFECT,
            args=args,
            target=self._digest_target(target),
            append_to_reader=False,
            invert=False
        )

    def is_grounded(self, *, target: typing.Optional[PlayerTarget] = None):
        """Checks if a player is supported by a block.

        Parameters
        ----------
        target : Optional[:class:`~.PlayerTarget`], optional
            The target of this :class:`~.IfPlayer`, or None for the current :class:`Player` instance's target.
            Defaults to ``None``.

        Returns
        -------
        :class:`~.IfPlayer`
            The generated IfPlayer instance.

        Examples
        --------
        ::

            with p_default.is_grounded():
            # OR
            with Player(PlayerTarget.DEFAULT).is_grounded():
                # ... code to be executed if the Default Player is supported by a block (on the 'ground') ...
        """
        return IfPlayer(
            action=IfPlayerType.IS_GROUNDED,
            args=Arguments(),
            target=self._digest_target(target),
            append_to_reader=False,
            invert=False
        )

#     def item_equals(
#         self, *items: typing.Union[ItemParam, ItemCollection, typing.Iterable[ItemParam], Listable],
#         target: typing.Optional[PlayerTarget] = None
#     ):
#         """Checks if the items in one of the events below is a certain item.
#
#         .. workswith::
#
#             Player Click Item Events, Player Pickup Item Event, Player Drop Item Event, Player Consume Item Event
#
#         Parameters
#         ----------
#         items : Optional[Union[:class:`~.ItemParam`, :class:`~.ItemCollection`, Iterable[:class:`~.ItemParam`], \
# :attr:`Listable`]]
#             Item(s) to check for (must match one of them). The items can be specified either as:
#
#             - ``None`` for an empty slot;
#             - :class:`~.ItemParam` for one item;
#             - :attr:`~.Listable` for a variable list of items;
#             - :class:`~.ItemCollection` or Iterable[:class:`~.ItemParam`] for a predetermined list of items.
#
#             .. note::
#
#                 If multiple items given, the event item can be any of them.
#
#         target : Optional[:class:`~.PlayerTarget`], optional
#             The target of this :class:`~.IfPlayer`, or None for the current :class:`Player` instance's target.
#             Defaults to ``None``.
#
#         Returns
#         -------
#         :class:`~.IfPlayer`
#             The generated IfPlayer instance.
#
#         Examples
#         --------
#         ::
#
#             with p_default.item_equals(items):
#             # OR
#             with Player(PlayerTarget.DEFAULT).item_equals(items):
#                 # ... code to be executed if the Default Player # TODO: Example
#         """
#         item_list = flatten(*items, except_iterables=[str], max_depth=1)
#
#         args = Arguments([
#             p_check(item, typing.Union[ItemParam, Listable], "items") for item in item_list
#         ])
#         return IfPlayer(
#             action=IfPlayerType.ITEM_EQUALS,
#             args=args,
#             target=self._digest_target(target),
#             append_to_reader=False,
#             invert=False
#         )

    def cursor_item_equals(
        self,
        *items: typing.Optional[typing.Union[ItemParam, ItemCollection, typing.Iterable[ItemParam], Listable]],
        target: typing.Optional[PlayerTarget] = None
    ):
        """Checks if the item that is being moved with a player's cursor is a certain item.

        Parameters
        ----------
        items : Optional[Optional[Union[:class:`~.ItemParam`, :class:`~.ItemCollection`, Iterable[:class:`~.ItemParam`], :attr:`Listable`]]], optional
            Items(s) to check for. The items can be specified either as:

            - ``None`` for an empty slot;
            - :class:`~.ItemParam` for one item;
            - :attr:`~.Listable` for a variable list of items;
            - :class:`~.ItemCollection` or Iterable[:class:`~.ItemParam`] for a predetermined list of items.
            
            .. note::
                
                If multiple items are given, the player can have any of them on their cursor.

        target : Optional[:class:`~.PlayerTarget`], optional
            The target of this :class:`~.IfPlayer`, or None for the current :class:`Player` instance's target.
            Defaults to ``None``.

        Returns
        -------
        :class:`~.IfPlayer`
            The generated IfPlayer instance.

        Warnings
        -----
        When used on the Player Click Item in Own Inventory Event, 'Cursor Item Equals' checks the previous cursor item, not the item that was clicked.


        Examples
        --------
        ::

            item_1 = Item(Material.STONE, name="my stone")
            item_2 = Item(Material.GOLD_BLOCK, lore=["e"])
            with p_default.cursor_item_equals(item_1, item_2):
            # OR
            with Player(PlayerTarget.DEFAULT).cursor_item_equals(item_1, item_2):
                # ... code to be executed if the Default Player has either of the given items on its cursor ...
        """
        item_list = flatten(*items, except_iterables=[str], max_depth=1)

        args = Arguments([
            p_check(item, typing.Union[ItemParam, Listable], "items") for item in item_list
        ])
        return IfPlayer(
            action=IfPlayerType.CURSOR_ITEM,
            args=args,
            target=self._digest_target(target),
            append_to_reader=False,
            invert=False
        )

    def hotbar_is(
        self, slot: Numeric,
        *, target: typing.Optional[PlayerTarget] = None
    ):
        """Checks if the player's currently selected hotbar slot corresponds with a slot ID between 1 and 9.

        Parameters
        ----------
        slot : :attr:`~.Numeric`
            Slot ID to check.

            .. note::

                - 1 = Leftmost slot
                - 9 = Rightmost slot

        target : Optional[:class:`~.PlayerTarget`], optional
            The target of this :class:`~.IfPlayer`, or None for the current :class:`Player` instance's target.
            Defaults to ``None``.

        Returns
        -------
        :class:`~.IfPlayer`
            The generated IfPlayer instance.

        Examples
        --------
        ::

            with p_default.hotbar_slot_is(5):
            # OR
            with Player(PlayerTarget.DEFAULT).hotbar_slot_is(5):
                # ... code to be executed if the Default Player's currently selected slot is the 5th slot ...
        """
        args = Arguments([
            p_check(slot, Numeric, "slot")
        ])
        return IfPlayer(
            action=IfPlayerType.SLOT_EQUALS,
            args=args,
            target=self._digest_target(target),
            append_to_reader=False,
            invert=False
        )

    # def is_holding_main(self, *, target: typing.Optional[PlayerTarget] = None):
    #     """
    #
    #     Parameters
    #     ----------
    #     target : Optional[:class:`~.PlayerTarget`], optional
    #         The target of this :class:`~.IfPlayer`, or None for the current :class:`Player` instance's target.
    #         Defaults to ``None``.
    #
    #     Returns
    #     -------
    #     :class:`~.IfPlayer`
    #         The generated IfPlayer instance.
    #
    #     Examples
    #     --------
    #     ::
    #
    #         with p_default.is_holding_main():
    #         # OR
    #         with Player(PlayerTarget.DEFAULT).is_holding_main():
    #             # ... code to be executed if the Default Player # TODO: desc.
    #     """
    #     return IfPlayer(
    #         action=IfPlayerType.IS_HOLDING_MAIN,
    #         args=Arguments(),
    #         target=self._digest_target(target),
    #         append_to_reader=False,
    #         invert=False
    #     )

    def is_holding(
            self,
        *items: typing.Optional[typing.Union[ItemParam, ItemCollection, typing.Iterable[ItemParam], Listable]],
        hand: typing.Optional[Hand] = None,
        target: typing.Optional[PlayerTarget] = None
    ):
        """Checks if a player is holding an item in their hand.

        Parameters
        ----------
        items : Optional[Optional[Union[:class:`~.ItemParam`, :class:`~.ItemCollection`, Iterable[:class:`~.ItemParam`], :attr:`Listable`]]], optional
            Item(s) to check for. The items can be specified either as:

            - ``None`` for an empty slot;
            - :class:`~.ItemParam` for one item;
            - :attr:`~.Listable` for a variable list of items;
            - :class:`~.ItemCollection` or Iterable[:class:`~.ItemParam`] for a predetermined list of items.

        hand : Optional[:class:`PlayerHand`]
            The specific hand whose item should be compared against the given items, or ``None`` to compare both hands
            (i.e., accept the player having the item on either hand). Defaults to ``None``.

        target : Optional[:class:`~.PlayerTarget`], optional
            The target of this :class:`~.IfPlayer`, or None for the current :class:`Player` instance's target.
            Defaults to ``None``.

        Returns
        -------
        :class:`~.IfPlayer`
            The generated IfPlayer instance.

        Examples
        --------
        ::

            item_1 = Item(Material.DIAMOND_SWORD)
            item_2 = Item(Material.DIRT, name="some dirt")
            hand = PlayerHand.MAIN_HAND
            with p_default.is_holding(item_1, item_2, hand=hand):
            # OR
            with Player(PlayerTarget.DEFAULT).is_holding(item_1, item_2, hand=hand):
                # ... code to be executed if the Default Player is holding either of the given items on the main hand ...
                # (do not specify - or specify None to - ``hand=`` in order to accept either hand.)
        """
        item_list = flatten(*items, except_iterables=[str], max_depth=1)

        args = Arguments([
            p_check(item, typing.Union[ItemParam, Listable], "items") for item in item_list
        ], tags=[
            Tag(
                "Hand Slot", option="Either Hand" if not hand else Hand(hand).value,  # default is Either Hand
                action=IfPlayerType.IS_HOLDING, block=BlockType.IF_GAME
            )
        ])
        return IfPlayer(
            action=IfPlayerType.IS_HOLDING,
            args=args,
            target=self._digest_target(target),
            append_to_reader=False,
            invert=False
        )

    def menu_slot_equals(
        self, slots: typing.Union[Numeric, Listable, typing.Iterable[Numeric]],
        *items: typing.Optional[typing.Union[ItemParam, ItemCollection, typing.Iterable[ItemParam], Listable]],
        target: typing.Optional[PlayerTarget] = None
    ):
        """Checks if the player's currently open inventory menu contains an item in a specific slot.

        Parameters
        ----------
        slots : Union[:attr:`~.Numeric`, :attr:`~.Listable`, Iterable[:attr:`~.Numeric`]]
            Slot ID(s) to check. Can be either a Numeric, a Listable (list var containing numbers) or an iterable of
            Numeric (e.g.: a list of numbers or number variables).

        items : Optional[Optional[Union[:class:`~.ItemParam`, :class:`~.ItemCollection`, Iterable[:class:`~.ItemParam`], :attr:`Listable`]]], optional
            Item(s) to check for. The items can be specified either as:

            - ``None`` for an empty slot;
            - :class:`~.ItemParam` for one item;
            - :attr:`~.Listable` for a variable list of items;
            - :class:`~.ItemCollection` or Iterable[:class:`~.ItemParam`] for a predetermined list of items.

        target : Optional[:class:`~.PlayerTarget`], optional
            The target of this :class:`~.IfPlayer`, or None for the current :class:`Player` instance's target.
            Defaults to ``None``.

        Returns
        -------
        :class:`~.IfPlayer`
            The generated IfPlayer instance.

        Examples
        --------
        ::

            item_1 = Item(Material.DIAMOND_SWORD)
            item_2 = Item(Material.DIRT, name="my dirt")
            with p_default.menu_slot_equals(5, item_1, item_2):
            # OR
            with Player(PlayerTarget.DEFAULT).menu_slot_equals(5, item_1, item_2):
                # ... code to be executed if the Default Player's currently open menu contains either of the given \
items at slot number 5 ...
                # multiple slots can also be specified with an iterable. E.g. [1, 2, 3, 4] -> one of slots 1,2,3,4
        """
        item_list = flatten(*items, except_iterables=[str], max_depth=1)

        slots_list = [p_check(slot, typing.Union[Numeric, Listable], f"slots[{i}]") for i, slot in enumerate(slots)] \
            if isinstance(slots, collections.Iterable) else [p_check(slots, typing.Union[Numeric, Listable], "slots")]

        args = Arguments([
            *slots_list,
            *[p_check(item, typing.Union[ItemParam, Listable], "items") for item in item_list]
        ])
        return IfPlayer(
            action=IfPlayerType.MENU_SLOT_EQUALS,
            args=args,
            target=self._digest_target(target),
            append_to_reader=False,
            invert=False
        )

    def is_blocking(self, *, target: typing.Optional[PlayerTarget] = None):
        """Checks if a player is blocking with a shield.

        Parameters
        ----------
        target : Optional[:class:`~.PlayerTarget`], optional
            The target of this :class:`~.IfPlayer`, or None for the current :class:`Player` instance's target.
            Defaults to ``None``.

        Returns
        -------
        :class:`~.IfPlayer`
            The generated IfPlayer instance.

        Examples
        --------
        ::

            with p_default.is_blocking():
            # OR
            with Player(PlayerTarget.DEFAULT).is_blocking():
                # ... code to be executed if the Default Player is blocking with a shield ...
        """
        return IfPlayer(
            action=IfPlayerType.IS_BLOCKING,
            args=Arguments(),
            target=self._digest_target(target),
            append_to_reader=False,
            invert=False
        )

    def is_sneaking(self, *, target: typing.Optional[PlayerTarget] = None):
        """Checks if a player is sneaking.

        Parameters
        ----------
        target : Optional[:class:`~.PlayerTarget`], optional
            The target of this :class:`~.IfPlayer`, or None for the current :class:`Player` instance's target.
            Defaults to ``None``.

        Returns
        -------
        :class:`~.IfPlayer`
            The generated IfPlayer instance.

        Examples
        --------
        ::

            with p_default.is_sneaking():
            # OR
            with Player(PlayerTarget.DEFAULT).is_sneaking():
                # ... code to be executed if the Default Player is sneaking ...
        """
        return IfPlayer(
            action=IfPlayerType.IS_SNEAKING,
            args=Arguments(),
            target=self._digest_target(target),
            append_to_reader=False,
            invert=False
        )

    def is_flying(self, *, target: typing.Optional[PlayerTarget] = None):
        """Checks if a player is flying.

        Parameters
        ----------
        target : Optional[:class:`~.PlayerTarget`], optional
            The target of this :class:`~.IfPlayer`, or None for the current :class:`Player` instance's target.
            Defaults to ``None``.

        Returns
        -------
        :class:`~.IfPlayer`
            The generated IfPlayer instance.

        Examples
        --------
        ::

            with p_default.is_flying():
            # OR
            with Player(PlayerTarget.DEFAULT).is_flying():
                # ... code to be executed if the Default Player is flying ...
        """
        return IfPlayer(
            action=IfPlayerType.IS_FLYING,
            args=Arguments(),
            target=self._digest_target(target),
            append_to_reader=False,
            invert=False
        )

    def name_equals(
        self, *names: typing.Union[Textable, Listable],
        target: typing.Optional[PlayerTarget] = None
    ):
        """Checks if a player's username is equal to one of the usernames given (case insensitive).

        Parameters
        ----------
        names : Union[:attr:`~.Textable`, :attr:`~.Listable`]
            Name(s) to check for.

            .. note:: Works with UUIDs.

        target : Optional[:class:`~.PlayerTarget`], optional
            The target of this :class:`~.IfPlayer`, or None for the current :class:`Player` instance's target.
            Defaults to ``None``.

        Returns
        -------
        :class:`~.IfPlayer`
            The generated IfPlayer instance.

        Examples
        --------
        Just specifying each name directly::

            with p_default.name_equals("Bob", "John"):
            # OR
            with Player(PlayerTarget.DEFAULT).name_equals("Bob", "John"):
                # ... code to be executed if the Default Player's name is either Bob or John ...

        Using a predefined list::

            names = ["Bob", John"]
            with p_default.name_equals(names):
            # OR
            with Player(PlayerTarget.DEFAULT).name_equals(names):
                # ... code to be executed if the Default Player's name is either Bob or John ...
                # note that a list variable with the possible names can also be given.
        """
        args = Arguments([
            p_check(name, typing.Union[Textable, Listable], f"names[{i}]") for i, name in enumerate(names)
        ])
        return IfPlayer(
            action=IfPlayerType.NAME_EQUALS,
            args=args,
            target=self._digest_target(target),
            append_to_reader=False,
            invert=False
        )

    def inv_open_type(
        self, inventory_type: IfPOpenInvType = IfPOpenInvType.ANY_INVENTORY,
        target: typing.Optional[PlayerTarget] = None
    ):
        """Checks if a player has a certain inventory type open.

        Parameters
        ----------
        inventory_type : :class:`~.IFPOpenInvType`
            The type of inventory to check for (i.e., check if the player has this type of inventory currently open).
            Defaults to :attr:`~.ANY_INVENTORY` (any inventory type is accepted).

        target : Optional[:class:`~.PlayerTarget`], optional
            The target of this :class:`~.IfPlayer`, or None for the current :class:`Player` instance's target.
            Defaults to ``None``.

        Returns
        -------
        :class:`~.IfPlayer`
            The generated IfPlayer instance.

        Warnings
        --------
        Does not work with special screens such as the death screen, chat box, etc..

        Examples
        --------
        ::

            inv_type = IfPOpenInvType.BLAST_FURNACE  # for example
            with p_default.inv_open_type(inv_type):
            # OR
            with Player(PlayerTarget.DEFAULT).inv_open_type(inv_type):
                # ... code to be executed if the Default Player has a Blast Furnace currently open ...
                # (do not specify any inventory type - or specify ANY_INVENTORY - to check if any inventory is open)
        """
        args = Arguments([], tags=[
            Tag(
                "Inventory Type", option=inventory_type,  # default is Any Inventory
                action=IfPlayerType.INV_OPEN, block=BlockType.IF_GAME
            )
        ])
        return IfPlayer(
            action=IfPlayerType.INV_OPEN,
            args=args,
            target=self._digest_target(target),
            append_to_reader=False,
            invert=False
        )

    def inv_slot_equals(
        self, slots: typing.Union[Numeric, Listable],
        *items: typing.Optional[typing.Union[ItemParam, ItemCollection, typing.Iterable[ItemParam], Listable]],
        target: typing.Optional[PlayerTarget] = None
    ):
        """Checks if a player has an item in a specific inventory slot/one of the given slots.

        Parameters
        ----------
        slots : Union[:attr:`~.Numeric`, :attr:`~.Listable`, Iterable[:attr:`~.Numeric`]]
            Slot ID(s) to check. Can be either a Numeric, a Listable (list var containing numbers) or an iterable of
            Numeric (e.g.: a list of numbers or number variables).

        items : Optional[Optional[Union[:class:`~.ItemParam`, :class:`~.ItemCollection`, Iterable[:class:`~.ItemParam`], :attr:`Listable`]]], optional
            Item(s) to check for. The items can be specified either as:

            - ``None`` for an empty slot;
            - :class:`~.ItemParam` for one item;
            - :attr:`~.Listable` for a variable list of items;
            - :class:`~.ItemCollection` or Iterable[:class:`~.ItemParam`] for a predetermined list of items.

        target : Optional[:class:`~.PlayerTarget`], optional
            The target of this :class:`~.IfPlayer`, or None for the current :class:`Player` instance's target.
            Defaults to ``None``.

        Returns
        -------
        :class:`~.IfPlayer`
            The generated IfPlayer instance.

        Examples
        --------
        ::

            item_1 = Item(Material.STONE)
            item_2 = Item(Material.SNOWBALL)
            with p_default.inv_slot_equals(29, item_1, item_2):
            # OR
            with Player(PlayerTarget.DEFAULT).inv_slot_equals(29, item_1, item_2):
                # ... code to be executed if the Default Player has either of the items at slot 29 ...
                # (you can check multiple slots by giving a list var or an iterable of Numeric instead of slot number.)
        """
        item_list = flatten(*items, except_iterables=[str], max_depth=1)

        slots_list = [p_check(slot, typing.Union[Numeric, Listable], f"slots[{i}]") for i, slot in enumerate(slots)] \
            if isinstance(slots, collections.Iterable) else [p_check(slots, typing.Union[Numeric, Listable], "slots")]

        args = Arguments([
            *slots_list,
            *[p_check(item, typing.Union[ItemParam, Listable], "items") for item in item_list]
        ])
        return IfPlayer(
            action=IfPlayerType.HAS_SLOT_ITEM,
            args=args,
            target=self._digest_target(target),
            append_to_reader=False,
            invert=False
        )

    def is_sprinting(self, *, target: typing.Optional[PlayerTarget] = None):
        """Checks if a player is sprinting or using the sprint key to swim.

        Parameters
        ----------
        target : Optional[:class:`~.PlayerTarget`], optional
            The target of this :class:`~.IfPlayer`, or None for the current :class:`Player` instance's target.
            Defaults to ``None``.

        Returns
        -------
        :class:`~.IfPlayer`
            The generated IfPlayer instance.

        Examples
        --------
        ::

            with p_default.is_sprinting():
            # OR
            with Player(PlayerTarget.DEFAULT).is_sprinting():
                # ... code to be executed if the Default Player is sprinting, or, if swimming, is using the swm animation ...
        """
        return IfPlayer(
            action=IfPlayerType.IS_SPRINTING,
            args=Arguments(),
            target=self._digest_target(target),
            append_to_reader=False,
            invert=False
        )

    def is_gliding(self, *, target: typing.Optional[PlayerTarget] = None):
        """Checks if a player is gliding with elytra.

        Parameters
        ----------
        target : Optional[:class:`~.PlayerTarget`], optional
            The target of this :class:`~.IfPlayer`, or None for the current :class:`Player` instance's target.
            Defaults to ``None``.

        Returns
        -------
        :class:`~.IfPlayer`
            The generated IfPlayer instance.

        Examples
        --------
        ::

            with p_default.is_gliding():
            # OR
            with Player(PlayerTarget.DEFAULT).is_gliding():
                # ... code to be executed if the Default Player is gliding with an Elytra ...
        """
        return IfPlayer(
            action=IfPlayerType.IS_GLIDING,
            args=Arguments(),
            target=self._digest_target(target),
            append_to_reader=False,
            invert=False
        )

    # def cmd_arg_equals(
    #         self, *texts: typing.Union[Textable, Listable], arg_num: Numeric,
    #         ignore_case: bool = True,
    #         target: typing.Optional[PlayerTarget] = None
    # ):
    #     """Checks if a certain argument of a player's command is equal to a certain text when the Player Command Event is executed.
    #
    #     .. rank:: Emperor
    #
    #     .. workswith:: Player Command Event
    #
    #     Parameters
    #     ----------
    #     texts : Union[:attr:`~.Textable`, :attr:`~.Listable`]
    #         Text(s) to check for.
    #
    #     arg_num : :attr:`~.Numeric`
    #         Argument number.
    #
    #     ignore_case : :class:`bool`, optional
    #         Defaults to ``True``.
    #
    #     target : Optional[:class:`~.PlayerTarget`], optional
    #         The target of this :class:`~.IfPlayer`, or None for the current :class:`Player` instance's target.
    #         Defaults to ``None``.
    #
    #     Returns
    #     -------
    #     :class:`~.IfPlayer`
    #         The generated IfPlayer instance.
    #
    #     Examples
    #     --------
    #     ::
    #
    #         with p_default.cmd_arg_equals(texts, arg_num):
    #         # OR
    #         with Player(PlayerTarget.DEFAULT).cmd_arg_equals(texts, arg_num):
    #             # ... code to be executed if the Default Player # TODO: Example
    #     """
    #     args = Arguments([
    #         *[p_check(text, typing.Union[Textable, Listable], f"texts[{i}]") for i, text in enumerate(texts)],
    #         p_check(arg_num, Numeric, "arg_num")
    #     ], tags=[
    #         Tag(
    #             "Ignore Case", option=bool(ignore_case),  # default is True
    #             action=IfPlayerType.CMD_ARG_EQUALS, block=BlockType.IF_GAME
    #         )
    #     ])
    #     return IfPlayer(
    #         action=IfPlayerType.CMD_ARG_EQUALS,
    #         args=args,
    #         target=self._digest_target(target),
    #         append_to_reader=False,
    #         invert=False
    #     )
    
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

    def armor_stand_tags(
        self,
        *, is_visible: typing.Optional[bool] = None, is_marker: typing.Optional[bool] = None,
        allow_item_taking_or_adding: typing.Optional[bool] = None,
        has_physics_or_updates: typing.Optional[bool] = None, is_small: typing.Optional[bool] = None,
        has_arms: typing.Optional[bool] = None, has_base_plate: typing.Optional[bool] = None,
        target: typing.Optional[EntityTarget] = None
    ):
        """Changes the settings of an armor stand, such as visibility.

        .. rank:: Mythic


        Parameters
        ----------
        is_visible : Optional[:class:`bool`], optional
            Whether this Armor Stand is visible.
            Specify ``True`` or ``False`` to change this setting, or ``None`` to leave it untouched. Defaults to
            ``None``.

        is_marker : Optional[:class:`bool`], optional
            Whether this Armor Stand is a marker (has no hitbox).
            Specify ``True`` or ``False`` to change this setting, or ``None`` to leave it untouched. Defaults to
            ``None``.

        allow_item_taking_or_adding : Optional[:class:`bool`], optional
            Whether this armor stand should have item taking/adding allowed.
            Specify ``True`` or ``False`` to change this setting, or ``None`` to leave it untouched. Defaults to
            ``None``.

        has_physics_or_updates : Optional[:class:`bool`], optional
            Specify ``True`` or ``False`` to change this setting, or ``None`` to leave it untouched. Defaults to
            ``None``.

        is_small : Optional[:class:`bool`], optional
            Specify ``True`` or ``False`` to change this setting, or ``None`` to leave it untouched. Defaults to
            ``None``.

        has_arms : Optional[:class:`bool`], optional
            Specify ``True`` or ``False`` to change this setting, or ``None`` to leave it untouched. Defaults to
            ``None``.

        has_base_plate : Optional[:class:`bool`], optional
            Specify ``True`` or ``False`` to change this setting, or ``None`` to leave it untouched. Defaults to
            ``None``.

        target : Optional[:class:`~.EntityTarget`], optional
            The target of this :class:`~.EntityAction`, or None for the current :class:`Entity` instance's target.
            Defaults to ``None``.

        Returns
        -------
        :class:`EntityAction`
            The generated EntityAction instance.

        Examples
        --------
        ::

            last_entity.armor_stand_tags(is_visible=True, has_physics_or_updates=False)  # selects last spawned entity
            # OR
            Entity(EntityTarget.LAST_ENTITY).armor_stand_tags(is_visible=True, has_physics_or_updates=False)
            # Makes the armor stand visible and makes it not affected by physics or updates; other params unchanged
        """
        args = Arguments([], tags=[  # Set to True, Set to False, Don't Change
            Tag(
                "Is Visible",
                option="Set to True" if is_visible else (
                    "Set to False" if is_visible is not None else "Don't Change"
                ),  # default is Don't Change
                action=EntityActionType.ARMOR_STAND_TAGS, block=BlockType.IF_GAME
            ),
            Tag(
                "Is Marker (No Hitbox)",
                option="Set to True" if is_marker else (
                    "Set to False" if is_marker is not None else "Don't Change"
                ),  # default is Don't Change
                action=EntityActionType.ARMOR_STAND_TAGS, block=BlockType.IF_GAME
            ),
            Tag(
                "Allow Item Taking / Adding",
                option="Set to True" if allow_item_taking_or_adding else (
                    "Set to False" if allow_item_taking_or_adding is not None else "Don't Change"
                ),  # default is Don't Change
                action=EntityActionType.ARMOR_STAND_TAGS, block=BlockType.IF_GAME
            ),
            Tag(
                "Has Physics / Updates",
                option="Set to True" if has_physics_or_updates else (
                    "Set to False" if has_physics_or_updates is not None else "Don't Change"
                ),  # default is Don't Change
                action=EntityActionType.ARMOR_STAND_TAGS, block=BlockType.IF_GAME
            ),
            Tag(
                "Is Small",
                option="Set to True" if is_small else (
                    "Set to False" if is_small is not None else "Don't Change"
                ),  # default is Don't Change
                action=EntityActionType.ARMOR_STAND_TAGS, block=BlockType.IF_GAME
            ),
            Tag(
                "Has Arms",
                option="Set to True" if has_arms else (
                    "Set to False" if has_arms is not None else "Don't Change"
                ),  # default is Don't Change
                action=EntityActionType.ARMOR_STAND_TAGS, block=BlockType.IF_GAME
            ),
            Tag(
                "Has Base Plate",
                option="Set to True" if has_base_plate else (
                    "Set to False" if has_base_plate is not None else "Don't Change"
                ),  # default is Don't Change
                action=EntityActionType.ARMOR_STAND_TAGS, block=BlockType.IF_GAME
            )
        ])
        return EntityAction(
            action=EntityActionType.ARMOR_STAND_TAGS,
            args=args,
            target=self._digest_target(target),
            append_to_reader=True
        )

    def block_disguise(
        self, block_type: BlockParam, name: typing.Optional[Textable] = None,
        *, target: typing.Optional[EntityTarget] = None
    ):
        """Disguises the entity as a block.

        .. rank:: Overlord


        Parameters
        ----------
        block_type : Union[:class:`Material`, :attr:`~.ItemParam`, :attr:`~.Textable`]
            The type of Block disguise.

            The type can be specified either as:

            - an instance of :class:`~.Material` (the material of the block to set);
            - an item (:attr:`~.ItemParam` - the item representing the block to set);
            - text (:attr:`~.Textable` - the material of the block to set as text).

        name : Optional[:attr:`~.Textable`], optional
            Name of disguise. Default is ``None`` (no special name).

        target : Optional[:class:`~.EntityTarget`], optional
            The target of this :class:`~.EntityAction`, or None for the current :class:`Entity` instance's target.
            Defaults to ``None``.

        Returns
        -------
        :class:`EntityAction`
            The generated EntityAction instance.

        Examples
        --------
        ::

            block_type = Material.GRASS_BLOCK  # disguise as a grass block
            last_entity.block_disguise(block_type, "Some Block")
            # OR
            Entity(EntityTarget.LAST_ENTITY).block_disguise(block_type, "Some Block)
            # last spawned entity is disguised as a grass block named "Some Block"
        """
        args = Arguments([
            p_check(block_type, typing.Union[ItemParam, Textable], "block_type"),
            p_check(name, typing.Optional[Textable], "name") if name is not None else None
        ])
        return EntityAction(
            action=EntityActionType.BLOCK_DISGUISE,
            args=args,
            target=self._digest_target(target),
            append_to_reader=True
        )

    def set_creeper_charged(
        self, is_charged: bool = True,
        *, target: typing.Optional[EntityTarget] = None
    ):
        """Sets whether a creeper has the charged effect.

        Parameters
        ----------
        is_charged : :class:`bool`, optional
            Whether or not the target creeper should be target. Defaults to ``True`` (should be charged).

        target : Optional[:class:`~.EntityTarget`], optional
            The target of this :class:`~.EntityAction`, or None for the current :class:`Entity` instance's target.
            Defaults to ``None``.

        Returns
        -------
        :class:`EntityAction`
            The generated EntityAction instance.

        Examples
        --------
        ::

            last_entity.creeper_charged(True)
            # OR
            Entity(EntityTarget.LAST_ENTITY).creeper_charged(True)
            # Creeper is now charged; False for not charged.
        """
        args = Arguments([], tags=[
            Tag(
                "Is Charged", option=bool(is_charged),  # default is True
                action=EntityActionType.CREEPER_CHARGED, block=BlockType.IF_GAME
            )
        ])
        return EntityAction(
            action=EntityActionType.CREEPER_CHARGED,
            args=args,
            target=self._digest_target(target),
            append_to_reader=True
        )

    def set_creeper_ignited(
        self, is_ignited: bool = True,
        *, target: typing.Optional[EntityTarget] = None
    ):
        """Sets whether a creeper is currently ignited. (getting ready to explode)

        Parameters
        ----------
        is_ignited : :class:`bool`, optional
            Whether or not the Creeper is ignited. Defaults to ``True`` (is ignited).

        target : Optional[:class:`~.EntityTarget`], optional
            The target of this :class:`~.EntityAction`, or None for the current :class:`Entity` instance's target.
            Defaults to ``None``.

        Returns
        -------
        :class:`EntityAction`
            The generated EntityAction instance.

        Examples
        --------
        ::

            last_mob.set_creeper_ignited(True)  # works if last mob spawned is a creeper
            # OR
            Entity(EntityTarget.LAST_MOB).set_creeper_ignited(True)  # creeper is now ignited; False for not ignited
        """
        args = Arguments([], tags=[
            Tag(
                "Is Ignited", option=bool(is_ignited),  # default is True
                action=EntityActionType.CREEPER_IGNITED, block=BlockType.IF_GAME
            )
        ])
        return EntityAction(
            action=EntityActionType.CREEPER_IGNITED,
            args=args,
            target=self._digest_target(target),
            append_to_reader=True
        )

    def set_creeper_max_fuse(
        self, ticks: Numeric,
        *, target: typing.Optional[EntityTarget] = None
    ):
        """Sets the starting amount of fuse ticks of a creeper.

        Parameters
        ----------
        ticks : :attr:`~.Numeric`
            Fuse ticks.

        target : Optional[:class:`~.EntityTarget`], optional
            The target of this :class:`~.EntityAction`, or None for the current :class:`Entity` instance's target.
            Defaults to ``None``.

        Returns
        -------
        :class:`EntityAction`
            The generated EntityAction instance.

        Examples
        --------
        ::

            last_mob.set_creeper_max_fuse(40)  # if last mob spawned is a creeper, this will work
            # OR
            Entity(EntityTarget.LAST_MOB).set_creeper_max_fuse(40)  # fuse is now 2 seconds
        """
        args = Arguments([
            p_check(ticks, Numeric, "ticks")
        ])
        return EntityAction(
            action=EntityActionType.CREEPER_MAX_FUSE,
            args=args,
            target=self._digest_target(target),
            append_to_reader=True
        )

    def set_creeper_radius(
        self, radius: Numeric,
        *, target: typing.Optional[EntityTarget] = None
    ):
        """Sets the explosion radius of a creeper.

        Parameters
        ----------
        radius : :attr:`~.Numeric`
            The new explosion radius.

            .. note::

                The maximum radius is 25.

        target : Optional[:class:`~.EntityTarget`], optional
            The target of this :class:`~.EntityAction`, or None for the current :class:`Entity` instance's target.
            Defaults to ``None``.

        Returns
        -------
        :class:`EntityAction`
            The generated EntityAction instance.

        Raises
        ------
        :exc:`ValueError`
            If the explosion radius is not within the range `0 <= radius <= 25`.

        Examples
        --------
        ::

            last_mob.set_creeper_radius(5)
            # OR
            Entity(EntityTarget.LAST_MOB).set_creeper_radius(5)  # the last spawned mob, if a creeper, now has its
                                                                 # explosion radius set to 5 blocks wide.
        """
        if isinstance(radius, (int, float, DFNumber)) and not 0 <= radius <= 25:
            raise ValueError("Invalid creeper explosion radius (must be between 0 and 25).")

        args = Arguments([
            p_check(radius, Numeric, "radius")
        ])
        return EntityAction(
            action=EntityActionType.CREEPER_RADIUS,
            args=args,
            target=self._digest_target(target),
            append_to_reader=True
        )

    def damage(
        self, damage: Numeric,
        *, target: typing.Optional[EntityTarget] = None
    ):
        """Damages the mob.

        Parameters
        ----------
        damage : :attr:`~.Numeric`
            Damage to inflict.

            .. note::

                1 damage = 0.5 hearts


        target : Optional[:class:`~.EntityTarget`], optional
            The target of this :class:`~.EntityAction`, or None for the current :class:`Entity` instance's target.
            Defaults to ``None``.

        Returns
        -------
        :class:`EntityAction`
            The generated EntityAction instance.

        Examples
        --------
        ::

            last_entity.damage(6)
            # OR
            Entity(EntityTarget.LAST_ENTITY).damage(6)  # deals 3 hearts of damage to the last spawned entity
        """
        args = Arguments([
            p_check(damage, Numeric, "damage")
        ])
        return EntityAction(
            action=EntityActionType.DAMAGE,
            args=args,
            target=self._digest_target(target),
            append_to_reader=True
        )

    def disable_glowing(self, *, target: typing.Optional[EntityTarget] = None):
        """Makes the entity no longer glow.

        Parameters
        ----------
        target : Optional[:class:`~.EntityTarget`], optional
            The target of this :class:`~.EntityAction`, or None for the current :class:`Entity` instance's target.
            Defaults to ``None``.

        Returns
        -------
        :class:`EntityAction`
            The generated EntityAction instance.

        Examples
        --------
        ::

            last_entity.disable_glowing()
            # OR
            Entity(EntityTarget.LAST_ENTITY).disable_glowing()
        """
        return EntityAction(
            action=EntityActionType.DISABLE_GLOWING,
            args=Arguments(),
            target=self._digest_target(target),
            append_to_reader=True
        )

    def enable_drop_items(self, *, target: typing.Optional[EntityTarget] = None):
        """After this code block is executed, the mob will drop their equipment and loot when they die.

        Parameters
        ----------
        target : Optional[:class:`~.EntityTarget`], optional
            The target of this :class:`~.EntityAction`, or None for the current :class:`Entity` instance's target.
            Defaults to ``None``.

        Returns
        -------
        :class:`EntityAction`
            The generated EntityAction instance.

        Examples
        --------
        ::

            last_entity.enable_drop_items()
            # OR
            Entity(EntityTarget.LAST_ENTITY).enable_drop_items()
        """
        return EntityAction(
            action=EntityActionType.DROP_ITEMS,
            args=Arguments(),
            target=self._digest_target(target),
            append_to_reader=True
        )

    def enable_ai(self, *, target: typing.Optional[EntityTarget] = None):
        """Enables the AI of the mob.

        .. rank:: Noble


        Parameters
        ----------
        target : Optional[:class:`~.EntityTarget`], optional
            The target of this :class:`~.EntityAction`, or None for the current :class:`Entity` instance's target.
            Defaults to ``None``.

        Returns
        -------
        :class:`EntityAction`
            The generated EntityAction instance.

        Examples
        --------
        ::

            last_entity.enable_ai()
            # OR
            Entity(EntityTarget.LAST_ENTITY).enable_ai()
        """
        return EntityAction(
            action=EntityActionType.ENABLE_AI,
            args=Arguments(),
            target=self._digest_target(target),
            append_to_reader=True
        )

    def enable_glowing(self, *, target: typing.Optional[EntityTarget] = None):
        """Makes the entity glow.

        Parameters
        ----------
        target : Optional[:class:`~.EntityTarget`], optional
            The target of this :class:`~.EntityAction`, or None for the current :class:`Entity` instance's target.
            Defaults to ``None``.

        Returns
        -------
        :class:`EntityAction`
            The generated EntityAction instance.

        Examples
        --------
        ::

            last_entity.enable_glowing()
            # OR
            Entity(EntityTarget.LAST_ENTITY).enable_glowing()
        """
        return EntityAction(
            action=EntityActionType.ENABLE_GLOWING,
            args=Arguments(),
            target=self._digest_target(target),
            append_to_reader=True
        )

    def set_end_crystal_target(
        self, loc: typing.Optional[Locatable] = None,
        *, target: typing.Optional[EntityTarget] = None
    ):
        """Sets an end crystal's beam target.

        Parameters
        ----------
        loc : Optional[:attr:`~.Locatable`], optional
            The end crystal beam's new target, or ``None`` to remove the beam. Default is ``None``.

            .. note::

                - To remove the beam, specify ``None`` (i.e., not a location).
                - The target location is rounded to the nearest block.

        target : Optional[:class:`~.EntityTarget`], optional
            The target of this :class:`~.EntityAction`, or None for the current :class:`Entity` instance's target.
            Defaults to ``None``.

        Returns
        -------
        :class:`EntityAction`
            The generated EntityAction instance.

        Examples
        --------
        ::

            loc = DFLocation(1, 2, 3)  # location of the new beam target
            last_entity.set_end_crystal_target(loc)
            # OR
            Entity(EntityTarget.LAST_ENTITY).set_end_crystal_target(loc)  # sets the last spawned entity's beam target,
                                                                          # should it be an ender crystal.
        """
        args = Arguments([
            p_check(loc, typing.Optional[Locatable], "loc") if loc is not None else None
        ])
        return EntityAction(
            action=EntityActionType.END_CRYSTAL_TARGET,
            args=args,
            target=self._digest_target(target),
            append_to_reader=True
        )

    def explode_creeper(self, *, target: typing.Optional[EntityTarget] = None):
        """Causes a creeper to instantly explode.

        Parameters
        ----------
        target : Optional[:class:`~.EntityTarget`], optional
            The target of this :class:`~.EntityAction`, or None for the current :class:`Entity` instance's target.
            Defaults to ``None``.

        Returns
        -------
        :class:`EntityAction`
            The generated EntityAction instance.

        Examples
        --------
        ::

            last_mob.explode_creeper()
            # OR
            Entity(EntityTarget.LAST_MOB).explode_creeper()
        """
        return EntityAction(
            action=EntityActionType.EXPLODE_CREEPER,
            args=Arguments(),
            target=self._digest_target(target),
            append_to_reader=True
        )

    def give_effect(
        self, *potions: typing.Union[Potionable, Listable],
        effect_particle_mode: EffectParticleMode = EffectParticleMode.SHOWN,
        overwrite_existing_effect: bool = False,
        target: typing.Optional[EntityTarget] = None
    ):
        """Gives the mob one or more potion effects.

        Parameters
        ----------
        potions : Union[:attr:`~.Potionable`, :attr:`~.Listable`]
            Potion effect(s) to give, or a List variable with all the potion effects.

        effect_particle_mode : :class:`~.EffectParticleMode`, optional
            The mode applied to the effect particles (either :attr:`~.EffectParticleMode.SHOWN`,
            :attr:`~.EffectParticleMode.BEACON` or :attr:`~.EffectParticleMode.HIDDEN`). Defaults to
            :attr:`~.EffectParticleMode.SHOWN`.

        overwrite_existing_effect : :class:`bool`, optional
            If existing effects should be overridden by the given ones. Defaults to ``False`` (no).

        target : Optional[:class:`~.EntityTarget`], optional
            The target of this :class:`~.EntityAction`, or None for the current :class:`Entity` instance's target.
            Defaults to ``None``.

        Returns
        -------
        :class:`EntityAction`
            The generated EntityAction instance.

        Examples
        --------
        ::

            potion_1 = DFPotion(PotionEffect.ABSORPTION, amplifier=255, duration=(5, 0))  # Absorption 255, 5 min dur.
            potion_2 = PotionVar("my var")  # potion variable
            last_entity.give_effect(potion_1, potion_2, effect_particle_mode=EffectParticleMode.BEACON)
            # OR
            Entity(EntityTarget.LAST_ENTITY).give_effect(potion_1, potion_2, effect_particle_mode=EffectParticleMode.BEACON)
            # gives two potion effects with beacon-mode particles.
        """
        args = Arguments([
            p_check(potion, typing.Union[Potionable, Listable], f"potions[{i}]") for i, potion in enumerate(potions)
        ], tags=[
            Tag(
                "Effect Particle Mode", option=effect_particle_mode,  # default is Shown
                action=EntityActionType.GIVE_EFFECT, block=BlockType.IF_GAME
            ),
            Tag(
                "Overwrite Existing Effect", option=bool(overwrite_existing_effect),  # default is False
                action=EntityActionType.GIVE_EFFECT, block=BlockType.IF_GAME
            )
        ])
        return EntityAction(
            action=EntityActionType.GIVE_EFFECT,
            args=args,
            target=self._digest_target(target),
            append_to_reader=True
        )

    def enable_gravity(self, *, target: typing.Optional[EntityTarget] = None):
        """Enables gravity for the entity.

        .. rank:: Overlord


        Parameters
        ----------
        target : Optional[:class:`~.EntityTarget`], optional
            The target of this :class:`~.EntityAction`, or None for the current :class:`Entity` instance's target.
            Defaults to ``None``.

        Returns
        -------
        :class:`EntityAction`
            The generated EntityAction instance.

        Examples
        --------
        ::

            last_entity.enable_gravity()
            # OR
            Entity(EntityTarget.LAST_ENTITY).enable_gravity()
        """
        return EntityAction(
            action=EntityActionType.GRAVITY,
            args=Arguments(),
            target=self._digest_target(target),
            append_to_reader=True
        )

    def heal(
        self, amount: typing.Optional[Numeric] = None,
        *, target: typing.Optional[EntityTarget] = None
    ):
        """Restores the mob's health fully or by an amount.

        Parameters
        ----------
        amount : Optional[:attr:`~.Numeric`], optional
            Amount to heal, or ``None`` to restore fully. Default is ``None`` (restore all of the mob's health).

            .. note::

                1 health = 0.5 hearts


        target : Optional[:class:`~.EntityTarget`], optional
            The target of this :class:`~.EntityAction`, or None for the current :class:`Entity` instance's target.
            Defaults to ``None``.

        Returns
        -------
        :class:`EntityAction`
            The generated EntityAction instance.

        Examples
        --------
        ::

            last_entity.heal(6)
            # OR
            Entity(EntityTarget.LAST_ENTITY).heal(6)  # Heals 3 hearts (+3 added)
            # do not specify anything to heal entirely
        """
        args = Arguments([
            p_check(amount, typing.Optional[Numeric], "amount") if amount is not None else None
        ])
        return EntityAction(
            action=EntityActionType.HEAL,
            args=args,
            target=self._digest_target(target),
            append_to_reader=True
        )

    def hide_name(self, *, target: typing.Optional[EntityTarget] = None):
        """Hides the name tag of the entity.

        Parameters
        ----------
        target : Optional[:class:`~.EntityTarget`], optional
            The target of this :class:`~.EntityAction`, or None for the current :class:`Entity` instance's target.
            Defaults to ``None``.

        Returns
        -------
        :class:`EntityAction`
            The generated EntityAction instance.

        Examples
        --------
        ::

            last_entity.hide_name()
            # OR
            Entity(EntityTarget.LAST_ENTITY).hide_name()
        """
        return EntityAction(
            action=EntityActionType.HIDE_NAME,
            args=Arguments(),
            target=self._digest_target(target),
            append_to_reader=True
        )

    def set_horse_appearance(
        self,
        *, horse_color: typing.Optional[HorseColor] = None,
        horse_variant: typing.Optional[HorseVariant] = None,
        target: typing.Optional[EntityTarget] = None
    ):
        """Sets the appearance (the variant) of a horse.

        Parameters
        ----------
        horse_color : Optional[:class:`~.HorseColor`]
            The new color of the horse, or ``None`` to keep unchanged. Defaults to ``None``.

        horse_variant : Optional[:class:`~.HorseVariant`]
            The new variant of the horse, or ``None`` to keep unchanged. Defaults to ``None``.

            .. warning::

                For no variant, specify :attr:`~.HorseVariant.NONE`, not ``None`` (``None`` is to keep unchanged).

        target : Optional[:class:`~.EntityTarget`], optional
            The target of this :class:`~.EntityAction`, or None for the current :class:`Entity` instance's target.
            Defaults to ``None``.

        Returns
        -------
        :class:`EntityAction`
            The generated EntityAction instance.

        Examples
        --------
        ::

            h_color = HorseColor.CHESTNUT  # new color: chestnut
            h_variant = HorseVariant.WHITE  # new variant: white
            last_mob.set_horse_appearance(horse_color=h_color, horse_variant=h_variant)
            # OR
            Entity(EntityTarget.LAST_MOB).set_horse_appearance(horse_color=h_color, horse_variant=h_variant)
            # If the last mob is a horse, then its color and variant are set accordingly.
        """
        args = Arguments([], tags=[
            Tag(
                "Horse Color", option=HorseColor(horse_color) if horse_color else "Don't Change",
                action=EntityActionType.HORSE_APPEARANCE, block=BlockType.IF_GAME
            ),
            Tag(
                "Horse Variant", option=HorseVariant(horse_variant) if horse_variant else "Don't Change",
                action=EntityActionType.HORSE_APPEARANCE, block=BlockType.IF_GAME
            )
        ])
        return EntityAction(
            action=EntityActionType.HORSE_APPEARANCE,
            args=args,
            target=self._digest_target(target),
            append_to_reader=True
        )

    def set_jump_strength(
        self, strength: Numeric,
        *, target: typing.Optional[EntityTarget] = None
    ):
        """Sets the jump strength of a horse.

        .. workswith:: Horse, Donkey, Mule, Llama, Trader Llama, Skeleton Horse, Zombie Horse

        Parameters
        ----------
        strength : :attr:`~.Numeric`
            The new jump strength.

            .. note::

                - A jump strength of 0 will prevent jumping.
                - Must be between 0 and 2, otherwise a ValueError is raised (if a constant is specified, i.e., not
                a variable).


        target : Optional[:class:`~.EntityTarget`], optional
            The target of this :class:`~.EntityAction`, or None for the current :class:`Entity` instance's target.
            Defaults to ``None``.

        Returns
        -------
        :class:`EntityAction`
            The generated EntityAction instance.

        Raises
        ------
        :exc:`ValueError`
            If `strength` is not between 0 and 2.

        Examples
        --------
        ::

            last_entity.set_jump_strength(2)
            # OR
            Entity(EntityTarget.LAST_ENTITY).set_jump_strength(2)  # last spawned mob, if horse, now has jump strength of 2
        """
        if isinstance(strength, (int, float, DFNumber)) and not 0 <= strength <= 2:
            raise ValueError("Invalid jump strength (must be between 0 and 2).")

        args = Arguments([
            p_check(strength, Numeric, "strength")
        ])
        return EntityAction(
            action=EntityActionType.JUMP_STRENGTH,
            args=args,
            target=self._digest_target(target),
            append_to_reader=True
        )

    def launch_fwd(
        self, power: Numeric,
        *, yaw_only: bool = False,
        target: typing.Optional[EntityTarget] = None
    ):
        """Launches the entity a certain amount forward or backward.

        Parameters
        ----------
        power : :attr:`~.Numeric`
            Launch power.

            .. note::

                A positive launch power is forward, and a negative one is backward.

        yaw_only : :class:`bool`, optional
            If ``True``, only yaw is considered on launch axis. If ``False``, pitch is also considered. Defaults
            to ``False``.

        target : Optional[:class:`~.EntityTarget`], optional
            The target of this :class:`~.EntityAction`, or None for the current :class:`Entity` instance's target.
            Defaults to ``None``.

        Returns
        -------
        :class:`EntityAction`
            The generated EntityAction instance.

        Examples
        --------
        ::

            last_entity.launch_fwd(5)
            # OR
            Entity(EntityTarget.LAST_ENTITY).launch_fwd(5)  # launches last spawned mob forward with a power of 5
            # -5 for backwards with same power
        """
        args = Arguments([
            p_check(power, Numeric, "power")
        ], tags=[
            Tag(
                "Launch Axis", option="Yaw Only" if yaw_only else "Pitch and Yaw",  # default is Pitch and Yaw
                action=EntityActionType.LAUNCH_FWD, block=BlockType.IF_GAME
            )
        ])
        return EntityAction(
            action=EntityActionType.LAUNCH_FWD,
            args=args,
            target=self._digest_target(target),
            append_to_reader=True
        )

    def launch_projectile(
        self, projectile: BlockParam, *, loc: typing.Optional[Locatable] = None,
        name: typing.Optional[Textable] = None, speed: typing.Optional[Numeric] = None,
        inaccuracy: typing.Optional[Numeric] = None, particle: typing.Optional[ParticleParam] = None,
        target: typing.Optional[EntityTarget] = None
    ):
        """Launches a projectile from the mob.

        Parameters
        ----------
        projectile : Union[:class:`Material`, :attr:`~.ItemParam`, :attr:`~.Textable`]
            The type of Projectile to launch.

            The type can be specified either as:

            - an instance of :class:`~.Material` (the material of the block to set);
            - an item (:attr:`~.ItemParam` - the item representing the block to set);
            - text (:attr:`~.Textable` - the material of the block to set as text).

        loc : Optional[:attr:`~.Locatable`], optional
            Launch point (where the projectile is launched from). Default is ``None`` (from the mob in a predetermined
            spot).

        name : Optional[:attr:`~.Textable`], optional
            Projectile name. Default is ``None`` (no name).

        speed : Optional[:attr:`~.Numeric`], optional
            The projectile's speed. Default is ``None`` (default speed).

            .. note::

                This has to be specified in order for `inaccuracy` to be given, or a :exc:`ValueError` is raised.

        inaccuracy : Optional[:attr:`~.Numeric`], optional
            Inaccuracy (how much random momentum is applied on launch), or ``None`` for the default (1).
            Default is ``None`` (1).

        particle : Optional[:attr:`~.ParticleParam`], optional
            A particle to be the projectile's launch trail. Default is ``None`` (no launch trail).

        target : Optional[:class:`~.EntityTarget`], optional
            The target of this :class:`~.EntityAction`, or None for the current :class:`Entity` instance's target.
            Defaults to ``None``.

        Returns
        -------
        :class:`EntityAction`
            The generated EntityAction instance.

        Raises
        ------
        :exc:`ValueError`
            Raised if `inaccuracy` was specified, while `speed` was not.

        Examples
        --------
        ::

            proj = Material.ARROW  # launch an arrow from the mob
            partc = ParticleType.BUBBLE  # bubble trail
            last_entity.launch_projectile(proj, name="My Arrow", speed=5, inaccuracy=2, particle=partc)
            # OR
            Entity(EntityTarget.LAST_ENTITY).launch_projectile(proj, name="My Arrow", speed=5, inaccuracy=2, particle=partc)
        """
        if inaccuracy is not None and speed is None:
            raise ValueError("Cannot specify 'inaccuracy' argument without specifying 'speed'.")

        args = Arguments([
            p_check(projectile, typing.Union[ItemParam, Textable], "projectile"),
            p_check(loc, typing.Optional[Locatable], "loc") if loc is not None else None,
            p_check(name, typing.Optional[Textable], "name") if name is not None else None,
            p_check(speed, typing.Optional[Numeric], "speed") if speed is not None else None,
            p_check(inaccuracy, typing.Optional[Numeric], "inaccuracy") if inaccuracy is not None else None,
            p_check(particle, typing.Optional[ParticleParam], "particle") if particle is not None else None
        ])
        return EntityAction(
            action=EntityActionType.LAUNCH_PROJ,
            args=args,
            target=self._digest_target(target),
            append_to_reader=True
        )

    def launch_toward(
        self, loc: Locatable, power: typing.Optional[Numeric] = None,
        *, ignore_distance: bool = False,
        target: typing.Optional[EntityTarget] = None
    ):
        """Launches the entity toward a certain location.

        Parameters
        ----------
        loc : :attr:`~.Locatable`
            Launch destination.

        power : Optional[:attr:`~.Numeric`], optional
            Launch power. Default is ``None`` (a default value is assigned for power).

            .. note:;

                A negative launch power will launch the entity away from the location.

        ignore_distance : :class:`bool`, optional
            If the distance between the entity and the location should be ignored when calculating the strength of the
            pull. Defaults to ``False``.

        target : Optional[:class:`~.EntityTarget`], optional
            The target of this :class:`~.EntityAction`, or None for the current :class:`Entity` instance's target.
            Defaults to ``None``.

        Returns
        -------
        :class:`EntityAction`
            The generated EntityAction instance.

        Examples
        --------
        ::

            loc = DFLocation(1, 2, 3)  # the location where to launch towards
            last_entity.launch_toward(loc, 10)
            # OR
            Entity(EntityTarget.LAST_ENTITY).launch_toward(loc, 10)  # launch last spawned entity towards location
                                                                     # with a power of 10
        """
        args = Arguments([
            p_check(loc, Locatable, "loc"),
            p_check(power, typing.Optional[Numeric], "power") if power is not None else None
        ], tags=[
            Tag(
                "Ignore Distance", option=bool(ignore_distance),  # default is False
                action=EntityActionType.LAUNCH_TOWARD, block=BlockType.IF_GAME
            )
        ])
        return EntityAction(
            action=EntityActionType.LAUNCH_TOWARD,
            args=args,
            target=self._digest_target(target),
            append_to_reader=True
        )

    def launch_up(
        self, power: Numeric,
        *, target: typing.Optional[EntityTarget] = None
    ):
        """Launches the entity a certain amount up or down. A positive amount is up, and a negative amount is down.

        Parameters
        ----------
        power : :attr:`~.Numeric`
            Launch power.

        target : Optional[:class:`~.EntityTarget`], optional
            The target of this :class:`~.EntityAction`, or None for the current :class:`Entity` instance's target.
            Defaults to ``None``.

        Returns
        -------
        :class:`EntityAction`
            The generated EntityAction instance.

        Examples
        --------
        ::

            last_entity.launch_up(10)
            # OR
            Entity(EntityTarget.LAST_ENTITY).launch_up(10)  # Launches the entity up with power 10 (use -10 for down).
        """
        args = Arguments([
            p_check(power, Numeric, "power")
        ])
        return EntityAction(
            action=EntityActionType.LAUNCH_UP,
            args=args,
            target=self._digest_target(target),
            append_to_reader=True
        )

    def mob_disguise(
        self, spawn_egg: SpawnEggable, name: typing.Optional[Textable] = None,
        *, target: typing.Optional[EntityTarget] = None
    ):
        """Disguises the entity as a mob.

        .. rank:: Overlord


        Parameters
        ----------
        spawn_egg : :attr:`~.SpawnEggable`
            Mob to disguise as (a spawn egg).

        name : Optional[:attr:`~.Textable`], optional
            Disguise name (of the mob). Default is ``None`` (no name).

        target : Optional[:class:`~.EntityTarget`], optional
            The target of this :class:`~.EntityAction`, or None for the current :class:`Entity` instance's target.
            Defaults to ``None``.

        Returns
        -------
        :class:`EntityAction`
            The generated EntityAction instance.

        Examples
        --------
        ::

            mob = Material.ZOMBIE_SPAWN_EGG  # disguise as zombie
            last_entity.mob_disguise(mob, "Zomb")
            # OR
            Entity(EntityTarget.LAST_ENTITY).mob_disguise(mob, "Zomb")  # disguise the last spawned entity as a zombie
                                                                        # named "Zomb"
        """
        args = Arguments([
            p_check(spawn_egg, SpawnEggable, "spawn_egg"),
            p_check(name, typing.Optional[Textable], "name") if name is not None else None
        ])
        return EntityAction(
            action=EntityActionType.MOB_DISGUISE,
            args=args,
            target=self._digest_target(target),
            append_to_reader=True
        )

    def set_mooshroom_variant(
        self, mooshroom_variant: MooshroomVariant = MooshroomVariant.RED,
        target: typing.Optional[EntityTarget] = None
    ):
        """Sets the skin type of a mooshroom.

        Parameters
        ----------
        mooshroom_variant : :class:`~.MooshroomVariant`
            The new variant (either :attr:`~.MooshroomVariant.RED` or :attr:`~.MooshroomVariant.BROWN`).
            Defaults to :attr:`~.MooshroomVariant.RED`.

        target : Optional[:class:`~.EntityTarget`], optional
            The target of this :class:`~.EntityAction`, or None for the current :class:`Entity` instance's target.
            Defaults to ``None``.

        Returns
        -------
        :class:`EntityAction`
            The generated EntityAction instance.

        Examples
        --------
        ::

            last_mob.set_mooshroom_variant(MooshroomVariant.BROWN)
            # OR
            Entity(EntityTarget.LAST_MOB).set_mooshroom_variant(MooshroomVariant.BROWN)  # if the last spawned mob is a
                                                                                         # mooshroom, it becomes of
                                                                                         # brown variant.
        """
        args = Arguments([], tags=[
            Tag(
                "Mooshroom Variant", option=MooshroomVariant(mooshroom_variant),  # default is Red
                action=EntityActionType.MOOSHROOM_VARIANT, block=BlockType.IF_GAME
            )
        ])
        return EntityAction(
            action=EntityActionType.MOOSHROOM_VARIANT,
            args=args,
            target=self._digest_target(target),
            append_to_reader=True
        )

    def move_to(
        self, loc: Locatable, speed: typing.Optional[Numeric] = None,
        *, target: typing.Optional[EntityTarget] = None
    ):
        """Instructs the mob's AI to always pathfind to a certain location at a certain speed.

        .. rank:: Overlord


        Parameters
        ----------
        loc : :attr:`~.Locatable`
            Target location.

        speed : Optional[:attr:`~.Numeric`], optional
            The walk speed the mob should have. Default is ``None`` (default walk speed).

        target : Optional[:class:`~.EntityTarget`], optional
            The target of this :class:`~.EntityAction`, or None for the current :class:`Entity` instance's target.
            Defaults to ``None``.

        Returns
        -------
        :class:`EntityAction`
            The generated EntityAction instance.

        Warnings
        -----
        'Move To' only works if the mob is close enough to the target so that its AI can pathfind to it.


        Examples
        --------
        ::

            loc = DFLocation(1, 2, 3)  # target location
            last_mob.move_to(loc, 5)
            # OR
            Entity(EntityTarget.LAST_MOB).move_to(loc, 5)  # Tells AI to move to target location at speed of 5
        """
        args = Arguments([
            p_check(loc, Locatable, "loc"),
            p_check(speed, typing.Optional[Numeric], "speed") if speed is not None else None
        ])
        return EntityAction(
            action=EntityActionType.MOVE_TO,
            args=args,
            target=self._digest_target(target),
            append_to_reader=True
        )

    def disable_ai(self, *, target: typing.Optional[EntityTarget] = None):
        """Disables the AI of the mob.

        .. rank:: Noble


        Parameters
        ----------
        target : Optional[:class:`~.EntityTarget`], optional
            The target of this :class:`~.EntityAction`, or None for the current :class:`Entity` instance's target.
            Defaults to ``None``.

        Returns
        -------
        :class:`EntityAction`
            The generated EntityAction instance.

        Examples
        --------
        ::

            last_mob.disable_ai()
            # OR
            Entity(EntityTarget.LAST_MOB).disable_ai()
        """
        return EntityAction(
            action=EntityActionType.NO_AI,
            args=Arguments(),
            target=self._digest_target(target),
            append_to_reader=True
        )

    def disable_drops(self, *, target: typing.Optional[EntityTarget] = None):
        """After this code block is executed, the mob will no longer drop their equipment and loot when they die.

        Parameters
        ----------
        target : Optional[:class:`~.EntityTarget`], optional
            The target of this :class:`~.EntityAction`, or None for the current :class:`Entity` instance's target.
            Defaults to ``None``.

        Returns
        -------
        :class:`EntityAction`
            The generated EntityAction instance.

        Examples
        --------
        ::

            last_mob.disable_drops()
            # OR
            Entity(EntityTarget.LAST_MOB).disable_drops()
        """
        return EntityAction(
            action=EntityActionType.NO_DROPS,
            args=Arguments(),
            target=self._digest_target(target),
            append_to_reader=True
        )

    def disable_gravity(self, *, target: typing.Optional[EntityTarget] = None):
        """Disables gravity for the entity.

        .. rank:: Overlord


        Parameters
        ----------
        target : Optional[:class:`~.EntityTarget`], optional
            The target of this :class:`~.EntityAction`, or None for the current :class:`Entity` instance's target.
            Defaults to ``None``.

        Returns
        -------
        :class:`EntityAction`
            The generated EntityAction instance.

        Examples
        --------
        ::

            last_entity.disable_gravity()
            # OR
            Entity(EntityTarget.LAST_ENTITY).disable_gravity()
        """
        return EntityAction(
            action=EntityActionType.NO_GRAVITY,
            args=Arguments(),
            target=self._digest_target(target),
            append_to_reader=True
        )

    def disable_proj_coll(self, *, target: typing.Optional[EntityTarget] = None):
        """Prevents projectiles from hitting the mob.

        Parameters
        ----------
        target : Optional[:class:`~.EntityTarget`], optional
            The target of this :class:`~.EntityAction`, or None for the current :class:`Entity` instance's target.
            Defaults to ``None``.

        Returns
        -------
        :class:`EntityAction`
            The generated EntityAction instance.

        Examples
        --------
        ::

            last_mob.disable_proj_coll()
            # OR
            Entity(EntityTarget.LAST_MOB).disable_proj_coll()
        """
        return EntityAction(
            action=EntityActionType.NO_PROJ_COLL,
            args=Arguments(),
            target=self._digest_target(target),
            append_to_reader=True
        )

    def disguise_as_player(
        self, name: Textable, *, skin: typing.Optional[Textable] = None,
        target: typing.Optional[EntityTarget] = None
    ):
        """Disguises the entity as a player.

        .. rank:: Overlord


        Parameters
        ----------
        name : :attr:`~.Textable`
            Name of the player to disguise as.

        skin : Optional[:attr:`~.Textable`], optional
            Name of the player whose skin should be used, or ``None`` for the skin of the player given in `name`.
            Default is ``None``.

        target : Optional[:class:`~.EntityTarget`], optional
            The target of this :class:`~.EntityAction`, or None for the current :class:`Entity` instance's target.
            Defaults to ``None``.

        Returns
        -------
        :class:`EntityAction`
            The generated EntityAction instance.

        Examples
        --------
        ::

            last_entity.disguise_as_player("John", skin="Notch")  # (last spawned entity)
            # OR
            Entity(EntityTarget.LAST_ENTITY).disguise_as_player("John", skin="Notch")  # disguises as the Notch skin,
                                                                                       # but named "John".
            # do not specify skin in order to apply the skin assigned to the given name (in this case, "John").
        """
        args = Arguments([
            p_check(name, Textable, "name"),
            p_check(skin, typing.Optional[Textable], "skin") if skin is not None else None
        ])
        return EntityAction(
            action=EntityActionType.PLAYER_DISGUISE,
            args=args,
            target=self._digest_target(target),
            append_to_reader=True
        )

    def enable_proj_coll(self, *, target: typing.Optional[EntityTarget] = None):
        """Allows projectiles to hit the mob.

        Parameters
        ----------
        target : Optional[:class:`~.EntityTarget`], optional
            The target of this :class:`~.EntityAction`, or None for the current :class:`Entity` instance's target.
            Defaults to ``None``.

        Returns
        -------
        :class:`EntityAction`
            The generated EntityAction instance.

        Examples
        --------
        ::

            last_entity.enable_proj_coll()
            # OR
            Entity(EntityTarget.LAST_ENTITY).enable_proj_coll()
        """
        return EntityAction(
            action=EntityActionType.PROJ_COLL,
            args=Arguments(),
            target=self._digest_target(target),
            append_to_reader=True
        )

    def set_projectile_item(
        self, item: ItemParam,
        *, target: typing.Optional[EntityTarget] = None
    ):
        """Sets the item the projectile displays as.

        .. workswith:: Snowball, Egg, Small Fireball, Ghast Fireball, Ender Pearl, Experience Bottle

        Parameters
        ----------
        item : :attr:`~.ItemParam`
            Item for the projectile to display as.

            .. note:: Does not work with air.

        target : Optional[:class:`~.EntityTarget`], optional
            The target of this :class:`~.EntityAction`, or None for the current :class:`Entity` instance's target.
            Defaults to ``None``.

        Returns
        -------
        :class:`EntityAction`
            The generated EntityAction instance.


        Examples
        --------
        ::

            item = Item(Material.STONE, name="My Stone")  # displays as a stone block named "My Stone"
            last_entity.projectile_item(item)
            # OR
            Entity(EntityTarget.LAST_ENTITY).projectile_item(item)
        """
        args = Arguments([
            p_check(item, ItemParam, "item")
        ])
        return EntityAction(
            action=EntityActionType.PROJECTILE_ITEM,
            args=args,
            target=self._digest_target(target),
            append_to_reader=True
        )

    def remove(self, *, target: typing.Optional[EntityTarget] = None):
        """Deletes the entity.

        Parameters
        ----------
        target : Optional[:class:`~.EntityTarget`], optional
            The target of this :class:`~.EntityAction`, or None for the current :class:`Entity` instance's target.
            Defaults to ``None``.

        Returns
        -------
        :class:`EntityAction`
            The generated EntityAction instance.

        Examples
        --------
        ::

            last_entity.remove()
            # OR
            Entity(EntityTarget.LAST_ENTITY).remove()
        """
        return EntityAction(
            action=EntityActionType.REMOVE,
            args=Arguments(),
            target=self._digest_target(target),
            append_to_reader=True
        )

    def remove_effect(
        self, *potions: typing.Union[Potionable, Listable],
        target: typing.Optional[EntityTarget] = None
    ):
        """Removes one or more potion effects from the mob.

        Parameters
        ----------
        potions : Union[:attr:`~.Potionable`, :attr:`~.Listable`]
            Potion effect(s) to be removed, or a List variable containing them.

        target : Optional[:class:`~.EntityTarget`], optional
            The target of this :class:`~.EntityAction`, or None for the current :class:`Entity` instance's target.
            Defaults to ``None``.

        Returns
        -------
        :class:`EntityAction`
            The generated EntityAction instance.

        Notes
        -----
        Amplifiers and durations do not have to be the same as the initial potion effect(s).


        Examples
        --------
        ::

            potion_1 = DFPotion(PotionEffect.ABSORPTION, amplifier=5)
            potion_2 = PotionVar("my var containing a potion")
            last_entity.remove_effect(potion_1, potion_2)
            # OR
            Entity(EntityTarget.LAST_ENTITY).remove_effect(potion_1, potion_2)  # removes potion_1 and potion_2 effects
                                                                                # from the last spawned entity.
        """
        args = Arguments([
            p_check(potion, typing.Union[Potionable, Listable], f"potions[{i}]") for i, potion in enumerate(potions)
        ])
        return EntityAction(
            action=EntityActionType.REMOVE_EFFECT,
            args=args,
            target=self._digest_target(target),
            append_to_reader=True
        )

    def ride_entity(
        self, name: Textable,
        *, target: typing.Optional[EntityTarget] = None
    ):
        """Mounts the target entity on top of another player or entity.

        .. rank:: Noble


        Parameters
        ----------
        name : :attr:`~.Textable`
            Name of player or entity to be ridden.

            .. note:: Player names will be prioritized before mob names.

        target : Optional[:class:`~.EntityTarget`], optional
            The target of this :class:`~.EntityAction`, or None for the current :class:`Entity` instance's target.
            Defaults to ``None``.

        Returns
        -------
        :class:`EntityAction`
            The generated EntityAction instance.


        Examples
        --------
        ::

            last_entity.ride_entity("Something")
            # OR
            Entity(EntityTarget.LAST_ENTITY).ride_entity("Something")  # mounts the last spawned entity on top of either
                                                                       # a player named "Something" or, if none, an
                                                                       # entity named "Something".
        """
        args = Arguments([
            p_check(name, Textable, "name")
        ])
        return EntityAction(
            action=EntityActionType.RIDE_ENTITY,
            args=args,
            target=self._digest_target(target),
            append_to_reader=True
        )

    def send_animation(
        self, animation_type: EntityAnimation,
        target: typing.Optional[EntityTarget] = None
    ):
        """Makes the mob perform an animation.

        Parameters
        ----------
        animation_type : :class:`~.EntityAnimation`
            The type of animation to send (see the EntiytAnimation enum documentation for options).

        target : Optional[:class:`~.EntityTarget`], optional
            The target of this :class:`~.EntityAction`, or None for the current :class:`Entity` instance's target.
            Defaults to ``None``.

        Returns
        -------
        :class:`EntityAction`
            The generated EntityAction instance.

        Examples
        --------
        ::

            last_entity.send_animation(EntityAnimation.SWING_RIGHT_ARM)
            # OR
            Entity(EntityTarget.LAST_ENTITY).send_animation(EntityAnimation.SWING_RIGHT_ARM)  # makes the last spawned entity
                                                                                              # swing its right arm.
        """
        args = Arguments([], tags=[
            Tag(
                "Animation Type", option=EntityAnimation(animation_type),  # default is Swing Right Arm
                action=EntityActionType.SEND_ANIMATION, block=BlockType.IF_GAME
            )
        ])
        return EntityAction(
            action=EntityActionType.SEND_ANIMATION,
            args=args,
            target=self._digest_target(target),
            append_to_reader=True
        )

    def set_age_or_size(
        self, age_or_size: Numeric,
        *, target: typing.Optional[EntityTarget] = None
    ):
        """Sets the age or size of the mob.

        Parameters
        ----------
        age_or_size : :attr:`~.Numeric`
            Mob age or size to set.

            .. note::

                - Ages below 0 make the mob a baby. For animals, age increases constantly.
                - For slimes, magma cubes and phantoms, size is set instead of age.

        target : Optional[:class:`~.EntityTarget`], optional
            The target of this :class:`~.EntityAction`, or None for the current :class:`Entity` instance's target.
            Defaults to ``None``.

        Returns
        -------
        :class:`EntityAction`
            The generated EntityAction instance.

        Examples
        --------
        ::

            last_mob.set_age_or_size(2)
            # OR
            Entity(EntityTarget.LAST_MOB).set_age_or_size(2)  # sets the last spawned mob's age or size to 2.
        """
        args = Arguments([
            p_check(age_or_size, Numeric, "age_or_size")
        ])
        return EntityAction(
            action=EntityActionType.SET_AGE_OR_SIZE,
            args=args,
            target=self._digest_target(target),
            append_to_reader=True
        )

    def set_is_age_locked(
        self, is_locked: bool = True,
        target: typing.Optional[EntityTarget] = None
    ):
        """Sets whether a mob should age.

        Parameters
        ----------
        is_locked : :class:`bool`, optional
            Whether or not the mob should be unable to age. Defaults to ``True`` (mob cannot age).

        target : Optional[:class:`~.EntityTarget`], optional
            The target of this :class:`~.EntityAction`, or None for the current :class:`Entity` instance's target.
            Defaults to ``None``.

        Returns
        -------
        :class:`EntityAction`
            The generated EntityAction instance.

        Examples
        --------
        ::

            last_mob.set_age_locked(True)
            # OR
            Entity(EntityTarget.LAST_MOB).set_age_locked(True)  # last spawned mob can no longer age
        """
        args = Arguments([], tags=[
            Tag(
                "Is Locked", option=bool(is_locked),  # default is True
                action=EntityActionType.SET_AGE_LOCKED, block=BlockType.IF_GAME
            )
        ])
        return EntityAction(
            action=EntityActionType.SET_AGE_LOCKED,
            args=args,
            target=self._digest_target(target),
            append_to_reader=True
        )

    # def set_armor(self, *, target: typing.Optional[EntityTarget] = None):
    #     """
    #
    #     Parameters
    #     ----------
    #     target : Optional[:class:`~.EntityTarget`], optional
    #         The target of this :class:`~.EntityAction`, or None for the current :class:`Entity` instance's target.
    #         Defaults to ``None``.
    #
    #     Returns
    #     -------
    #     :class:`EntityAction`
    #         The generated EntityAction instance.
    #
    #     Examples
    #     --------
    #     ::
    #
    #         last_entity.set_armor()
    #         # OR
    #         Entity(EntityTarget.LAST_ENTITY).set_armor()
    #     """
    #     return EntityAction(
    #         action=EntityActionType.SET_ARMOR,
    #         args=Arguments(),
    #         target=self._digest_target(target),
    #         append_to_reader=True
    #     )

    def set_cat_type(
        self, skin_type: CatType,
        *, target: typing.Optional[EntityTarget] = None
    ):
        """Sets the skin type of a cat.

        Parameters
        ----------
        skin_type : :class:`~.CatType`
            The new skin type of the cat (see the CatType docs for options).

        target : Optional[:class:`~.EntityTarget`], optional
            The target of this :class:`~.EntityAction`, or None for the current :class:`Entity` instance's target.
            Defaults to ``None``.

        Returns
        -------
        :class:`EntityAction`
            The generated EntityAction instance.

        Examples
        --------
        ::

            last_mob.set_cat_type(CatType.TABBY)
            # OR
            Entity(EntityTarget.LAST_MOB).set_cat_type(CatType.TABBY)  # if the last spawned mob is a cat, its cat type
                                                                       # becomes "Tabby"
        """
        args = Arguments([], tags=[
            Tag(
                "Skin Type", option=CatType(skin_type),  # default is Tabby
                action=EntityActionType.SET_CAT_TYPE, block=BlockType.IF_GAME
            )
        ])
        return EntityAction(
            action=EntityActionType.SET_CAT_TYPE,
            args=args,
            target=self._digest_target(target),
            append_to_reader=True
        )

    def set_color(
            self, color: EntityColor,
            target: typing.Optional[EntityTarget] = None
    ):
        """Sets the color of a mob.

        .. workswith:: Sheep, Shulker, Dog (collar), Cat (collar)

        Parameters
        ----------
        color : :class:`~.EntityColor`
            The new color of the mob (see EntityColor docs for options).

        target : Optional[:class:`~.EntityTarget`], optional
            The target of this :class:`~.EntityAction`, or None for the current :class:`Entity` instance's target.
            Defaults to ``None``.

        Returns
        -------
        :class:`EntityAction`
            The generated EntityAction instance.

        Examples
        --------
        ::

            last_mob.set_color(EntityColor.WHITE)
            # OR
            Entity(EntityTarget.LAST_MOB).set_color(EntityColor.WHITE)  # sets the last spawned mob's color to white
        """
        args = Arguments([], tags=[
            Tag(
                "Color", option=EntityColor(color),  # default is White
                action=EntityActionType.SET_COLOR, block=BlockType.IF_GAME
            )
        ])
        return EntityAction(
            action=EntityActionType.SET_COLOR,
            args=args,
            target=self._digest_target(target),
            append_to_reader=True
        )

    def set_fall_distance(
        self, distance: Numeric,
        *, target: typing.Optional[EntityTarget] = None
    ):
        """Sets the entity's fall distance, affecting fall damage upon landing.

        Parameters
        ----------
        distance : :attr:`~.Numeric`
            Fall distance (in blocks).

        target : Optional[:class:`~.EntityTarget`], optional
            The target of this :class:`~.EntityAction`, or None for the current :class:`Entity` instance's target.
            Defaults to ``None``.

        Returns
        -------
        :class:`EntityAction`
            The generated EntityAction instance.

        Examples
        --------
        ::

            last_entity.set_fall_distance(10)
            # OR
            Entity(EntityTarget.LAST_ENTITY).set_fall_distance(10)  # Sets the last spawned entity's fall distance to 10 blocks.
        """
        args = Arguments([
            p_check(distance, Numeric, "distance")
        ])
        return EntityAction(
            action=EntityActionType.SET_FALL_DISTANCE,
            args=args,
            target=self._digest_target(target),
            append_to_reader=True
        )

    def set_fire_ticks(
        self, duration: Numeric,
        *, target: typing.Optional[EntityTarget] = None
    ):
        """Sets the entity on fire for a certain number of ticks.

        Parameters
        ----------
        duration : :attr:`~.Numeric`
            Duration for which the entity should be on fire (in ticks).

            .. note::

                A duration of 0 extinguishes the entity (i.e., removes fire).

        target : Optional[:class:`~.EntityTarget`], optional
            The target of this :class:`~.EntityAction`, or None for the current :class:`Entity` instance's target.
            Defaults to ``None``.

        Returns
        -------
        :class:`EntityAction`
            The generated EntityAction instance.


        Examples
        --------
        ::

            last_entity.set_fire_ticks(60)
            # OR
            Entity(EntityTarget.LAST_ENTITY).set_fire_ticks(60)  # Last spawned entity is now on fire for 3 seconds
        """
        args = Arguments([
            p_check(duration, Numeric, "duration")
        ])
        return EntityAction(
            action=EntityActionType.SET_FIRE_TICKS,
            args=args,
            target=self._digest_target(target),
            append_to_reader=True
        )

    def set_fox_type(
        self, fox_type: FoxType,
        target: typing.Optional[EntityTarget] = None
    ):
        """Sets the fur type of a fox.

        Parameters
        ----------
        fox_type : :class:`~.FoxType`
            The new type of fox fur (either :attr:`~.FoxType.RED` or :attr:`~.FoxType.SNOW`).

        target : Optional[:class:`~.EntityTarget`], optional
            The target of this :class:`~.EntityAction`, or None for the current :class:`Entity` instance's target.
            Defaults to ``None``.

        Returns
        -------
        :class:`EntityAction`
            The generated EntityAction instance.

        Examples
        --------
        ::

            last_mob.set_fox_type(FoxType.RED)
            # OR
            Entity(EntityTarget.LAST_MOB).set_fox_type(FoxType.RED)  # Sets the last spawned mob's fox type to a Red Fox.
        """
        args = Arguments([], tags=[
            Tag(
                "Fox Type", option=FoxType(fox_type),  # default is Red
                action=EntityActionType.SET_FOX_TYPE, block=BlockType.IF_GAME
            )
        ])
        return EntityAction(
            action=EntityActionType.SET_FOX_TYPE,
            args=args,
            target=self._digest_target(target),
            append_to_reader=True
        )

    def set_hand_item(
        self, item: typing.Optional[ItemParam] = None,
        *, hand_slot: Hand = Hand.MAIN_HAND,
        target: typing.Optional[EntityTarget] = None
    ):
        """Sets the item in the mob's main hand or off hand.

        Parameters
        ----------
        item : Optional[:attr:`~.ItemParam`], optional
            Item to set. Default is ``None``.

        hand_slot : :class:`~.Hand`, optional
            The hand this item should be given to (either :attr:`~.Hand.MAIN_HAND` or :attr:`~.Hand.OFF_HAND`).
            Defaults to :attr:`~.Hand.MAIN_HAND`.

        target : Optional[:class:`~.EntityTarget`], optional
            The target of this :class:`~.EntityAction`, or None for the current :class:`Entity` instance's target.
            Defaults to ``None``.

        Returns
        -------
        :class:`EntityAction`
            The generated EntityAction instance.

        Examples
        --------
        ::

            item = Item(Material.DIAMOND, name="Some Diamond")  # item to give
            last_entity.set_hand_item(item, hand_slot=Hand.OFF_HAND)
            # OR
            Entity(EntityTarget.LAST_ENTITY).set_hand_item(item, hand_slot=Hand.OFF_HAND)  # sets the last spawned entity's
                                                                                           # offhand to the given item.
        """
        args = Arguments([
            p_check(item, typing.Optional[ItemParam], "item") if item is not None else None
        ], tags=[
            Tag(
                "Hand Slot", option=Hand(hand_slot),  # default is Main Hand
                action=EntityActionType.SET_HAND_ITEM, block=BlockType.IF_GAME
            )
        ])
        return EntityAction(
            action=EntityActionType.SET_HAND_ITEM,
            args=args,
            target=self._digest_target(target),
            append_to_reader=True
        )

    def set_health(
        self, health: Numeric,
        *, absorption: bool = False, combined: bool = False,
        target: typing.Optional[EntityTarget] = None
    ):
        """Sets the mob's health or absorption hearts.

        Parameters
        ----------
        health : :attr:`~.Numeric`
            New health.

            .. note::

                1 health = 0.5 hearts

        absorption : :class:`bool`, optional
            If ``True``, the mob's absorption health is set instead of regular health. Defaults to ``False`` (set regular
            health).

        combined : :class:`bool`, optional
            If ``True``, both the mob's regular and absorption hearts are set. Defaults to ``False`` (just regular health).

            .. note::

                Specifying this overrides what was specified for `absorption`.

        target : Optional[:class:`~.EntityTarget`], optional
            The target of this :class:`~.EntityAction`, or None for the current :class:`Entity` instance's target.
            Defaults to ``None``.

        Returns
        -------
        :class:`EntityAction`
            The generated EntityAction instance.

        Examples
        --------
        Setting regular health::

            last_mob.set_health(15)
            # OR
            Entity(EntityTarget.LAST_MOB).set_health(15)  # sets the last spawned mob's health to 15 (7.5 hearts).

        Setting absorption health::

            last_mob.set_health(15, absorption=True)
            # OR
            Entity(EntityTarget.LAST_MOB).set_health(15, absorption=True)  # sets the last spawned mob's absorption
                                                                           # health to 15 (7.5 absorp. hearts).

        Setting combined health (regular and absorption health)::

            last_mob.set_health(15, combined = True)
            # OR
            Entity(EntityTarget.LAST_MOB).set_health(15, combined = True)  # sets the last spawned mob's combined to 15
                                                                           # (7.5 hearts in total).
        """
        args = Arguments([
            p_check(health, Numeric, "health")
        ], tags=[
            Tag(
                "Heal Type", option="Combined Health" if combined else (
                    "Absorption Health" if absorption else "Regular Health"
                ),  # default is Regular Health
                action=EntityActionType.SET_HEALTH, block=BlockType.IF_GAME
            )
        ])
        return EntityAction(
            action=EntityActionType.SET_HEALTH,
            args=args,
            target=self._digest_target(target),
            append_to_reader=True
        )

    def set_horse_armor(
        self, item: typing.Optional[ItemParam] = None,
        *, target: typing.Optional[EntityTarget] = None
    ):
        """Sets the armor of a horse.

        Parameters
        ----------
        item : Optional[:attr:`~.ItemParam`], optional
            Armor item. Default is ``None`` (no armor).

        target : Optional[:class:`~.EntityTarget`], optional
            The target of this :class:`~.EntityAction`, or None for the current :class:`Entity` instance's target.
            Defaults to ``None``.

        Returns
        -------
        :class:`EntityAction`
            The generated EntityAction instance.

        Examples
        --------
        ::

            armor = Item(Material.DIAMOND_HORSE_ARMOR)  # a diamond horse armor
            last_mob.set_horse_armor(armor)
            # OR
            Entity(EntityTarget.LAST_MOB).set_horse_armor(armor)  # last spawned mob, if horse, gets diamond horse armor
        """
        args = Arguments([
            p_check(item, typing.Optional[ItemParam], "item") if item is not None else None
        ])
        return EntityAction(
            action=EntityActionType.SET_HORSE_ARMOR,
            args=args,
            target=self._digest_target(target),
            append_to_reader=True
        )

    def set_horse_chest(
        self, has_chest: bool = True,
        target: typing.Optional[EntityTarget] = None
    ):
        """Sets whether a horse has a chest equipped.

        .. workswith:: Donkey, Mule, Llama, Trader Llama

        Parameters
        ----------
        has_chest : :class:`bool`, optional
            If ``True``, the horse will have a chest equipped. If ``False``, it won't. Defaults to ``True`` (has chest).

        target : Optional[:class:`~.EntityTarget`], optional
            The target of this :class:`~.EntityAction`, or None for the current :class:`Entity` instance's target.
            Defaults to ``None``.

        Returns
        -------
        :class:`EntityAction`
            The generated EntityAction instance.

        Examples
        --------
        ::

            last_mob.set_horse_chest(True)
            # OR
            Entity(EntityTarget.LAST_MOB).set_horse_chest(True)  # if the last spawned mob is a valid horse, it will
                                                                 # have a chest equipped. (Specify False to remove.)
        """
        args = Arguments([], tags=[
            Tag(
                "Has Chest", option=bool(has_chest),  # default is True
                action=EntityActionType.SET_HORSE_CHEST, block=BlockType.IF_GAME
            )
        ])
        return EntityAction(
            action=EntityActionType.SET_HORSE_CHEST,
            args=args,
            target=self._digest_target(target),
            append_to_reader=True
        )

    def set_invulnerable(
        self, invulnerable: bool = True,
        target: typing.Optional[EntityTarget] = None
    ):
        """Sets whether an entity is invulnerable to damage.

        Parameters
        ----------
        invulnerable : :class:`bool`, optional
            If ``True``, the entity will be invulnerable. Otherwise (``False``), vulnerable. Defaults to ``True``.

        target : Optional[:class:`~.EntityTarget`], optional
            The target of this :class:`~.EntityAction`, or None for the current :class:`Entity` instance's target.
            Defaults to ``None``.

        Returns
        -------
        :class:`EntityAction`
            The generated EntityAction instance.

        Examples
        --------
        ::

            last_entity.set_invulnerable(True)
            # OR
            Entity(EntityTarget.LAST_ENTITY).set_invulnerable(True)  # last spawned entity is now invulnerable (False to undo)
        """
        args = Arguments([], tags=[
            Tag(
                "Invulnerable", option=bool(invulnerable),  # default is True
                action=EntityActionType.SET_INVULNERABLE, block=BlockType.IF_GAME
            )
        ])
        return EntityAction(
            action=EntityActionType.SET_INVULNERABLE,
            args=args,
            target=self._digest_target(target),
            append_to_reader=True
        )

    def set_item_owner(
        self, uuid: typing.Optional[Textable] = None,
        *, target: typing.Optional[EntityTarget] = None
    ):
        """Sets an item's owner.

        Parameters
        ----------
        uuid : Optional[:attr:`~.Textable`], optional
            The new owner's UUID. Default is ``None``.

            .. note:: Specifying no owner will clear the item's owner.

        target : Optional[:class:`~.EntityTarget`], optional
            The target of this :class:`~.EntityAction`, or None for the current :class:`Entity` instance's target.
            Defaults to ``None``.

        Returns
        -------
        :class:`EntityAction`
            The generated EntityAction instance.

        Notes
        -----
        Items with owners can only be picked up by their owner until the item is within 10 seconds of despawning.

        Examples
        --------
        ::

            uuid = TextVar("some var with an UUID")  # uuid of new item owner
            last_entity.set_item_owner(uuid)
            # OR
            Entity(EntityTarget.LAST_ENTITY).set_item_owner(uuid)  # If the last spawned entity is an item, its owner
                                                                   # will be set to the player who owns that UUID.
        """
        args = Arguments([
            p_check(uuid, typing.Optional[Textable], "uuid") if uuid is not None else None
        ])
        return EntityAction(
            action=EntityActionType.SET_ITEM_OWNER,
            args=args,
            target=self._digest_target(target),
            append_to_reader=True
        )

    def set_max_health(
        self, health: Numeric,
        *, heal_fully: bool = False,
        target: typing.Optional[EntityTarget] = None
    ):
        """Sets the maximum amount of health that the mob can have.

        Parameters
        ----------
        health : :attr:`~.Numeric`
            New maximum health of the mob.

        heal_fully : :class:`bool`, optional
            If ``True``, the mob is healed to the new max health. Defaults to ``False`` (not healed).

        target : Optional[:class:`~.EntityTarget`], optional
            The target of this :class:`~.EntityAction`, or None for the current :class:`Entity` instance's target.
            Defaults to ``None``.

        Returns
        -------
        :class:`EntityAction`
            The generated EntityAction instance.

        Examples
        --------
        ::

            last_entity.set_max_health(26)
            # OR
            Entity(EntityTarget.LAST_ENTITY).set_max_health(26)  # mob's max health is now 26 (13 hearts).
        """
        args = Arguments([
            p_check(health, Numeric, "health")
        ], tags=[
            Tag(
                "Heal Mob to Max Health", option=bool(heal_fully),  # default is False
                action=EntityActionType.SET_MAX_HEALTH, block=BlockType.IF_GAME
            )
        ])
        return EntityAction(
            action=EntityActionType.SET_MAX_HEALTH,
            args=args,
            target=self._digest_target(target),
            append_to_reader=True
        )

    def set_mob_sitting(
        self, is_sitting: bool = True,
        target: typing.Optional[EntityTarget] = None
    ):
        """Sets whether a tamed mob is sitting.

        Parameters
        ----------
        is_sitting : :class:`bool`, optional
            If ``True``, the mob will be sitting. Defaults to ``True``.

        target : Optional[:class:`~.EntityTarget`], optional
            The target of this :class:`~.EntityAction`, or None for the current :class:`Entity` instance's target.
            Defaults to ``None``.

        Returns
        -------
        :class:`EntityAction`
            The generated EntityAction instance.

        Examples
        --------
        ::

            last_mob.set_mob_sitting(True)
            # OR
            Entity(EntityTarget.LAST_MOB).set_mob_sitting(True)  # Last spawned mob will now be sitting; False to undo
        """
        args = Arguments([], tags=[
            Tag(
                "Is Sitting", option=bool(is_sitting),  # default is True
                action=EntityActionType.SET_MOB_SITTING, block=BlockType.IF_GAME
            )
        ])
        return EntityAction(
            action=EntityActionType.SET_MOB_SITTING,
            args=args,
            target=self._digest_target(target),
            append_to_reader=True
        )

    def set_name(
        self, name: Textable,
        *, hide_name_tag: bool = False,
        target: typing.Optional[EntityTarget] = None
    ):
        """Changes the name of the entity.

        Parameters
        ----------
        name : :attr:`~.Textable`
            The entity's new name.

        hide_name_tag : :class:`bool`, optional
            If ``True``, the entity's name will be hidden (i.e., not show up above it). Defaults to ``False`` (visible).

        target : Optional[:class:`~.EntityTarget`], optional
            The target of this :class:`~.EntityAction`, or None for the current :class:`Entity` instance's target.
            Defaults to ``None``.

        Returns
        -------
        :class:`EntityAction`
            The generated EntityAction instance.

        Examples
        --------
        ::

            last_entity.set_name("My Entity", hide_name_tag=True)
            # OR
            Entity(EntityTarget.LAST_ENTITY).set_name("My Entity", hide_name_tag=True)  # Sets the last spawned entity's
                                                                                        # name to "My Entity", while
                                                                                        # keeping it hidden.
        """
        args = Arguments([
            p_check(name, Textable, "name")
        ], tags=[
            Tag(
                "Hide Name Tag", option=bool(hide_name_tag),  # default is False
                action=EntityActionType.SET_NAME, block=BlockType.IF_GAME
            )
        ])
        return EntityAction(
            action=EntityActionType.SET_NAME,
            args=args,
            target=self._digest_target(target),
            append_to_reader=True
        )

    def set_panda_genes(
        self,
        *, main_gene: typing.Optional[PandaGene] = None, hidden_gene: typing.Optional[PandaGene] = None,
        target: typing.Optional[EntityTarget] = None
    ):
        """Sets the genes (traits) of a panda.

        Parameters
        ----------
        main_gene : Optional[:class:`~.PandaGene`]
            The panda's new main gene (see PandaGene docs for options), or ``None`` to not change. Defaults to ``None``.

        hidden_gene : Optional[:class:`~.PandaGene`]
            The panda's new hidden gene (see PandaGene docs for options), or ``None`` to not change. Defaults to ``None``.

        target : Optional[:class:`~.EntityTarget`], optional
            The target of this :class:`~.EntityAction`, or None for the current :class:`Entity` instance's target.
            Defaults to ``None``.

        Returns
        -------
        :class:`EntityAction`
            The generated EntityAction instance.

        Examples
        --------
        ::

            last_mob.set_panda_genes(main_gene=PandaGene.LAZY, hidden_gene=PandaGene.AGGRESSIVE)
            # OR
            Entity(EntityTarget.LAST_MOB).set_panda_genes(main_gene=PandaGene.LAZY, hidden_gene=PandaGene.AGGRESSIVE)
        """
        args = Arguments([], tags=[  # hidden goes first!!!
            Tag(
                "Hidden Gene", option=PandaGene(hidden_gene) if hidden_gene is not None else None,  # default is Don't Change
                action=EntityActionType.SET_PANDA_GENES, block=BlockType.IF_GAME
            ),
            Tag(
                "Main Gene", option=PandaGene(main_gene) if main_gene is not None else None,  # default is Don't Change
                action=EntityActionType.SET_PANDA_GENES, block=BlockType.IF_GAME
            )
        ])
        return EntityAction(
            action=EntityActionType.SET_PANDA_GENES,
            args=args,
            target=self._digest_target(target),
            append_to_reader=True
        )

    def set_parrot_variant(
        self, parrot_variant: ParrotVariant,
        *, target: typing.Optional[EntityTarget] = None
    ):
        """Sets the skin variant of a parrot.

        Parameters
        ----------
        parrot_variant : :class:`~.ParrotVariant`
            The new variant of the target parrot (see ParrotVariant docs for options).

        target : Optional[:class:`~.EntityTarget`], optional
            The target of this :class:`~.EntityAction`, or None for the current :class:`Entity` instance's target.
            Defaults to ``None``.

        Returns
        -------
        :class:`EntityAction`
            The generated EntityAction instance.

        Examples
        --------
        ::

            last_mob.set_parrot_variant(ParrotVariant.RED)
            # OR
            Entity(EntityTarget.LAST_MOB).set_parrot_variant(ParrotVariant.RED)  # last spawned mob, if parrot,
                                                                                 # is now a red parrot.
        """
        args = Arguments([], tags=[
            Tag(
                "Parrot Variant", option=ParrotVariant(parrot_variant),  # default is Red
                action=EntityActionType.SET_PARROT_VARIANT, block=BlockType.IF_GAME
            )
        ])
        return EntityAction(
            action=EntityActionType.SET_PARROT_VARIANT,
            args=args,
            target=self._digest_target(target),
            append_to_reader=True
        )

    def set_pickup_delay(
        self, delay: Numeric,
        *, target: typing.Optional[EntityTarget] = None
    ):
        """Sets an item's pickup delay.

        Parameters
        ----------
        delay : :attr:`~.Numeric`
            New pickup delay (in ticks).

        target : Optional[:class:`~.EntityTarget`], optional
            The target of this :class:`~.EntityAction`, or None for the current :class:`Entity` instance's target.
            Defaults to ``None``.

        Returns
        -------
        :class:`EntityAction`
            The generated EntityAction instance.

        Examples
        --------
        ::

            last_entity.set_pickup_delay(60)
            # OR
            Entity(EntityTarget.LAST_ENTITY).set_pickup_delay(60)  # Last spawned entity, if an item, will have its
                                                                   # pickup delay set to 3 seconds (60 ticks).
        """
        args = Arguments([
            p_check(delay, Numeric, "delay")
        ])
        return EntityAction(
            action=EntityActionType.SET_PICKUP_DELAY,
            args=args,
            target=self._digest_target(target),
            append_to_reader=True
        )

    def set_armorstand_pose(
            self, x_rot: typing.Optional[Numeric] = None, y_rot: typing.Optional[Numeric] = None,
            z_rot: typing.Optional[Numeric] = None,
            *, armor_stand_part: ArmorStandPart = ArmorStandPart.HEAD,
            target: typing.Optional[EntityTarget] = None
    ):
        """Sets the three-dimensional rotation of an armor stand part.

        .. rank:: Mythic


        Parameters
        ----------
        x_rot : Optional[:attr:`~.Numeric`], optional
            X Rotation (0 to 360 degrees). Default is ``None``.

        y_rot : Optional[:attr:`~.Numeric`], optional
            Y Rotation (0 to 360 degrees). Default is ``None``.

        z_rot : Optional[:attr:`~.Numeric`], optional
            Z Rotation (0 to 360 degrees). Default is ``None``

        part : :class:`~.ArmorStandPart`, optional
            The part of the armor stand to be rotated (either :attr:`~.ArmorStandPart.HEAD`,
            :attr:`~.ArmorStandPart.BODY`, :attr:`~.ArmorStandPart.LEFT_ARM`, :attr:`~.ArmorStandPart.RIGHT_ARM`,
            :attr:`~.ArmorStandPart.LEFT_LEG` or :attr:`~.ArmorStandPart.RIGHT_LEG`). Defaults to HEAD.

        target : Optional[:class:`~.EntityTarget`], optional
            The target of this :class:`~.EntityAction`, or None for the current :class:`Entity` instance's target.
            Defaults to ``None``.

        Returns
        -------
        :class:`EntityAction`
            The generated EntityAction instance.

        Examples
        --------
        ::

            last_entity.set_armorstand_pose(45, 45, 45, part=ArmorStandPart.HEAD)
            # OR
            Entity(EntityTarget.LAST_ENTITY).set_armorstand_pose(45, 45, 45, part=ArmorStandPart.HEAD)
            # if the last spawned entity is an armor stand, its head is rotated 45 degrees on each of x, y, z.
        """
        if isinstance(x_rot, (int, float, DFNumber)):
            x_rot = DFNumber(x_rot % 360)

        if isinstance(y_rot, (int, float, DFNumber)):
            y_rot = DFNumber(y_rot % 360)

        if isinstance(z_rot, (int, float, DFNumber)):
            z_rot = DFNumber(z_rot % 360)

        args = Arguments([
            p_check(x_rot, typing.Optional[Numeric], "x_rot") if x_rot is not None else None,
            p_check(y_rot, typing.Optional[Numeric], "y_rot") if y_rot is not None else None,
            p_check(z_rot, typing.Optional[Numeric], "z_rot") if z_rot is not None else None
        ], tags=[
            Tag(
                "Armor Stand Part", option=ArmorStandPart(part),  # default is Head
                action=EntityActionType.SET_POSE, block=BlockType.IF_GAME
            )
        ])
        return EntityAction(
            action=EntityActionType.SET_POSE,
            args=args,
            target=self._digest_target(target),
            append_to_reader=True
        )

    def set_rabbit_type(
            self,
            *, skin_type="Brown",
            target: typing.Optional[EntityTarget] = None
    ):
        """Sets the skin type of a rabbit.

        Parameters
        ----------
        skin_type :
            Brown, White, Black, Black and White, Gold, Salt and Pepper

        target : Optional[:class:`~.EntityTarget`], optional
            The target of this :class:`~.EntityAction`, or None for the current :class:`Entity` instance's target.
            Defaults to ``None``.

        Returns
        -------
        :class:`EntityAction`
            The generated EntityAction instance.

        Examples
        --------
        ::

            last_entity.set_rabbit_type()
            # OR
            Entity(EntityTarget.LAST_ENTITY).set_rabbit_type()  # TODO: Example
        """
        args = Arguments([], tags=[
            Tag(
                "Skin Type", option=skin_type,  # default is Brown
                action=EntityActionType.SET_RABBIT_TYPE, block=BlockType.IF_GAME
            )
        ])
        return EntityAction(
            action=EntityActionType.SET_RABBIT_TYPE,
            args=args,
            target=self._digest_target(target),
            append_to_reader=True
        )

    def set_saddle(
            self, item: typing.Optional[ItemParam] = None,
            *, target: typing.Optional[EntityTarget] = None
    ):
        """Sets the saddle or carpet item of a mob.
        .. workswith:: Horses, Pigs, Llamas (Decor)

        Parameters
        ----------
        item : Optional[:attr:`~.ItemParam`], optional
            Saddle item. Default is ``None``.

        target : Optional[:class:`~.EntityTarget`], optional
            The target of this :class:`~.EntityAction`, or None for the current :class:`Entity` instance's target.
            Defaults to ``None``.

        Returns
        -------
        :class:`EntityAction`
            The generated EntityAction instance.

        Notes
        -----
        - Specifying no saddle item will remove the mob's saddle.
        - Pigs do not retain saddle metadata, only that they have a saddle.


        Examples
        --------
        ::

            last_entity.set_saddle(item)
            # OR
            Entity(EntityTarget.LAST_ENTITY).set_saddle(item)  # TODO: Example
        """
        args = Arguments([
            p_check(item, typing.Optional[ItemParam], "item") if item is not None else None
        ])
        return EntityAction(
            action=EntityActionType.SET_SADDLE,
            args=args,
            target=self._digest_target(target),
            append_to_reader=True
        )

    def set_sheep_sheared(
            self,
            *, is_sheared: bool = True,
            target: typing.Optional[EntityTarget] = None
    ):
        """Sets whether a sheep is currently sheared.

        Parameters
        ----------
        is_sheared : :class:`bool`, optional
            Defaults to ``True``.

        target : Optional[:class:`~.EntityTarget`], optional
            The target of this :class:`~.EntityAction`, or None for the current :class:`Entity` instance's target.
            Defaults to ``None``.

        Returns
        -------
        :class:`EntityAction`
            The generated EntityAction instance.

        Examples
        --------
        ::

            last_entity.set_sheep_sheared()
            # OR
            Entity(EntityTarget.LAST_ENTITY).set_sheep_sheared()  # TODO: Example
        """
        args = Arguments([], tags=[
            Tag(
                "Is Sheared", option=bool(is_sheared),  # default is True
                action=EntityActionType.SET_SHEEP_SHEARED, block=BlockType.IF_GAME
            )
        ])
        return EntityAction(
            action=EntityActionType.SET_SHEEP_SHEARED,
            args=args,
            target=self._digest_target(target),
            append_to_reader=True
        )

    def set_slime_ai(
            self,
            *, do_ai: bool = True,
            target: typing.Optional[EntityTarget] = None
    ):
        """Allows a slime's AI to be enabled and disabled, but unlike the disable AI action, the slime can still be moved.
        .. workswith:: Slime, Magma Cube

        Parameters
        ----------
        do_ai : :class:`bool`, optional
            Defaults to ``True``.

        target : Optional[:class:`~.EntityTarget`], optional
            The target of this :class:`~.EntityAction`, or None for the current :class:`Entity` instance's target.
            Defaults to ``None``.

        Returns
        -------
        :class:`EntityAction`
            The generated EntityAction instance.

        Examples
        --------
        ::

            last_entity.set_slime_ai()
            # OR
            Entity(EntityTarget.LAST_ENTITY).set_slime_ai()  # TODO: Example
        """
        args = Arguments([], tags=[
            Tag(
                "Do AI", option=bool(do_ai),  # default is True
                action=EntityActionType.SET_SLIME_AI, block=BlockType.IF_GAME
            )
        ])
        return EntityAction(
            action=EntityActionType.SET_SLIME_AI,
            args=args,
            target=self._digest_target(target),
            append_to_reader=True
        )

    def set_target(
            self, name: Textable,
            *, target: typing.Optional[EntityTarget] = None
    ):
        """Instructs the mob's AI to target a specific mob or player.

        .. rank:: Overlord


        Parameters
        ----------
        name : :attr:`~.Textable`
            Target name.

        target : Optional[:class:`~.EntityTarget`], optional
            The target of this :class:`~.EntityAction`, or None for the current :class:`Entity` instance's target.
            Defaults to ``None``.

        Returns
        -------
        :class:`EntityAction`
            The generated EntityAction instance.

        Examples
        --------
        ::

            last_entity.set_target(name)
            # OR
            Entity(EntityTarget.LAST_ENTITY).set_target(name)  # TODO: Example
        """
        args = Arguments([
            p_check(name, Textable, "name")
        ])
        return EntityAction(
            action=EntityActionType.SET_TARGET,
            args=args,
            target=self._digest_target(target),
            append_to_reader=True
        )

    def set_trop_fish_type(
            self,
            *, pattern_color="Don't Change", body_color="Don't Change", pattern="Don't Change",
            target: typing.Optional[EntityTarget] = None
    ):
        """Sets the appearance of a tropical fish.

        Parameters
        ----------
        pattern_color :
            White, Orange, Magenta, Light Blue, Yellow, Lime, Pink, Gray, Light Gray, Cyan, Purple, Blue, Brown, Green, Red, Black, Don't Change

        body_color :
            White, Orange, Magenta, Light Blue, Yellow, Lime, Pink, Gray, Light Gray, Cyan, Purple, Blue, Brown, Green, Red, Black, Don't Change

        pattern :
            Kob, Sunstreak, Snooper, Dasher, Brinely, Spotty, Flopper, Stripey, Glitter, Blockfish, Betty, Clayfish, Don't Change

        target : Optional[:class:`~.EntityTarget`], optional
            The target of this :class:`~.EntityAction`, or None for the current :class:`Entity` instance's target.
            Defaults to ``None``.

        Returns
        -------
        :class:`EntityAction`
            The generated EntityAction instance.

        Examples
        --------
        ::

            last_entity.set_trop_fish_type()
            # OR
            Entity(EntityTarget.LAST_ENTITY).set_trop_fish_type()  # TODO: Example
        """
        args = Arguments([], tags=[
            Tag(
                "Pattern Color", option=pattern_color,  # default is Don't Change
                action=EntityActionType.SET_TROP_FISH_TYPE, block=BlockType.IF_GAME
            ),
            Tag(
                "Body Color", option=body_color,  # default is Don't Change
                action=EntityActionType.SET_TROP_FISH_TYPE, block=BlockType.IF_GAME
            ),
            Tag(
                "Pattern", option=pattern,  # default is Don't Change
                action=EntityActionType.SET_TROP_FISH_TYPE, block=BlockType.IF_GAME
            )
        ])
        return EntityAction(
            action=EntityActionType.SET_TROP_FISH_TYPE,
            args=args,
            target=self._digest_target(target),
            append_to_reader=True
        )

    def set_villager_prof(
            self,
            *, profession="None",
            target: typing.Optional[EntityTarget] = None
    ):
        """Sets a villager's profession.

        Parameters
        ----------
        profession :
            None, Armorer, Butcher, Cartographer, Cleric, Farmer, Fisherman, Fletcher, Leatherworker, Librarian, Mason, Nitwit, Shepherd, Toolsmith, Weaponsmith

        target : Optional[:class:`~.EntityTarget`], optional
            The target of this :class:`~.EntityAction`, or None for the current :class:`Entity` instance's target.
            Defaults to ``None``.

        Returns
        -------
        :class:`EntityAction`
            The generated EntityAction instance.

        Examples
        --------
        ::

            last_entity.set_villager_prof()
            # OR
            Entity(EntityTarget.LAST_ENTITY).set_villager_prof()  # TODO: Example
        """
        args = Arguments([], tags=[
            Tag(
                "Profession", option=profession,  # default is None
                action=EntityActionType.SET_VILLAGER_PROF, block=BlockType.IF_GAME
            )
        ])
        return EntityAction(
            action=EntityActionType.SET_VILLAGER_PROF,
            args=args,
            target=self._digest_target(target),
            append_to_reader=True
        )

    def set_villager_type(
            self,
            *, biome="Desert",
            target: typing.Optional[EntityTarget] = None
    ):
        """Sets the biome type of a villager.

        Parameters
        ----------
        biome :
            Desert, Jungle, Plains, Savanna, Snow, Swamp, Taiga

        target : Optional[:class:`~.EntityTarget`], optional
            The target of this :class:`~.EntityAction`, or None for the current :class:`Entity` instance's target.
            Defaults to ``None``.

        Returns
        -------
        :class:`EntityAction`
            The generated EntityAction instance.

        Examples
        --------
        ::

            last_entity.set_villager_type()
            # OR
            Entity(EntityTarget.LAST_ENTITY).set_villager_type()  # TODO: Example
        """
        args = Arguments([], tags=[
            Tag(
                "Biome", option=biome,  # default is Desert
                action=EntityActionType.SET_VILLAGER_TYPE, block=BlockType.IF_GAME
            )
        ])
        return EntityAction(
            action=EntityActionType.SET_VILLAGER_TYPE,
            args=args,
            target=self._digest_target(target),
            append_to_reader=True
        )

    def set_wolf_angry(
            self,
            *, is_angry: bool = True,
            target: typing.Optional[EntityTarget] = None
    ):
        """Sets whether a wolf is angry.

        Parameters
        ----------
        is_angry : :class:`bool`, optional
            Defaults to ``True``.

        target : Optional[:class:`~.EntityTarget`], optional
            The target of this :class:`~.EntityAction`, or None for the current :class:`Entity` instance's target.
            Defaults to ``None``.

        Returns
        -------
        :class:`EntityAction`
            The generated EntityAction instance.

        Examples
        --------
        ::

            last_entity.set_wolf_angry()
            # OR
            Entity(EntityTarget.LAST_ENTITY).set_wolf_angry()  # TODO: Example
        """
        args = Arguments([], tags=[
            Tag(
                "Is Angry", option=bool(is_angry),  # default is True
                action=EntityActionType.SET_WOLF_ANGRY, block=BlockType.IF_GAME
            )
        ])
        return EntityAction(
            action=EntityActionType.SET_WOLF_ANGRY,
            args=args,
            target=self._digest_target(target),
            append_to_reader=True
        )

    def shear_sheep(self, *, target: typing.Optional[EntityTarget] = None):
        """Causes a sheep to be sheared.

        Parameters
        ----------
        target : Optional[:class:`~.EntityTarget`], optional
            The target of this :class:`~.EntityAction`, or None for the current :class:`Entity` instance's target.
            Defaults to ``None``.

        Returns
        -------
        :class:`EntityAction`
            The generated EntityAction instance.

        Examples
        --------
        ::

            last_entity.shear_sheep()
            # OR
            Entity(EntityTarget.LAST_ENTITY).shear_sheep()
        """
        return EntityAction(
            action=EntityActionType.SHEAR_SHEEP,
            args=Arguments(),
            target=self._digest_target(target),
            append_to_reader=True
        )

    def sheep_eat(self, *, target: typing.Optional[EntityTarget] = None):
        """Causes a sheep to eat grass.

        Parameters
        ----------
        target : Optional[:class:`~.EntityTarget`], optional
            The target of this :class:`~.EntityAction`, or None for the current :class:`Entity` instance's target.
            Defaults to ``None``.

        Returns
        -------
        :class:`EntityAction`
            The generated EntityAction instance.

        Examples
        --------
        ::

            last_entity.sheep_eat()
            # OR
            Entity(EntityTarget.LAST_ENTITY).sheep_eat()
        """
        return EntityAction(
            action=EntityActionType.SHEEP_EAT,
            args=Arguments(),
            target=self._digest_target(target),
            append_to_reader=True
        )

    def show_name(self, *, target: typing.Optional[EntityTarget] = None):
        """Shows the name tag of the entity.

        Parameters
        ----------
        target : Optional[:class:`~.EntityTarget`], optional
            The target of this :class:`~.EntityAction`, or None for the current :class:`Entity` instance's target.
            Defaults to ``None``.

        Returns
        -------
        :class:`EntityAction`
            The generated EntityAction instance.

        Examples
        --------
        ::

            last_entity.show_name()
            # OR
            Entity(EntityTarget.LAST_ENTITY).show_name()
        """
        return EntityAction(
            action=EntityActionType.SHOW_NAME,
            args=Arguments(),
            target=self._digest_target(target),
            append_to_reader=True
        )

    def silence(self, *, target: typing.Optional[EntityTarget] = None):
        """Prevents the entity from making any sounds.

        .. rank:: Noble


        Parameters
        ----------
        target : Optional[:class:`~.EntityTarget`], optional
            The target of this :class:`~.EntityAction`, or None for the current :class:`Entity` instance's target.
            Defaults to ``None``.

        Returns
        -------
        :class:`EntityAction`
            The generated EntityAction instance.

        Examples
        --------
        ::

            last_entity.silence()
            # OR
            Entity(EntityTarget.LAST_ENTITY).silence()
        """
        return EntityAction(
            action=EntityActionType.SILENCE,
            args=Arguments(),
            target=self._digest_target(target),
            append_to_reader=True
        )

    def snowman_pumpkin(
            self,
            *, has_pumpkin: bool = True,
            target: typing.Optional[EntityTarget] = None
    ):
        """Sets whether a snowman is wearing a pumpkin.

        Parameters
        ----------
        has_pumpkin : :class:`bool`, optional
            Defaults to ``True``.

        target : Optional[:class:`~.EntityTarget`], optional
            The target of this :class:`~.EntityAction`, or None for the current :class:`Entity` instance's target.
            Defaults to ``None``.

        Returns
        -------
        :class:`EntityAction`
            The generated EntityAction instance.

        Examples
        --------
        ::

            last_entity.snowman_pumpkin()
            # OR
            Entity(EntityTarget.LAST_ENTITY).snowman_pumpkin()  # TODO: Example
        """
        args = Arguments([], tags=[
            Tag(
                "Has Pumpkin", option=bool(has_pumpkin),  # default is True
                action=EntityActionType.SNOWMAN_PUMPKIN, block=BlockType.IF_GAME
            )
        ])
        return EntityAction(
            action=EntityActionType.SNOWMAN_PUMPKIN,
            args=args,
            target=self._digest_target(target),
            append_to_reader=True
        )

    def tame(
            self, name: typing.Optional[Textable] = None,
            *, target: typing.Optional[EntityTarget] = None
    ):
        """Tames the mob (if possible).

        Parameters
        ----------
        name : Optional[:attr:`~.Textable`], optional
            Name of owner. Default is ``None``.

        target : Optional[:class:`~.EntityTarget`], optional
            The target of this :class:`~.EntityAction`, or None for the current :class:`Entity` instance's target.
            Defaults to ``None``.

        Returns
        -------
        :class:`EntityAction`
            The generated EntityAction instance.

        Notes
        -----
        - Specifying no owner will untame the mob.
        - Can overwrite a previous owner.


        Examples
        --------
        ::

            last_entity.tame(name)
            # OR
            Entity(EntityTarget.LAST_ENTITY).tame(name)  # TODO: Example
        """
        args = Arguments([
            p_check(name, typing.Optional[Textable], "name") if name is not None else None
        ])
        return EntityAction(
            action=EntityActionType.TAME,
            args=args,
            target=self._digest_target(target),
            append_to_reader=True
        )

    def teleport(
            self, loc: Locatable,
            *, keep_current_rotation: bool = False,
            target: typing.Optional[EntityTarget] = None
    ):
        """Teleports the entity to a specified location.

        Parameters
        ----------
        loc : :attr:`~.Locatable`
            New position.

        keep_current_rotation : :class:`bool`, optional
            Defaults to ``False``.

        target : Optional[:class:`~.EntityTarget`], optional
            The target of this :class:`~.EntityAction`, or None for the current :class:`Entity` instance's target.
            Defaults to ``None``.

        Returns
        -------
        :class:`EntityAction`
            The generated EntityAction instance.

        Examples
        --------
        ::

            last_entity.teleport(loc)
            # OR
            Entity(EntityTarget.LAST_ENTITY).teleport(loc)  # TODO: Example
        """
        args = Arguments([
            p_check(loc, Locatable, "loc")
        ], tags=[
            Tag(
                "Keep Current Rotation", option=bool(keep_current_rotation),  # default is False
                action=EntityActionType.TELEPORT, block=BlockType.IF_GAME
            )
        ])
        return EntityAction(
            action=EntityActionType.TELEPORT,
            args=args,
            target=self._digest_target(target),
            append_to_reader=True
        )

    def tp_sequence(
            self, *locs: typing.Union[Locatable, Listable], ticks: typing.Optional[Numeric] = None,
            target: typing.Optional[EntityTarget] = None
    ):
        """Teleports the entity to multiple locations, with a delay between each teleport.

        .. rank:: Noble


        Parameters
        ----------
        locs : Union[:attr:`~.Locatable`, :attr:`~.Listable`]
            Locations to teleport to.

        ticks : Optional[:attr:`~.Numeric`], optional
            Teleport delay (ticks, default = 60). Default is ``None``.

        target : Optional[:class:`~.EntityTarget`], optional
            The target of this :class:`~.EntityAction`, or None for the current :class:`Entity` instance's target.
            Defaults to ``None``.

        Returns
        -------
        :class:`EntityAction`
            The generated EntityAction instance.

        Examples
        --------
        ::

            last_entity.tp_sequence(locs, ticks)
            # OR
            Entity(EntityTarget.LAST_ENTITY).tp_sequence(locs, ticks)  # TODO: Example
        """
        args = Arguments([
            *[p_check(loc, typing.Union[Locatable, Listable], f"locs[{i}]") for i, loc in enumerate(locs)],
            p_check(ticks, typing.Optional[Numeric], "ticks") if ticks is not None else None
        ])
        return EntityAction(
            action=EntityActionType.TP_SEQUENCE,
            args=args,
            target=self._digest_target(target),
            append_to_reader=True
        )

    def undisguise(self, *, target: typing.Optional[EntityTarget] = None):
        """Removes the entity's disguise.

        .. rank:: Overlord


        Parameters
        ----------
        target : Optional[:class:`~.EntityTarget`], optional
            The target of this :class:`~.EntityAction`, or None for the current :class:`Entity` instance's target.
            Defaults to ``None``.

        Returns
        -------
        :class:`EntityAction`
            The generated EntityAction instance.

        Examples
        --------
        ::

            last_entity.undisguise()
            # OR
            Entity(EntityTarget.LAST_ENTITY).undisguise()
        """
        return EntityAction(
            action=EntityActionType.UNDISGUISE,
            args=Arguments(),
            target=self._digest_target(target),
            append_to_reader=True
        )

    def unsilence(self, *, target: typing.Optional[EntityTarget] = None):
        """Allows the entity to make sounds.

        .. rank:: Noble


        Parameters
        ----------
        target : Optional[:class:`~.EntityTarget`], optional
            The target of this :class:`~.EntityAction`, or None for the current :class:`Entity` instance's target.
            Defaults to ``None``.

        Returns
        -------
        :class:`EntityAction`
            The generated EntityAction instance.

        Examples
        --------
        ::

            last_entity.unsilence()
            # OR
            Entity(EntityTarget.LAST_ENTITY).unsilence()
        """
        return EntityAction(
            action=EntityActionType.UNSILENCE,
            args=Arguments(),
            target=self._digest_target(target),
            append_to_reader=True
        )

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
        :class:`~.IfEntity`
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
        :class:`~.IfEntity`
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
        """Checks if an entity is within a certain distance of a location.

        Parameters
        ----------
        center : :attr:`~.Locatable`
            Center location with which to check how near the entity is to it.

        range : Optional[:attr:`~.Numeric`], optional
            Maximum distance permitted from the location, or ``None`` for the default (5 blocks). Default is ``None``.

        ignore_y_axis : :class:`bool`, optional
            Whether the Y-axis should be ignored when calculating distance. Defaults to ``False`` (no).

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

            center = DFLocation(1, 2, 3)  # where the entity should be near to
            distance = 10  # 10 blocks max distance
            with last_entity.is_near(center, distance, ignore_y_axis=False):
            # OR
            with Entity(EntityTarget.LAST_ENTITY).is_near(center, distance, ignore_y_axis=False):
                # ... code to be executed if the Last Spawned Entity is at most 10 blocks away from 'center' ...
        """
        args = Arguments([
            p_check(center, Locatable, "center"),
            p_check(range, Numeric, "distance") if range is not None else None
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
        :class:`~.IfEntity`
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
        :class:`~.IfEntity`
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
        _ = [
            p_check(el, typing.Union[ItemParam, Textable, Locatable], f"block_types_or_locs[{i}]")
            for i, el in enumerate(loaded_btypes)
        ]
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
        :class:`~.IfEntity`
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

    def is_projectile(self, *, target: typing.Optional[EntityTarget] = None):
        """Checks if an entity is a projectile.

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

            with last_entity.is_projectile():
            # OR
            with Entity(EntityTarget.LAST_ENTITY).is_projectile():
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
        :class:`~.IfEntity`
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
