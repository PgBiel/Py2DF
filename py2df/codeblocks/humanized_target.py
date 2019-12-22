import collections
import itertools
import typing

from ._block_utils import _load_btype, BlockParam, _load_btypes
from .actions import PlayerAction, EntityAction
from .ifs import IfPlayer, IfEntity
from ..classes import Arguments, ItemCollection, Tag
from ..enums import PlayerTarget, EntityTarget, PlayerActionType, EntityActionType, IfPlayerType, IfEntityType, \
    BlockType, PlayerHand, IfPOpenInvType
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
        hand: typing.Optional[PlayerHand] = None,
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
                "Hand Slot", option="Either Hand" if not hand else PlayerHand(hand).value,  # default is Either Hand
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
