import collections
import itertools
import typing

from .._block_utils import _load_btype, BlockParam, _load_btypes, BlockMetadata
from ..actions import PlayerAction
from ..ifs import IfPlayer, IfEntity
from ...classes import Arguments, ItemCollection, Tag, DFNumber
from ...enums import PlayerTarget, PlayerActionType, IfPlayerType, BlockType, Hand, IfPOpenInvType
from ...typings import Textable, Numeric, Locatable, ItemParam, Potionable, ParticleParam, p_check, SpawnEggable, \
    p_bool_check, Listable
from ...utils import remove_u200b_from_doc, flatten


__all__ = ("Player",)


class Player:
    """Represents a DiamondFire Player. Used for Player Action and If Player humanized methods.

    Parameters
    ----------\u200b
    target : Optional[:class:`~.PlayerTarget`], optional
        The target that this instance represents (Default Player, Killer, Victim etc.) or ``None`` for empty target
        (equivalent to leaving the target line empty on DF - becomes the current selection, or the Default
        Player). Defaults to ``None``.

    Attributes
    ----------\u200b
    target : Optional[:class:`~.PlayerTarget`]
        The target that this instance represents (Default Player, Killer, Victim etc.) or ``None`` for empty target
        (equivalent to leaving the target line empty on DF - becomes the current selection, or the Default
        Player).
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

    def action_bar(
            self, *texts: typing.Optional[typing.Union[Textable, Listable]],
            text_value_merging="No Spaces",
            target: typing.Optional[PlayerTarget] = None
    ):
        """Sends a message on the action bar for the selected player.

        .. rank:: Mythic


        Parameters
        ----------
        texts : Optional[Union[:attr:`~.Textable`, :attr:`~.Listable`]], optional
            Message to send. Default is ``None``.

        text_value_merging :
            Add Spaces, No Spaces

        target : Optional[:class:`~.PlayerTarget`], optional
            The target of this :class:`~.PlayerAction`, or None for the current :class:`Player` instance's target.
            Defaults to ``None``.

        Returns
        -------
        :class:`PlayerAction`
            The generated PlayerAction instance.

        Notes
        -----
        - Multiple text items will be merged into one message.
        - Numbers and locations in the chest will be converted to text.


        Examples
        --------
        ::

            p_default.action_bar(texts)
            # OR
            Player(PlayerTarget.DEFAULT).action_bar(texts)  # TODO: Example
        """
        args = Arguments([
            p_check(text, typing.Optional[typing.Union[Textable, Listable]], f"texts[{i}]") for i, text in
            enumerate(texts)
        ], tags=[
            Tag(
                "Text Value Merging", option=text_value_merging,  # default is No Spaces
                action=PlayerActionType.ACTION_BAR, block=BlockType.IF_GAME
            )
        ])
        return PlayerAction(
            action=PlayerActionType.ACTION_BAR,
            args=args,
            target=self._digest_target(target),
            append_to_reader=True
        )

    def add_inv_row(
            self,
            *items: typing.Optional[typing.Union[ItemParam, ItemCollection, typing.Iterable[ItemParam], Listable]],
            new_row_position="Bottom Row",
            target: typing.Optional[PlayerTarget] = None
    ):
        """Adds a row to the bottom of the currently open inventory.

        .. rank:: Emperor


        Parameters
        ----------
        items : Optional[Optional[Union[:class:`~.ItemParam`, :class:`~.ItemCollection`, Iterable[:class:`~.ItemParam`], :attr:`Listable`]]], optional
            Items to display. The items can be specified either as:

            - ``None`` for an empty slot;
            - :class:`~.Item` for one item;
            - :attr:`~.Listable` for a variable list of items;
            - :class:`~.ItemCollection` or Iterable[:class:`~.Item`] for a predetermined list of items.

        new_row_position :
            Top Row, Bottom Row

        target : Optional[:class:`~.PlayerTarget`], optional
            The target of this :class:`~.PlayerAction`, or None for the current :class:`Player` instance's target.
            Defaults to ``None``.

        Returns
        -------
        :class:`PlayerAction`
            The generated PlayerAction instance.

        Examples
        --------
        ::

            p_default.add_inv_row(items)
            # OR
            Player(PlayerTarget.DEFAULT).add_inv_row(items)  # TODO: Example
        """
        item_list = flatten(*items, except_iterables=[str], max_depth=1)

        args = Arguments([
            p_check(item, typing.Union[ItemParam, Listable], "items") for item in item_list
        ], tags=[
            Tag(
                "New Row Position", option=new_row_position,  # default is Bottom Row
                action=PlayerActionType.ADD_INV_ROW, block=BlockType.IF_GAME
            )
        ])
        return PlayerAction(
            action=PlayerActionType.ADD_INV_ROW,
            args=args,
            target=self._digest_target(target),
            append_to_reader=True
        )

    def allow_drops(self, *, target: typing.Optional[PlayerTarget] = None):
        """Allows the player to drop items from their inventory.

        Parameters
        ----------
        target : Optional[:class:`~.PlayerTarget`], optional
            The target of this :class:`~.PlayerAction`, or None for the current :class:`Player` instance's target.
            Defaults to ``None``.

        Returns
        -------
        :class:`PlayerAction`
            The generated PlayerAction instance.

        Examples
        --------
        ::

            p_default.allow_drops()
            # OR
            Player(PlayerTarget.DEFAULT).allow_drops()
        """
        return PlayerAction(
            action=PlayerActionType.ALLOW_DROPS,
            args=Arguments(),
            target=self._digest_target(target),
            append_to_reader=True
        )

    def block_disguise(
            self, block_type: BlockParam, name: typing.Optional[Textable] = None,
            *, target: typing.Optional[PlayerTarget] = None
    ):
        """Disguises the player as a block.

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
            Name of disguise. Default is ``None``.

        target : Optional[:class:`~.PlayerTarget`], optional
            The target of this :class:`~.PlayerAction`, or None for the current :class:`Player` instance's target.
            Defaults to ``None``.

        Returns
        -------
        :class:`PlayerAction`
            The generated PlayerAction instance.

        Examples
        --------
        ::

            p_default.block_disguise(block_type, name)
            # OR
            Player(PlayerTarget.DEFAULT).block_disguise(block_type, name)  # TODO: Example
        """
        args = Arguments([
            p_check(block_type, typing.Union[ItemParam, Textable], "block_type"),
            p_check(name, typing.Optional[Textable], "name") if name is not None else None
        ])
        return PlayerAction(
            action=PlayerActionType.BLOCK_DISGUISE,
            args=args,
            target=self._digest_target(target),
            append_to_reader=True
        )

    def break_animation(
            self, *locs: typing.Union[Locatable, Listable], level: typing.Optional[Numeric] = None,
            overwrite_previous_fracture: bool = True,
            target: typing.Optional[PlayerTarget] = None
    ):
        """Makes the player see block fractures on the given blocks.

        Parameters
        ----------
        locs : Union[:attr:`~.Locatable`, :attr:`~.Listable`]
            Block(s) to fracture.

        level : Optional[:attr:`~.Numeric`], optional
            Fracture level (1 to 10). Default is ``None``.

        overwrite_previous_fracture : :class:`bool`, optional
            Defaults to ``True``.

        target : Optional[:class:`~.PlayerTarget`], optional
            The target of this :class:`~.PlayerAction`, or None for the current :class:`Player` instance's target.
            Defaults to ``None``.

        Returns
        -------
        :class:`PlayerAction`
            The generated PlayerAction instance.

        Notes
        -----
        - Not specifying a fracture level will clear the block's fracture effect.
        - Fracture animations automatically disappear after 20 seconds.


        Examples
        --------
        ::

            p_default.break_animation(locs, level)
            # OR
            Player(PlayerTarget.DEFAULT).break_animation(locs, level)  # TODO: Example
        """
        args = Arguments([
            *[p_check(loc, typing.Union[Locatable, Listable], f"locs[{i}]") for i, loc in enumerate(locs)],
            p_check(level, typing.Optional[Numeric], "level") if level is not None else None
        ], tags=[
            Tag(
                "Overwrite Previous Fracture", option=bool(overwrite_previous_fracture),  # default is True
                action=PlayerActionType.BREAK_ANIMATION, block=BlockType.IF_GAME
            )
        ])
        return PlayerAction(
            action=PlayerActionType.BREAK_ANIMATION,
            args=args,
            target=self._digest_target(target),
            append_to_reader=True
        )

    def chat_color(
            self, text: Textable,
            *, target: typing.Optional[PlayerTarget] = None
    ):
        """Sets the color of all future messages in chat for the player.

        .. rank:: Overlord


        Parameters
        ----------
        text : :attr:`~.Textable`
            New chat color.

        target : Optional[:class:`~.PlayerTarget`], optional
            The target of this :class:`~.PlayerAction`, or None for the current :class:`Player` instance's target.
            Defaults to ``None``.

        Returns
        -------
        :class:`PlayerAction`
            The generated PlayerAction instance.

        Examples
        --------
        ::

            p_default.chat_color(text)
            # OR
            Player(PlayerTarget.DEFAULT).chat_color(text)  # TODO: Example
        """
        args = Arguments([
            p_check(text, Textable, "text")
        ])
        return PlayerAction(
            action=PlayerActionType.CHAT_COLOR,
            args=args,
            target=self._digest_target(target),
            append_to_reader=True
        )

    def clear_chat(self, *, target: typing.Optional[PlayerTarget] = None):
        """Clears all messages on the player's chat window.

        Parameters
        ----------
        target : Optional[:class:`~.PlayerTarget`], optional
            The target of this :class:`~.PlayerAction`, or None for the current :class:`Player` instance's target.
            Defaults to ``None``.

        Returns
        -------
        :class:`PlayerAction`
            The generated PlayerAction instance.

        Examples
        --------
        ::

            p_default.clear_chat()
            # OR
            Player(PlayerTarget.DEFAULT).clear_chat()
        """
        return PlayerAction(
            action=PlayerActionType.CLEAR_CHAT,
            args=Arguments(),
            target=self._digest_target(target),
            append_to_reader=True
        )

    def clear_effects(self, *, target: typing.Optional[PlayerTarget] = None):
        """Removes all potion effects from the player.

        Parameters
        ----------
        target : Optional[:class:`~.PlayerTarget`], optional
            The target of this :class:`~.PlayerAction`, or None for the current :class:`Player` instance's target.
            Defaults to ``None``.

        Returns
        -------
        :class:`PlayerAction`
            The generated PlayerAction instance.

        Examples
        --------
        ::

            p_default.clear_effects()
            # OR
            Player(PlayerTarget.DEFAULT).clear_effects()
        """
        return PlayerAction(
            action=PlayerActionType.CLEAR_EFFECTS,
            args=Arguments(),
            target=self._digest_target(target),
            append_to_reader=True
        )

    def clear_inv(
            self,
            *, clear_mode="Entire Inventory", clear_crafting_and_cursor: bool = True,
            target: typing.Optional[PlayerTarget] = None
    ):
        """Empties the player's inventory.

        Parameters
        ----------
        clear_mode :
            Entire Inventory, Upper Inventory, Hotbar, Armor

        clear_crafting_and_cursor : :class:`bool`, optional
            Defaults to ``True``.

        target : Optional[:class:`~.PlayerTarget`], optional
            The target of this :class:`~.PlayerAction`, or None for the current :class:`Player` instance's target.
            Defaults to ``None``.

        Returns
        -------
        :class:`PlayerAction`
            The generated PlayerAction instance.

        Examples
        --------
        ::

            p_default.clear_inv()
            # OR
            Player(PlayerTarget.DEFAULT).clear_inv()  # TODO: Example
        """
        args = Arguments([], tags=[
            Tag(
                "Clear Mode", option=clear_mode,  # default is Entire Inventory
                action=PlayerActionType.CLEAR_INV, block=BlockType.IF_GAME
            ),
            Tag(
                "Clear Crafting and Cursor", option=bool(clear_crafting_and_cursor),  # default is True
                action=PlayerActionType.CLEAR_INV, block=BlockType.IF_GAME
            )
        ])
        return PlayerAction(
            action=PlayerActionType.CLEAR_INV,
            args=args,
            target=self._digest_target(target),
            append_to_reader=True
        )

    def clear_item(
            self, *items: typing.Union[ItemParam, ItemCollection, typing.Iterable[ItemParam], Listable],
            target: typing.Optional[PlayerTarget] = None
    ):
        """Removes all of a certain item from the player.

        Parameters
        ----------
        items : Optional[Union[:class:`~.ItemParam`, :class:`~.ItemCollection`, Iterable[:class:`~.ItemParam`], :attr:`Listable`]]
            Item(s) to clear. The items can be specified either as:

            - ``None`` for an empty slot;
            - :class:`~.Item` for one item;
            - :attr:`~.Listable` for a variable list of items;
            - :class:`~.ItemCollection` or Iterable[:class:`~.Item`] for a predetermined list of items.

        target : Optional[:class:`~.PlayerTarget`], optional
            The target of this :class:`~.PlayerAction`, or None for the current :class:`Player` instance's target.
            Defaults to ``None``.

        Returns
        -------
        :class:`PlayerAction`
            The generated PlayerAction instance.

        Examples
        --------
        ::

            p_default.clear_item(items)
            # OR
            Player(PlayerTarget.DEFAULT).clear_item(items)  # TODO: Example
        """
        item_list = flatten(*items, except_iterables=[str], max_depth=1)

        args = Arguments([
            p_check(item, typing.Union[ItemParam, Listable], "items") for item in item_list
        ])
        return PlayerAction(
            action=PlayerActionType.CLEAR_ITEM,
            args=args,
            target=self._digest_target(target),
            append_to_reader=True
        )

    def close_inv(self, *, target: typing.Optional[PlayerTarget] = None):
        """Closes the player's currently open inventory menu.

        .. rank:: Emperor


        Parameters
        ----------
        target : Optional[:class:`~.PlayerTarget`], optional
            The target of this :class:`~.PlayerAction`, or None for the current :class:`Player` instance's target.
            Defaults to ``None``.

        Returns
        -------
        :class:`PlayerAction`
            The generated PlayerAction instance.

        Examples
        --------
        ::

            p_default.close_inv()
            # OR
            Player(PlayerTarget.DEFAULT).close_inv()
        """
        return PlayerAction(
            action=PlayerActionType.CLOSE_INV,
            args=Arguments(),
            target=self._digest_target(target),
            append_to_reader=True
        )

    def damage(
            self, damage: Numeric,
            *, target: typing.Optional[PlayerTarget] = None
    ):
        """Damages the player.

        Parameters
        ----------
        damage : :attr:`~.Numeric`
            Damage to inflict.

        .. note::

            1 damage = 0.5 hearts


        target : Optional[:class:`~.PlayerTarget`], optional
            The target of this :class:`~.PlayerAction`, or None for the current :class:`Player` instance's target.
            Defaults to ``None``.

        Returns
        -------
        :class:`PlayerAction`
            The generated PlayerAction instance.

        Examples
        --------
        ::

            p_default.damage(damage)
            # OR
            Player(PlayerTarget.DEFAULT).damage(damage)  # TODO: Example
        """
        args = Arguments([
            p_check(damage, Numeric, "damage")
        ])
        return PlayerAction(
            action=PlayerActionType.DAMAGE,
            args=args,
            target=self._digest_target(target),
            append_to_reader=True
        )

    def death_drops(self, *, target: typing.Optional[PlayerTarget] = None):
        """When this code block is executed, the player will drop the contents of their inventory when they die.

        Parameters
        ----------
        target : Optional[:class:`~.PlayerTarget`], optional
            The target of this :class:`~.PlayerAction`, or None for the current :class:`Player` instance's target.
            Defaults to ``None``.

        Returns
        -------
        :class:`PlayerAction`
            The generated PlayerAction instance.

        Examples
        --------
        ::

            p_default.death_drops()
            # OR
            Player(PlayerTarget.DEFAULT).death_drops()
        """
        return PlayerAction(
            action=PlayerActionType.DEATH_DROPS,
            args=Arguments(),
            target=self._digest_target(target),
            append_to_reader=True
        )

    def disable_blocks(
            self, *block_types: typing.Optional[typing.Union[BlockParam, Listable]],
            target: typing.Optional[PlayerTarget] = None
    ):
        """Prevents the player from placing and breaking certain blocks. If no blocks are in the chest, all blocks will be disallowed.

        .. rank:: Noble


        Parameters
        ----------
        block_types : Optional[Union[:class:`Material`, :attr:`~.ItemParam`, :attr:`~.Textable`, :attr:`~.Listable`]], optional
            The type of Blocks to disallow.

            The type can be specified either as:

            - an instance of :class:`~.Material` (the material of the block to set);
            - an item (:attr:`~.ItemParam` - the item representing the block to set);
            - text (:attr:`~.Textable` - the material of the block to set as text);
            - a :attr:`~.Listable` (A List - in DF - variable containing either Item or Text parameters).

        target : Optional[:class:`~.PlayerTarget`], optional
            The target of this :class:`~.PlayerAction`, or None for the current :class:`Player` instance's target.
            Defaults to ``None``.

        Returns
        -------
        :class:`PlayerAction`
            The generated PlayerAction instance.

        Examples
        --------
        ::

            p_default.disable_blocks(block_types)
            # OR
            Player(PlayerTarget.DEFAULT).disable_blocks(block_types)  # TODO: Example
        """
        true_btypes = _load_btypes(block_types)

        args = Arguments([
            p_check(block_type, typing.Union[ItemParam, Textable], f"block_types[{i}]") for i, block_type in
            enumerate(true_btypes)
        ])
        return PlayerAction(
            action=PlayerActionType.DISABLE_BLOCKS,
            args=args,
            target=self._digest_target(target),
            append_to_reader=True
        )

    def disable_flight(self, *, target: typing.Optional[PlayerTarget] = None):
        """Prevents the player from flying.

        Parameters
        ----------
        target : Optional[:class:`~.PlayerTarget`], optional
            The target of this :class:`~.PlayerAction`, or None for the current :class:`Player` instance's target.
            Defaults to ``None``.

        Returns
        -------
        :class:`PlayerAction`
            The generated PlayerAction instance.

        Examples
        --------
        ::

            p_default.disable_flight()
            # OR
            Player(PlayerTarget.DEFAULT).disable_flight()
        """
        return PlayerAction(
            action=PlayerActionType.DISABLE_FLIGHT,
            args=Arguments(),
            target=self._digest_target(target),
            append_to_reader=True
        )

    def disable_pvp(self, *, target: typing.Optional[PlayerTarget] = None):
        """Prevents the player from damaging other players.

        Parameters
        ----------
        target : Optional[:class:`~.PlayerTarget`], optional
            The target of this :class:`~.PlayerAction`, or None for the current :class:`Player` instance's target.
            Defaults to ``None``.

        Returns
        -------
        :class:`PlayerAction`
            The generated PlayerAction instance.

        Examples
        --------
        ::

            p_default.disable_pvp()
            # OR
            Player(PlayerTarget.DEFAULT).disable_pvp()
        """
        return PlayerAction(
            action=PlayerActionType.DISABLE_PVP,
            args=Arguments(),
            target=self._digest_target(target),
            append_to_reader=True
        )

    def disallow_drops(self, *, target: typing.Optional[PlayerTarget] = None):
        """Prevents the player from dropping items from their inventory.

        Parameters
        ----------
        target : Optional[:class:`~.PlayerTarget`], optional
            The target of this :class:`~.PlayerAction`, or None for the current :class:`Player` instance's target.
            Defaults to ``None``.

        Returns
        -------
        :class:`PlayerAction`
            The generated PlayerAction instance.

        Examples
        --------
        ::

            p_default.disallow_drops()
            # OR
            Player(PlayerTarget.DEFAULT).disallow_drops()
        """
        return PlayerAction(
            action=PlayerActionType.DISALLOW_DROPS,
            args=Arguments(),
            target=self._digest_target(target),
            append_to_reader=True
        )

    def enable_blocks(
            self, *block_types: typing.Optional[typing.Union[BlockParam, Listable]],
            target: typing.Optional[PlayerTarget] = None
    ):
        """Allows the player to place and break certain blocks. If no blocks are in the chest, all blocks will be enabled.

        .. rank:: Noble


        Parameters
        ----------
        block_types : Optional[Union[:class:`Material`, :attr:`~.ItemParam`, :attr:`~.Textable`, :attr:`~.Listable`]], optional
            The type of Blocks to allow.

            The type can be specified either as:

            - an instance of :class:`~.Material` (the material of the block to set);
            - an item (:attr:`~.ItemParam` - the item representing the block to set);
            - text (:attr:`~.Textable` - the material of the block to set as text);
            - a :attr:`~.Listable` (A List - in DF - variable containing either Item or Text parameters).

        target : Optional[:class:`~.PlayerTarget`], optional
            The target of this :class:`~.PlayerAction`, or None for the current :class:`Player` instance's target.
            Defaults to ``None``.

        Returns
        -------
        :class:`PlayerAction`
            The generated PlayerAction instance.

        Examples
        --------
        ::

            p_default.enable_blocks(block_types)
            # OR
            Player(PlayerTarget.DEFAULT).enable_blocks(block_types)  # TODO: Example
        """
        true_btypes = _load_btypes(block_types)

        args = Arguments([
            p_check(block_type, typing.Union[ItemParam, Textable], f"block_types[{i}]") for i, block_type in
            enumerate(true_btypes)
        ])
        return PlayerAction(
            action=PlayerActionType.ENABLE_BLOCKS,
            args=args,
            target=self._digest_target(target),
            append_to_reader=True
        )

    def enable_flight(self, *, target: typing.Optional[PlayerTarget] = None):
        """Allows the player to fly.

        Parameters
        ----------
        target : Optional[:class:`~.PlayerTarget`], optional
            The target of this :class:`~.PlayerAction`, or None for the current :class:`Player` instance's target.
            Defaults to ``None``.

        Returns
        -------
        :class:`PlayerAction`
            The generated PlayerAction instance.

        Examples
        --------
        ::

            p_default.enable_flight()
            # OR
            Player(PlayerTarget.DEFAULT).enable_flight()
        """
        return PlayerAction(
            action=PlayerActionType.ENABLE_FLIGHT,
            args=Arguments(),
            target=self._digest_target(target),
            append_to_reader=True
        )

    def enable_pvp(self, *, target: typing.Optional[PlayerTarget] = None):
        """Allows the player to damage other players.

        Parameters
        ----------
        target : Optional[:class:`~.PlayerTarget`], optional
            The target of this :class:`~.PlayerAction`, or None for the current :class:`Player` instance's target.
            Defaults to ``None``.

        Returns
        -------
        :class:`PlayerAction`
            The generated PlayerAction instance.

        Examples
        --------
        ::

            p_default.enable_pvp()
            # OR
            Player(PlayerTarget.DEFAULT).enable_pvp()
        """
        return PlayerAction(
            action=PlayerActionType.ENABLE_PVP,
            args=Arguments(),
            target=self._digest_target(target),
            append_to_reader=True
        )

    def expand_inv(
            self,
            *items: typing.Optional[typing.Union[ItemParam, ItemCollection, typing.Iterable[ItemParam], Listable]],
            target: typing.Optional[PlayerTarget] = None
    ):
        """If an inventory menu is open for the player, 'Expand Inventory Menu' adds 3 more rows using the contents of the chest.

        .. rank:: Emperor


        Parameters
        ----------
        items : Optional[Optional[Union[:class:`~.ItemParam`, :class:`~.ItemCollection`, Iterable[:class:`~.ItemParam`], :attr:`Listable`]]], optional
            Items to display. The items can be specified either as:

            - ``None`` for an empty slot;
            - :class:`~.Item` for one item;
            - :attr:`~.Listable` for a variable list of items;
            - :class:`~.ItemCollection` or Iterable[:class:`~.Item`] for a predetermined list of items.

        target : Optional[:class:`~.PlayerTarget`], optional
            The target of this :class:`~.PlayerAction`, or None for the current :class:`Player` instance's target.
            Defaults to ``None``.

        Returns
        -------
        :class:`PlayerAction`
            The generated PlayerAction instance.

        Examples
        --------
        ::

            p_default.expand_inv(items)
            # OR
            Player(PlayerTarget.DEFAULT).expand_inv(items)  # TODO: Example
        """
        item_list = flatten(*items, except_iterables=[str], max_depth=1)

        args = Arguments([
            p_check(item, typing.Union[ItemParam, Listable], "items") for item in item_list
        ])
        return PlayerAction(
            action=PlayerActionType.EXPAND_INV,
            args=args,
            target=self._digest_target(target),
            append_to_reader=True
        )

    def flight_speed(
            self, speed: Numeric,
            *, target: typing.Optional[PlayerTarget] = None
    ):
        """Sets the player's flight speed.

        .. rank:: Noble


        Parameters
        ----------
        speed : :attr:`~.Numeric`
            % of normal flight speed (-1000 to 1000).

        target : Optional[:class:`~.PlayerTarget`], optional
            The target of this :class:`~.PlayerAction`, or None for the current :class:`Player` instance's target.
            Defaults to ``None``.

        Returns
        -------
        :class:`PlayerAction`
            The generated PlayerAction instance.

        Examples
        --------
        ::

            p_default.flight_speed(speed)
            # OR
            Player(PlayerTarget.DEFAULT).flight_speed(speed)  # TODO: Example
        """
        args = Arguments([
            p_check(speed, Numeric, "speed")
        ])
        return PlayerAction(
            action=PlayerActionType.FLIGHT_SPEED,
            args=args,
            target=self._digest_target(target),
            append_to_reader=True
        )

    def force_flight(
            self,
            *, flight_mode="Start Flight",
            target: typing.Optional[PlayerTarget] = None
    ):
        """Forces the player to start or stop flying.

        Parameters
        ----------
        flight_mode :
            Start Flight, Stop Flight

        target : Optional[:class:`~.PlayerTarget`], optional
            The target of this :class:`~.PlayerAction`, or None for the current :class:`Player` instance's target.
            Defaults to ``None``.

        Returns
        -------
        :class:`PlayerAction`
            The generated PlayerAction instance.

        Examples
        --------
        ::

            p_default.force_flight()
            # OR
            Player(PlayerTarget.DEFAULT).force_flight()  # TODO: Example
        """
        args = Arguments([], tags=[
            Tag(
                "Flight Mode", option=flight_mode,  # default is Start Flight
                action=PlayerActionType.FORCE_FLIGHT, block=BlockType.IF_GAME
            )
        ])
        return PlayerAction(
            action=PlayerActionType.FORCE_FLIGHT,
            args=args,
            target=self._digest_target(target),
            append_to_reader=True
        )

    def force_glide(
            self,
            *, glide_mode="Start Gliding",
            target: typing.Optional[PlayerTarget] = None
    ):
        """Forces the player to start or stop gliding.

        Parameters
        ----------
        glide_mode :
            Start Gliding, Stop Gliding

        target : Optional[:class:`~.PlayerTarget`], optional
            The target of this :class:`~.PlayerAction`, or None for the current :class:`Player` instance's target.
            Defaults to ``None``.

        Returns
        -------
        :class:`PlayerAction`
            The generated PlayerAction instance.

        Examples
        --------
        ::

            p_default.force_glide()
            # OR
            Player(PlayerTarget.DEFAULT).force_glide()  # TODO: Example
        """
        args = Arguments([], tags=[
            Tag(
                "Glide Mode", option=glide_mode,  # default is Start Gliding
                action=PlayerActionType.FORCE_GLIDE, block=BlockType.IF_GAME
            )
        ])
        return PlayerAction(
            action=PlayerActionType.FORCE_GLIDE,
            args=args,
            target=self._digest_target(target),
            append_to_reader=True
        )

    def give_effect(
            self, *potions: typing.Union[Potionable, Listable],
            effect_particle_mode="Shown", overwrite_existing_effect: bool = False,
            target: typing.Optional[PlayerTarget] = None
    ):
        """Gives the player one or more potion effects.

        Parameters
        ----------
        potions : Union[:attr:`~.Potionable`, :attr:`~.Listable`]
            Potion effects.

        effect_particle_mode :
            Shown, Beacon, Hidden

        overwrite_existing_effect : :class:`bool`, optional
            Defaults to ``False``.

        target : Optional[:class:`~.PlayerTarget`], optional
            The target of this :class:`~.PlayerAction`, or None for the current :class:`Player` instance's target.
            Defaults to ``None``.

        Returns
        -------
        :class:`PlayerAction`
            The generated PlayerAction instance.

        Examples
        --------
        ::

            p_default.give_effect(potions)
            # OR
            Player(PlayerTarget.DEFAULT).give_effect(potions)  # TODO: Example
        """
        args = Arguments([
            p_check(potion, typing.Union[Potionable, Listable], f"potions[{i}]") for i, potion in enumerate(potions)
        ], tags=[
            Tag(
                "Effect Particle Mode", option=effect_particle_mode,  # default is Shown
                action=PlayerActionType.GIVE_EFFECT, block=BlockType.IF_GAME
            ),
            Tag(
                "Overwrite Existing Effect", option=bool(overwrite_existing_effect),  # default is False
                action=PlayerActionType.GIVE_EFFECT, block=BlockType.IF_GAME
            )
        ])
        return PlayerAction(
            action=PlayerActionType.GIVE_EFFECT,
            args=args,
            target=self._digest_target(target),
            append_to_reader=True
        )

    def give_items(
            self, *items: typing.Union[ItemParam, ItemCollection, typing.Iterable[ItemParam], Listable],
            amount: typing.Optional[Numeric] = None,
            target: typing.Optional[PlayerTarget] = None
    ):
        """Gives the player all of the items in the chest.

        Parameters
        ----------
        items : Optional[Union[:class:`~.ItemParam`, :class:`~.ItemCollection`, Iterable[:class:`~.ItemParam`], :attr:`Listable`]]
            Item(s) to give. The items can be specified either as:

            - ``None`` for an empty slot;
            - :class:`~.Item` for one item;
            - :attr:`~.Listable` for a variable list of items;
            - :class:`~.ItemCollection` or Iterable[:class:`~.Item`] for a predetermined list of items.

        amount : Optional[:attr:`~.Numeric`], optional
            Amount to give. Default is ``None``.

        target : Optional[:class:`~.PlayerTarget`], optional
            The target of this :class:`~.PlayerAction`, or None for the current :class:`Player` instance's target.
            Defaults to ``None``.

        Returns
        -------
        :class:`PlayerAction`
            The generated PlayerAction instance.

        Notes
        -----
        If an amount is specified, the items will be repeatedly given that many times.


        Examples
        --------
        ::

            p_default.give_items(items, amount)
            # OR
            Player(PlayerTarget.DEFAULT).give_items(items, amount)  # TODO: Example
        """
        item_list = flatten(*items, except_iterables=[str], max_depth=1)

        args = Arguments([
            *[p_check(item, typing.Union[ItemParam, Listable], "items") for item in item_list],
            p_check(amount, typing.Optional[Numeric], "amount") if amount is not None else None
        ])
        return PlayerAction(
            action=PlayerActionType.GIVE_ITEMS,
            args=args,
            target=self._digest_target(target),
            append_to_reader=True
        )

    def give_rng_item(
            self, *items: typing.Union[ItemParam, ItemCollection, typing.Iterable[ItemParam], Listable],
            target: typing.Optional[PlayerTarget] = None
    ):
        """Gives the player a random item or stack of items from the chest.

        Parameters
        ----------
        items : Optional[Union[:class:`~.ItemParam`, :class:`~.ItemCollection`, Iterable[:class:`~.ItemParam`], :attr:`Listable`]]
            Items to pick from. The items can be specified either as:

            - ``None`` for an empty slot;
            - :class:`~.Item` for one item;
            - :attr:`~.Listable` for a variable list of items;
            - :class:`~.ItemCollection` or Iterable[:class:`~.Item`] for a predetermined list of items.

        target : Optional[:class:`~.PlayerTarget`], optional
            The target of this :class:`~.PlayerAction`, or None for the current :class:`Player` instance's target.
            Defaults to ``None``.

        Returns
        -------
        :class:`PlayerAction`
            The generated PlayerAction instance.

        Notes
        -----
        Will give a different item to each targeted player.


        Examples
        --------
        ::

            p_default.give_rng_item(items)
            # OR
            Player(PlayerTarget.DEFAULT).give_rng_item(items)  # TODO: Example
        """
        item_list = flatten(*items, except_iterables=[str], max_depth=1)

        args = Arguments([
            p_check(item, typing.Union[ItemParam, Listable], "items") for item in item_list
        ])
        return PlayerAction(
            action=PlayerActionType.GIVE_RNG_ITEM,
            args=args,
            target=self._digest_target(target),
            append_to_reader=True
        )

    def gm_adventure(self, *, target: typing.Optional[PlayerTarget] = None):
        """Sets the player's gamemode to adventure mode.

        Parameters
        ----------
        target : Optional[:class:`~.PlayerTarget`], optional
            The target of this :class:`~.PlayerAction`, or None for the current :class:`Player` instance's target.
            Defaults to ``None``.

        Returns
        -------
        :class:`PlayerAction`
            The generated PlayerAction instance.

        Examples
        --------
        ::

            p_default.gm_adventure()
            # OR
            Player(PlayerTarget.DEFAULT).gm_adventure()
        """
        return PlayerAction(
            action=PlayerActionType.GM_ADVENTURE,
            args=Arguments(),
            target=self._digest_target(target),
            append_to_reader=True
        )

    def gm_creative(self, *, target: typing.Optional[PlayerTarget] = None):
        """Sets the player's gamemode to creative mode.

        Parameters
        ----------
        target : Optional[:class:`~.PlayerTarget`], optional
            The target of this :class:`~.PlayerAction`, or None for the current :class:`Player` instance's target.
            Defaults to ``None``.

        Returns
        -------
        :class:`PlayerAction`
            The generated PlayerAction instance.

        Notes
        -----
        - BE WARNED, the player can spawn in any item they wish through the use of toolbars!
        - Click own inventory events may not work as expected.


        Examples
        --------
        ::

            p_default.gm_creative()
            # OR
            Player(PlayerTarget.DEFAULT).gm_creative()
        """
        return PlayerAction(
            action=PlayerActionType.GM_CREATIVE,
            args=Arguments(),
            target=self._digest_target(target),
            append_to_reader=True
        )

    def gm_survival(self, *, target: typing.Optional[PlayerTarget] = None):
        """Sets the player's gamemode to survival mode.

        Parameters
        ----------
        target : Optional[:class:`~.PlayerTarget`], optional
            The target of this :class:`~.PlayerAction`, or None for the current :class:`Player` instance's target.
            Defaults to ``None``.

        Returns
        -------
        :class:`PlayerAction`
            The generated PlayerAction instance.

        Examples
        --------
        ::

            p_default.gm_survival()
            # OR
            Player(PlayerTarget.DEFAULT).gm_survival()
        """
        return PlayerAction(
            action=PlayerActionType.GM_SURVIVAL,
            args=Arguments(),
            target=self._digest_target(target),
            append_to_reader=True
        )

    def heal(
            self, amount: typing.Optional[Numeric] = None,
            *, target: typing.Optional[PlayerTarget] = None
    ):
        """Restores the player's health fully or by an amount.

        Parameters
        ----------
        amount : Optional[:attr:`~.Numeric`], optional
            Amount to heal. Default is ``None``.

        .. note::

            1 health = 0.5 hearts


        target : Optional[:class:`~.PlayerTarget`], optional
            The target of this :class:`~.PlayerAction`, or None for the current :class:`Player` instance's target.
            Defaults to ``None``.

        Returns
        -------
        :class:`PlayerAction`
            The generated PlayerAction instance.

        Examples
        --------
        ::

            p_default.heal(amount)
            # OR
            Player(PlayerTarget.DEFAULT).heal(amount)  # TODO: Example
        """
        args = Arguments([
            p_check(amount, typing.Optional[Numeric], "amount") if amount is not None else None
        ])
        return PlayerAction(
            action=PlayerActionType.HEAL,
            args=args,
            target=self._digest_target(target),
            append_to_reader=True
        )

    def hide_disguise(self, *, target: typing.Optional[PlayerTarget] = None):
        """Hides the player's disguise on their screen.

        .. rank:: Overlord


        Parameters
        ----------
        target : Optional[:class:`~.PlayerTarget`], optional
            The target of this :class:`~.PlayerAction`, or None for the current :class:`Player` instance's target.
            Defaults to ``None``.

        Returns
        -------
        :class:`PlayerAction`
            The generated PlayerAction instance.

        Examples
        --------
        ::

            p_default.hide_disguise()
            # OR
            Player(PlayerTarget.DEFAULT).hide_disguise()
        """
        return PlayerAction(
            action=PlayerActionType.HIDE_DISGUISE,
            args=Arguments(),
            target=self._digest_target(target),
            append_to_reader=True
        )

    def keep_inv(self, *, target: typing.Optional[PlayerTarget] = None):
        """When this code block is executed, the player will keep the contents of their inventory when they die.

        Parameters
        ----------
        target : Optional[:class:`~.PlayerTarget`], optional
            The target of this :class:`~.PlayerAction`, or None for the current :class:`Player` instance's target.
            Defaults to ``None``.

        Returns
        -------
        :class:`PlayerAction`
            The generated PlayerAction instance.

        Examples
        --------
        ::

            p_default.keep_inv()
            # OR
            Player(PlayerTarget.DEFAULT).keep_inv()
        """
        return PlayerAction(
            action=PlayerActionType.KEEP_INV,
            args=Arguments(),
            target=self._digest_target(target),
            append_to_reader=True
        )

    def kick(self, *, target: typing.Optional[PlayerTarget] = None):
        """Kicks the player from the plot.

        .. rank:: Noble


        Parameters
        ----------
        target : Optional[:class:`~.PlayerTarget`], optional
            The target of this :class:`~.PlayerAction`, or None for the current :class:`Player` instance's target.
            Defaults to ``None``.

        Returns
        -------
        :class:`PlayerAction`
            The generated PlayerAction instance.

        Examples
        --------
        ::

            p_default.kick()
            # OR
            Player(PlayerTarget.DEFAULT).kick()
        """
        return PlayerAction(
            action=PlayerActionType.KICK,
            args=Arguments(),
            target=self._digest_target(target),
            append_to_reader=True
        )

    def launch_fwd(
            self, power: Numeric,
            *, launch_axis="Pitch and Yaw",
            target: typing.Optional[PlayerTarget] = None
    ):
        """Launches the player a certain amount forward or backward.

        Parameters
        ----------
        power : :attr:`~.Numeric`
            Launch power.

        launch_axis :
            Pitch and Yaw, Yaw Only

        target : Optional[:class:`~.PlayerTarget`], optional
            The target of this :class:`~.PlayerAction`, or None for the current :class:`Player` instance's target.
            Defaults to ``None``.

        Returns
        -------
        :class:`PlayerAction`
            The generated PlayerAction instance.

        Notes
        -----
        A positive launch power is forward, and a negative one is backward.


        Examples
        --------
        ::

            p_default.launch_fwd(power)
            # OR
            Player(PlayerTarget.DEFAULT).launch_fwd(power)  # TODO: Example
        """
        args = Arguments([
            p_check(power, Numeric, "power")
        ], tags=[
            Tag(
                "Launch Axis", option=launch_axis,  # default is Pitch and Yaw
                action=PlayerActionType.LAUNCH_FWD, block=BlockType.IF_GAME
            )
        ])
        return PlayerAction(
            action=PlayerActionType.LAUNCH_FWD,
            args=args,
            target=self._digest_target(target),
            append_to_reader=True
        )

    def launch_proj(
            self, projectile: BlockParam, loc: typing.Optional[Locatable] = None,
            name: typing.Optional[Textable] = None, speed: typing.Optional[Numeric] = None,
            inaccuracy: typing.Optional[Numeric] = None, particle: typing.Optional[ParticleParam] = None,
            *, target: typing.Optional[PlayerTarget] = None
    ):
        """Launches a projectile from the player.

        Parameters
        ----------
        projectile : Union[:class:`Material`, :attr:`~.ItemParam`, :attr:`~.Textable`]
            The type of Projectile to launch.

            The type can be specified either as:

            - an instance of :class:`~.Material` (the material of the block to set);
            - an item (:attr:`~.ItemParam` - the item representing the block to set);
            - text (:attr:`~.Textable` - the material of the block to set as text).

        loc : Optional[:attr:`~.Locatable`], optional
            Launch point. Default is ``None``.

        name : Optional[:attr:`~.Textable`], optional
            Projectile name. Default is ``None``.

        speed : Optional[:attr:`~.Numeric`], optional
            Speed. Default is ``None``.

        inaccuracy : Optional[:attr:`~.Numeric`], optional
            Inaccuracy (default = 1). Default is ``None``.

        particle : Optional[:attr:`~.ParticleParam`], optional
            Launch trail. Default is ``None``.

        target : Optional[:class:`~.PlayerTarget`], optional
            The target of this :class:`~.PlayerAction`, or None for the current :class:`Player` instance's target.
            Defaults to ``None``.

        Returns
        -------
        :class:`PlayerAction`
            The generated PlayerAction instance.

        Notes
        -----
        Inaccuracy controls how much random momentum is applied on launch.


        Examples
        --------
        ::

            p_default.launch_proj(projectile, loc, name, speed, inaccuracy, particle)
            # OR
            Player(PlayerTarget.DEFAULT).launch_proj(projectile, loc, name, speed, inaccuracy, particle)  # TODO: Example
        """
        args = Arguments([
            p_check(projectile, typing.Union[ItemParam, Textable], "projectile"),
            p_check(loc, typing.Optional[Locatable], "loc") if loc is not None else None,
            p_check(name, typing.Optional[Textable], "name") if name is not None else None,
            p_check(speed, typing.Optional[Numeric], "speed") if speed is not None else None,
            p_check(inaccuracy, typing.Optional[Numeric], "inaccuracy") if inaccuracy is not None else None,
            p_check(particle, typing.Optional[ParticleParam], "particle") if particle is not None else None
        ])
        return PlayerAction(
            action=PlayerActionType.LAUNCH_PROJ,
            args=args,
            target=self._digest_target(target),
            append_to_reader=True
        )

    def launch_toward(
            self, loc: Locatable, power: typing.Optional[Numeric] = None,
            *, ignore_distance: bool = False,
            target: typing.Optional[PlayerTarget] = None
    ):
        """Launches the player toward a certain location.

        Parameters
        ----------
        loc : :attr:`~.Locatable`
            Launch destination.

        power : Optional[:attr:`~.Numeric`], optional
            Launch power. Default is ``None``.

        ignore_distance : :class:`bool`, optional
            Defaults to ``False``.

        target : Optional[:class:`~.PlayerTarget`], optional
            The target of this :class:`~.PlayerAction`, or None for the current :class:`Player` instance's target.
            Defaults to ``None``.

        Returns
        -------
        :class:`PlayerAction`
            The generated PlayerAction instance.

        Notes
        -----
        A negative launch power will launch the player away from the location.


        Examples
        --------
        ::

            p_default.launch_toward(loc, power)
            # OR
            Player(PlayerTarget.DEFAULT).launch_toward(loc, power)  # TODO: Example
        """
        args = Arguments([
            p_check(loc, Locatable, "loc"),
            p_check(power, typing.Optional[Numeric], "power") if power is not None else None
        ], tags=[
            Tag(
                "Ignore Distance", option=bool(ignore_distance),  # default is False
                action=PlayerActionType.LAUNCH_TOWARD, block=BlockType.IF_GAME
            )
        ])
        return PlayerAction(
            action=PlayerActionType.LAUNCH_TOWARD,
            args=args,
            target=self._digest_target(target),
            append_to_reader=True
        )

    def launch_up(
            self, power: Numeric,
            *, target: typing.Optional[PlayerTarget] = None
    ):
        """Launches the player a certain amount up or down. A positive amount is up, and a negative amount is down.

        Parameters
        ----------
        power : :attr:`~.Numeric`
            Launch power.

        target : Optional[:class:`~.PlayerTarget`], optional
            The target of this :class:`~.PlayerAction`, or None for the current :class:`Player` instance's target.
            Defaults to ``None``.

        Returns
        -------
        :class:`PlayerAction`
            The generated PlayerAction instance.

        Examples
        --------
        ::

            p_default.launch_up(power)
            # OR
            Player(PlayerTarget.DEFAULT).launch_up(power)  # TODO: Example
        """
        args = Arguments([
            p_check(power, Numeric, "power")
        ])
        return PlayerAction(
            action=PlayerActionType.LAUNCH_UP,
            args=args,
            target=self._digest_target(target),
            append_to_reader=True
        )

    def lightning_effect(
            self, loc: Locatable,
            *, target: typing.Optional[PlayerTarget] = None
    ):
        """Plays a thunderbolt effect to the player that is silent and deals no damage.

        Parameters
        ----------
        loc : :attr:`~.Locatable`
            Strike location.

        target : Optional[:class:`~.PlayerTarget`], optional
            The target of this :class:`~.PlayerAction`, or None for the current :class:`Player` instance's target.
            Defaults to ``None``.

        Returns
        -------
        :class:`PlayerAction`
            The generated PlayerAction instance.

        Examples
        --------
        ::

            p_default.lightning_effect(loc)
            # OR
            Player(PlayerTarget.DEFAULT).lightning_effect(loc)  # TODO: Example
        """
        args = Arguments([
            p_check(loc, Locatable, "loc")
        ])
        return PlayerAction(
            action=PlayerActionType.LIGHTNING_EFFECT,
            args=args,
            target=self._digest_target(target),
            append_to_reader=True
        )

    def load_inv(self, *, target: typing.Optional[PlayerTarget] = None):
        """Loads the selected saved inventory.

        .. rank:: Noble


        Parameters
        ----------
        target : Optional[:class:`~.PlayerTarget`], optional
            The target of this :class:`~.PlayerAction`, or None for the current :class:`Player` instance's target.
            Defaults to ``None``.

        Returns
        -------
        :class:`PlayerAction`
            The generated PlayerAction instance.

        Notes
        -----
        - If no saved inventory exists, the player's inventory will be cleared.
        - Inventories loaded with 'Load Saved Inventory' take several ticks to load. Use 'Control: Wait' if you need to check the inventory's contents after it is loaded.


        Examples
        --------
        ::

            p_default.load_inv()
            # OR
            Player(PlayerTarget.DEFAULT).load_inv()
        """
        return PlayerAction(
            action=PlayerActionType.LOAD_INV,
            args=Arguments(),
            target=self._digest_target(target),
            append_to_reader=True
        )

    def mob_disguise(
            self, spawn_egg: SpawnEggable, name: typing.Optional[Textable] = None,
            *, target: typing.Optional[PlayerTarget] = None
    ):
        """Disguises the player as a mob.

        .. rank:: Overlord


        Parameters
        ----------
        spawn_egg : :attr:`~.SpawnEggable`
            Mob disguise.

        name : Optional[:attr:`~.Textable`], optional
            Disguise name. Default is ``None``.

        target : Optional[:class:`~.PlayerTarget`], optional
            The target of this :class:`~.PlayerAction`, or None for the current :class:`Player` instance's target.
            Defaults to ``None``.

        Returns
        -------
        :class:`PlayerAction`
            The generated PlayerAction instance.

        Examples
        --------
        ::

            p_default.mob_disguise(spawn_egg, name)
            # OR
            Player(PlayerTarget.DEFAULT).mob_disguise(spawn_egg, name)  # TODO: Example
        """
        args = Arguments([
            p_check(spawn_egg, SpawnEggable, "spawn_egg"),
            p_check(name, typing.Optional[Textable], "name") if name is not None else None
        ])
        return PlayerAction(
            action=PlayerActionType.MOB_DISGUISE,
            args=args,
            target=self._digest_target(target),
            append_to_reader=True
        )

    def nat_regen(self, *, target: typing.Optional[PlayerTarget] = None):
        """Allows the player's health to regenerate naturally.

        Parameters
        ----------
        target : Optional[:class:`~.PlayerTarget`], optional
            The target of this :class:`~.PlayerAction`, or None for the current :class:`Player` instance's target.
            Defaults to ``None``.

        Returns
        -------
        :class:`PlayerAction`
            The generated PlayerAction instance.

        Examples
        --------
        ::

            p_default.nat_regen()
            # OR
            Player(PlayerTarget.DEFAULT).nat_regen()
        """
        return PlayerAction(
            action=PlayerActionType.NAT_REGEN,
            args=Arguments(),
            target=self._digest_target(target),
            append_to_reader=True
        )

    def no_death_drops(self, *, target: typing.Optional[PlayerTarget] = None):
        """When this code block is executed, the player will no longer drop the contents of their inventory when they die.

        Parameters
        ----------
        target : Optional[:class:`~.PlayerTarget`], optional
            The target of this :class:`~.PlayerAction`, or None for the current :class:`Player` instance's target.
            Defaults to ``None``.

        Returns
        -------
        :class:`PlayerAction`
            The generated PlayerAction instance.

        Examples
        --------
        ::

            p_default.no_death_drops()
            # OR
            Player(PlayerTarget.DEFAULT).no_death_drops()
        """
        return PlayerAction(
            action=PlayerActionType.NO_DEATH_DROPS,
            args=Arguments(),
            target=self._digest_target(target),
            append_to_reader=True
        )

    def no_keep_inv(self, *, target: typing.Optional[PlayerTarget] = None):
        """When this code block is executed, the player will no longer keep the contents of their inventory when they die.

        Parameters
        ----------
        target : Optional[:class:`~.PlayerTarget`], optional
            The target of this :class:`~.PlayerAction`, or None for the current :class:`Player` instance's target.
            Defaults to ``None``.

        Returns
        -------
        :class:`PlayerAction`
            The generated PlayerAction instance.

        Examples
        --------
        ::

            p_default.no_keep_inv()
            # OR
            Player(PlayerTarget.DEFAULT).no_keep_inv()
        """
        return PlayerAction(
            action=PlayerActionType.NO_KEEP_INV,
            args=Arguments(),
            target=self._digest_target(target),
            append_to_reader=True
        )

    def no_nat_regen(self, *, target: typing.Optional[PlayerTarget] = None):
        """Prevents the player's health from regenerating naturally.

        Parameters
        ----------
        target : Optional[:class:`~.PlayerTarget`], optional
            The target of this :class:`~.PlayerAction`, or None for the current :class:`Player` instance's target.
            Defaults to ``None``.

        Returns
        -------
        :class:`PlayerAction`
            The generated PlayerAction instance.

        Examples
        --------
        ::

            p_default.no_nat_regen()
            # OR
            Player(PlayerTarget.DEFAULT).no_nat_regen()
        """
        return PlayerAction(
            action=PlayerActionType.NO_NAT_REGEN,
            args=Arguments(),
            target=self._digest_target(target),
            append_to_reader=True
        )

    def no_proj_coll(self, *, target: typing.Optional[PlayerTarget] = None):
        """Prevents projectiles from hitting the player.

        Parameters
        ----------
        target : Optional[:class:`~.PlayerTarget`], optional
            The target of this :class:`~.PlayerAction`, or None for the current :class:`Player` instance's target.
            Defaults to ``None``.

        Returns
        -------
        :class:`PlayerAction`
            The generated PlayerAction instance.

        Examples
        --------
        ::

            p_default.no_proj_coll()
            # OR
            Player(PlayerTarget.DEFAULT).no_proj_coll()
        """
        return PlayerAction(
            action=PlayerActionType.NO_PROJ_COLL,
            args=Arguments(),
            target=self._digest_target(target),
            append_to_reader=True
        )

    def open_block_inv(
            self, loc: Locatable,
            *, target: typing.Optional[PlayerTarget] = None
    ):
        """Opens a container inventory. Also works with crafting tables.

        .. rank:: Emperor


        Parameters
        ----------
        loc : :attr:`~.Locatable`
            Block to access.

        target : Optional[:class:`~.PlayerTarget`], optional
            The target of this :class:`~.PlayerAction`, or None for the current :class:`Player` instance's target.
            Defaults to ``None``.

        Returns
        -------
        :class:`PlayerAction`
            The generated PlayerAction instance.

        Examples
        --------
        ::

            p_default.open_block_inv(loc)
            # OR
            Player(PlayerTarget.DEFAULT).open_block_inv(loc)  # TODO: Example
        """
        args = Arguments([
            p_check(loc, Locatable, "loc")
        ])
        return PlayerAction(
            action=PlayerActionType.OPEN_BLOCK_INV,
            args=args,
            target=self._digest_target(target),
            append_to_reader=True
        )

    def open_book(
            self, item: ItemParam,
            *, target: typing.Optional[PlayerTarget] = None
    ):
        """Opens a written book menu.

        .. rank:: Emperor


        Parameters
        ----------
        item : :attr:`~.ItemParam`
            Book item.

        target : Optional[:class:`~.PlayerTarget`], optional
            The target of this :class:`~.PlayerAction`, or None for the current :class:`Player` instance's target.
            Defaults to ``None``.

        Returns
        -------
        :class:`PlayerAction`
            The generated PlayerAction instance.

        Notes
        -----
        Opened book and quills cannot be edited.


        Examples
        --------
        ::

            p_default.open_book(item)
            # OR
            Player(PlayerTarget.DEFAULT).open_book(item)  # TODO: Example
        """
        args = Arguments([
            p_check(item, ItemParam, "item")
        ])
        return PlayerAction(
            action=PlayerActionType.OPEN_BOOK,
            args=args,
            target=self._digest_target(target),
            append_to_reader=True
        )

    def particle_effect(
            self, particle: ParticleParam, loc: Locatable, num: typing.Optional[Numeric] = None,
            *, target: typing.Optional[PlayerTarget] = None
    ):
        """Plays one or more of the particle to the player.

        Parameters
        ----------
        particle : :attr:`~.ParticleParam`
            Particle effect.

        loc : :attr:`~.Locatable`
            Particle location.

        num : Optional[:attr:`~.Numeric`], optional
            Particle count. Default is ``None``.

        target : Optional[:class:`~.PlayerTarget`], optional
            The target of this :class:`~.PlayerAction`, or None for the current :class:`Player` instance's target.
            Defaults to ``None``.

        Returns
        -------
        :class:`PlayerAction`
            The generated PlayerAction instance.

        Examples
        --------
        ::

            p_default.particle_effect(particle, loc, num)
            # OR
            Player(PlayerTarget.DEFAULT).particle_effect(particle, loc, num)  # TODO: Example
        """
        args = Arguments([
            p_check(particle, ParticleParam, "particle"),
            p_check(loc, Locatable, "loc"),
            p_check(num, typing.Optional[Numeric], "num") if num is not None else None
        ])
        return PlayerAction(
            action=PlayerActionType.PARTICLE_EFFECT,
            args=args,
            target=self._digest_target(target),
            append_to_reader=True
        )

    def perform_command(
            self, text: Textable,
            *, target: typing.Optional[PlayerTarget] = None
    ):
        """Makes the player execute a plot command.

        .. rank:: Emperor


        Parameters
        ----------
        text : :attr:`~.Textable`
            Plot command.

        target : Optional[:class:`~.PlayerTarget`], optional
            The target of this :class:`~.PlayerAction`, or None for the current :class:`Player` instance's target.
            Defaults to ``None``.

        Returns
        -------
        :class:`PlayerAction`
            The generated PlayerAction instance.

        Examples
        --------
        ::

            p_default.perform_command(text)
            # OR
            Player(PlayerTarget.DEFAULT).perform_command(text)  # TODO: Example
        """
        args = Arguments([
            p_check(text, Textable, "text")
        ])
        return PlayerAction(
            action=PlayerActionType.PERFORM_COMMAND,
            args=args,
            target=self._digest_target(target),
            append_to_reader=True
        )

    def play_sound(
            self, *sounds: typing.Union[SoundParam, Listable], loc: typing.Optional[Locatable] = None,
            target: typing.Optional[PlayerTarget] = None
    ):
        """Plays a sound effect for the player.

        Parameters
        ----------
        sounds : Union[:attr:`~.SoundParam`, :attr:`~.Listable`]
            Sound to play.

        loc : Optional[:attr:`~.Locatable`], optional
            Playback location. Default is ``None``.

        target : Optional[:class:`~.PlayerTarget`], optional
            The target of this :class:`~.PlayerAction`, or None for the current :class:`Player` instance's target.
            Defaults to ``None``.

        Returns
        -------
        :class:`PlayerAction`
            The generated PlayerAction instance.

        Examples
        --------
        ::

            p_default.play_sound(sounds, loc)
            # OR
            Player(PlayerTarget.DEFAULT).play_sound(sounds, loc)  # TODO: Example
        """
        args = Arguments([
            *[p_check(sound, typing.Union[SoundParam, Listable], f"sounds[{i}]") for i, sound in enumerate(sounds)],
            p_check(loc, typing.Optional[Locatable], "loc") if loc is not None else None
        ])
        return PlayerAction(
            action=PlayerActionType.PLAY_SOUND,
            args=args,
            target=self._digest_target(target),
            append_to_reader=True
        )

    def play_sound_seq(
            self, *sounds: typing.Union[SoundParam, Listable], delay: typing.Optional[Numeric] = None,
            loc: typing.Optional[Locatable] = None,
            target: typing.Optional[PlayerTarget] = None
    ):
        """Plays a sequence of sounds for the player, with a delay after each sound.

        Parameters
        ----------
        sounds : Union[:attr:`~.SoundParam`, :attr:`~.Listable`]
            Sounds to play.

        delay : Optional[:attr:`~.Numeric`], optional
            Sound delay (ticks, default = 60). Default is ``None``.

        loc : Optional[:attr:`~.Locatable`], optional
            Playback location. Default is ``None``.

        target : Optional[:class:`~.PlayerTarget`], optional
            The target of this :class:`~.PlayerAction`, or None for the current :class:`Player` instance's target.
            Defaults to ``None``.

        Returns
        -------
        :class:`PlayerAction`
            The generated PlayerAction instance.

        Examples
        --------
        ::

            p_default.play_sound_seq(sounds, delay, loc)
            # OR
            Player(PlayerTarget.DEFAULT).play_sound_seq(sounds, delay, loc)  # TODO: Example
        """
        args = Arguments([
            *[p_check(sound, typing.Union[SoundParam, Listable], f"sounds[{i}]") for i, sound in enumerate(sounds)],
            p_check(delay, typing.Optional[Numeric], "delay") if delay is not None else None,
            p_check(loc, typing.Optional[Locatable], "loc") if loc is not None else None
        ])
        return PlayerAction(
            action=PlayerActionType.PLAY_SOUND_SEQ,
            args=args,
            target=self._digest_target(target),
            append_to_reader=True
        )

    def player_disguise(
            self, name: Textable, text_2: typing.Optional[Textable] = None,
            *, target: typing.Optional[PlayerTarget] = None
    ):
        """Disguises the player as another player.

        .. rank:: Overlord


        Parameters
        ----------
        name : :attr:`~.Textable`
            Disguise player name.

        text_2 : Optional[:attr:`~.Textable`], optional
            Disguise skin. Default is ``None``.

        target : Optional[:class:`~.PlayerTarget`], optional
            The target of this :class:`~.PlayerAction`, or None for the current :class:`Player` instance's target.
            Defaults to ``None``.

        Returns
        -------
        :class:`PlayerAction`
            The generated PlayerAction instance.

        Examples
        --------
        ::

            p_default.player_disguise(name, text_2)
            # OR
            Player(PlayerTarget.DEFAULT).player_disguise(name, text_2)  # TODO: Example
        """
        args = Arguments([
            p_check(name, Textable, "name"),
            p_check(text_2, typing.Optional[Textable], "text_2") if text_2 is not None else None
        ])
        return PlayerAction(
            action=PlayerActionType.PLAYER_DISGUISE,
            args=args,
            target=self._digest_target(target),
            append_to_reader=True
        )

    def proj_coll(self, *, target: typing.Optional[PlayerTarget] = None):
        """Allows projectiles to hit the player.

        Parameters
        ----------
        target : Optional[:class:`~.PlayerTarget`], optional
            The target of this :class:`~.PlayerAction`, or None for the current :class:`Player` instance's target.
            Defaults to ``None``.

        Returns
        -------
        :class:`PlayerAction`
            The generated PlayerAction instance.

        Examples
        --------
        ::

            p_default.proj_coll()
            # OR
            Player(PlayerTarget.DEFAULT).proj_coll()
        """
        return PlayerAction(
            action=PlayerActionType.PROJ_COLL,
            args=Arguments(),
            target=self._digest_target(target),
            append_to_reader=True
        )

    def remove_boss_bar(
            self,
            *, bar_slot="All Bossbars",
            target: typing.Optional[PlayerTarget] = None
    ):
        """Removes the given boss bar from the player if there is one.

        .. rank:: Mythic


        Parameters
        ----------
        bar_slot :
            All Bossbars, 1, 2, 3, 4

        target : Optional[:class:`~.PlayerTarget`], optional
            The target of this :class:`~.PlayerAction`, or None for the current :class:`Player` instance's target.
            Defaults to ``None``.

        Returns
        -------
        :class:`PlayerAction`
            The generated PlayerAction instance.

        Examples
        --------
        ::

            p_default.remove_boss_bar()
            # OR
            Player(PlayerTarget.DEFAULT).remove_boss_bar()  # TODO: Example
        """
        args = Arguments([], tags=[
            Tag(
                "Bar Slot", option=bar_slot,  # default is All Bossbars
                action=PlayerActionType.REMOVE_BOSS_BAR, block=BlockType.IF_GAME
            )
        ])
        return PlayerAction(
            action=PlayerActionType.REMOVE_BOSS_BAR,
            args=args,
            target=self._digest_target(target),
            append_to_reader=True
        )

    def remove_effect(
            self, *potions: typing.Union[Potionable, Listable],
            target: typing.Optional[PlayerTarget] = None
    ):
        """Removes 1 or more potion effects from the player.

        Parameters
        ----------
        potions : Union[:attr:`~.Potionable`, :attr:`~.Listable`]
            Potion effects.

        target : Optional[:class:`~.PlayerTarget`], optional
            The target of this :class:`~.PlayerAction`, or None for the current :class:`Player` instance's target.
            Defaults to ``None``.

        Returns
        -------
        :class:`PlayerAction`
            The generated PlayerAction instance.

        Notes
        -----
        Amplifiers and durations do not have to be the same as the initial potion effect(s).


        Examples
        --------
        ::

            p_default.remove_effect(potions)
            # OR
            Player(PlayerTarget.DEFAULT).remove_effect(potions)  # TODO: Example
        """
        args = Arguments([
            p_check(potion, typing.Union[Potionable, Listable], f"potions[{i}]") for i, potion in enumerate(potions)
        ])
        return PlayerAction(
            action=PlayerActionType.REMOVE_EFFECT,
            args=args,
            target=self._digest_target(target),
            append_to_reader=True
        )

    def remove_inv_row(
            self, num: typing.Optional[Numeric] = None,
            *, row_to_remove="Bottom Row",
            target: typing.Optional[PlayerTarget] = None
    ):
        """Removes the given number of rows from the bottom of the currently open inventory.

        .. rank:: Emperor


        Parameters
        ----------
        num : Optional[:attr:`~.Numeric`], optional
            Rows to remove. Default is ``None``.

        row_to_remove :
            Top Row, Bottom Row

        target : Optional[:class:`~.PlayerTarget`], optional
            The target of this :class:`~.PlayerAction`, or None for the current :class:`Player` instance's target.
            Defaults to ``None``.

        Returns
        -------
        :class:`PlayerAction`
            The generated PlayerAction instance.

        Examples
        --------
        ::

            p_default.remove_inv_row(num)
            # OR
            Player(PlayerTarget.DEFAULT).remove_inv_row(num)  # TODO: Example
        """
        args = Arguments([
            p_check(num, typing.Optional[Numeric], "num") if num is not None else None
        ], tags=[
            Tag(
                "Row to Remove", option=row_to_remove,  # default is Bottom Row
                action=PlayerActionType.REMOVE_INV_ROW, block=BlockType.IF_GAME
            )
        ])
        return PlayerAction(
            action=PlayerActionType.REMOVE_INV_ROW,
            args=args,
            target=self._digest_target(target),
            append_to_reader=True
        )

    def remove_item(
            self, *items: typing.Union[ItemParam, ItemCollection, typing.Iterable[ItemParam], Listable],
            target: typing.Optional[PlayerTarget] = None
    ):
        """Removes certain items from the player.

        Parameters
        ----------
        items : Optional[Union[:class:`~.ItemParam`, :class:`~.ItemCollection`, Iterable[:class:`~.ItemParam`], :attr:`Listable`]]
            Item(s) to remove. The items can be specified either as:

            - ``None`` for an empty slot;
            - :class:`~.Item` for one item;
            - :attr:`~.Listable` for a variable list of items;
            - :class:`~.ItemCollection` or Iterable[:class:`~.Item`] for a predetermined list of items.

        target : Optional[:class:`~.PlayerTarget`], optional
            The target of this :class:`~.PlayerAction`, or None for the current :class:`Player` instance's target.
            Defaults to ``None``.

        Returns
        -------
        :class:`PlayerAction`
            The generated PlayerAction instance.

        Examples
        --------
        ::

            p_default.remove_item(items)
            # OR
            Player(PlayerTarget.DEFAULT).remove_item(items)  # TODO: Example
        """
        item_list = flatten(*items, except_iterables=[str], max_depth=1)

        args = Arguments([
            p_check(item, typing.Union[ItemParam, Listable], "items") for item in item_list
        ])
        return PlayerAction(
            action=PlayerActionType.REMOVE_ITEM,
            args=args,
            target=self._digest_target(target),
            append_to_reader=True
        )

    def replace_item(
            self,
            *items_1: typing.Optional[typing.Union[ItemParam, ItemCollection, typing.Iterable[ItemParam], Listable]],
            item_2: ItemParam, amount: typing.Optional[Numeric] = None,
            target: typing.Optional[PlayerTarget] = None
    ):
        """Replaces the specified items with the given item in the player's inventory.

        Parameters
        ----------
        items_1 : Optional[Optional[Union[:class:`~.ItemParam`, :class:`~.ItemCollection`, Iterable[:class:`~.ItemParam`], :attr:`Listable`]]], optional
            Item(s) to replace. The items can be specified either as:

            - ``None`` for an empty slot;
            - :class:`~.Item` for one item;
            - :attr:`~.Listable` for a variable list of items;
            - :class:`~.ItemCollection` or Iterable[:class:`~.Item`] for a predetermined list of items.

        item_2 : :attr:`~.ItemParam`
            Item to replace with.

        amount : Optional[:attr:`~.Numeric`], optional
            Amount of items to replace. Default is ``None``.

        target : Optional[:class:`~.PlayerTarget`], optional
            The target of this :class:`~.PlayerAction`, or None for the current :class:`Player` instance's target.
            Defaults to ``None``.

        Returns
        -------
        :class:`PlayerAction`
            The generated PlayerAction instance.

        Examples
        --------
        ::

            p_default.replace_item(items_1, item_2, amount)
            # OR
            Player(PlayerTarget.DEFAULT).replace_item(items_1, item_2, amount)  # TODO: Example
        """
        item_list = flatten(*items_1, except_iterables=[str], max_depth=1)

        args = Arguments([
            *[p_check(obj, typing.Union[ItemParam, Listable], "items_1") for obj in item_list],
            p_check(item_2, ItemParam, "item_2"),
            p_check(amount, typing.Optional[Numeric], "amount") if amount is not None else None
        ])
        return PlayerAction(
            action=PlayerActionType.REPLACE_ITEM,
            args=args,
            target=self._digest_target(target),
            append_to_reader=True
        )

    def replace_proj(
            self, projectile: typing.Optional[BlockParam] = None, name: typing.Optional[Textable] = None,
            particle: typing.Optional[ParticleParam] = None,
            *, target: typing.Optional[PlayerTarget] = None
    ):
        """Replaces the projectile fired in the Shoot Bow Event.
        .. workswith:: Player Shoot Bow Event

        Parameters
        ----------
        projectile : Optional[Union[:class:`Material`, :attr:`~.ItemParam`, :attr:`~.Textable`]], optional
            The type of Projectile to launch.

            The type can be specified either as:

            - an instance of :class:`~.Material` (the material of the block to set);
            - an item (:attr:`~.ItemParam` - the item representing the block to set);
            - text (:attr:`~.Textable` - the material of the block to set as text).

        name : Optional[:attr:`~.Textable`], optional
            Projectile name. Default is ``None``.

        particle : Optional[:attr:`~.ParticleParam`], optional
            Launch trail. Default is ``None``.

        target : Optional[:class:`~.PlayerTarget`], optional
            The target of this :class:`~.PlayerAction`, or None for the current :class:`Player` instance's target.
            Defaults to ``None``.

        Returns
        -------
        :class:`PlayerAction`
            The generated PlayerAction instance.

        Examples
        --------
        ::

            p_default.replace_proj(projectile, name, particle)
            # OR
            Player(PlayerTarget.DEFAULT).replace_proj(projectile, name, particle)  # TODO: Example
        """
        args = Arguments([
            p_check(projectile, typing.Union[ItemParam, Textable], "projectile") if projectile is not None else None,
            p_check(name, typing.Optional[Textable], "name") if name is not None else None,
            p_check(particle, typing.Optional[ParticleParam], "particle") if particle is not None else None
        ])
        return PlayerAction(
            action=PlayerActionType.REPLACE_PROJ,
            args=args,
            target=self._digest_target(target),
            append_to_reader=True
        )

    def respawn(self, *, target: typing.Optional[PlayerTarget] = None):
        """Respawns the player if they are dead.

        .. rank:: Mythic


        Parameters
        ----------
        target : Optional[:class:`~.PlayerTarget`], optional
            The target of this :class:`~.PlayerAction`, or None for the current :class:`Player` instance's target.
            Defaults to ``None``.

        Returns
        -------
        :class:`PlayerAction`
            The generated PlayerAction instance.

        Examples
        --------
        ::

            p_default.respawn()
            # OR
            Player(PlayerTarget.DEFAULT).respawn()
        """
        return PlayerAction(
            action=PlayerActionType.RESPAWN,
            args=Arguments(),
            target=self._digest_target(target),
            append_to_reader=True
        )

    def ride_entity(
            self, name: Textable,
            *, target: typing.Optional[PlayerTarget] = None
    ):
        """Mounts the player on top of another player or entity.

        .. rank:: Noble


        Parameters
        ----------
        name : :attr:`~.Textable`
            Name of player or entity to ride.

        target : Optional[:class:`~.PlayerTarget`], optional
            The target of this :class:`~.PlayerAction`, or None for the current :class:`Player` instance's target.
            Defaults to ``None``.

        Returns
        -------
        :class:`PlayerAction`
            The generated PlayerAction instance.

        Notes
        -----
        Player names will be prioritized before mob names.


        Examples
        --------
        ::

            p_default.ride_entity(name)
            # OR
            Player(PlayerTarget.DEFAULT).ride_entity(name)  # TODO: Example
        """
        args = Arguments([
            p_check(name, Textable, "name")
        ])
        return PlayerAction(
            action=PlayerActionType.RIDE_ENTITY,
            args=args,
            target=self._digest_target(target),
            append_to_reader=True
        )

    def rm_arrows(self, *, target: typing.Optional[PlayerTarget] = None):
        """Clears any arrows stuck  in the player's body.

        Parameters
        ----------
        target : Optional[:class:`~.PlayerTarget`], optional
            The target of this :class:`~.PlayerAction`, or None for the current :class:`Player` instance's target.
            Defaults to ``None``.

        Returns
        -------
        :class:`PlayerAction`
            The generated PlayerAction instance.

        Examples
        --------
        ::

            p_default.rm_arrows()
            # OR
            Player(PlayerTarget.DEFAULT).rm_arrows()
        """
        return PlayerAction(
            action=PlayerActionType.RM_ARROWS,
            args=Arguments(),
            target=self._digest_target(target),
            append_to_reader=True
        )

    def rm_world_border(self, *, target: typing.Optional[PlayerTarget] = None):
        """Removes the world border for this player.

        .. rank:: Emperor


        Parameters
        ----------
        target : Optional[:class:`~.PlayerTarget`], optional
            The target of this :class:`~.PlayerAction`, or None for the current :class:`Player` instance's target.
            Defaults to ``None``.

        Returns
        -------
        :class:`PlayerAction`
            The generated PlayerAction instance.

        Examples
        --------
        ::

            p_default.rm_world_border()
            # OR
            Player(PlayerTarget.DEFAULT).rm_world_border()
        """
        return PlayerAction(
            action=PlayerActionType.RM_WORLD_BORDER,
            args=Arguments(),
            target=self._digest_target(target),
            append_to_reader=True
        )

    def rng_teleport(
            self, *locs: typing.Union[Locatable, Listable],
            keep_current_rotation: bool = False,
            target: typing.Optional[PlayerTarget] = None
    ):
        """Teleports the player to a random location in the chest.

        .. rank:: Noble


        Parameters
        ----------
        locs : Union[:attr:`~.Locatable`, :attr:`~.Listable`]
            Locations to choose from.

        keep_current_rotation : :class:`bool`, optional
            Defaults to ``False``.

        target : Optional[:class:`~.PlayerTarget`], optional
            The target of this :class:`~.PlayerAction`, or None for the current :class:`Player` instance's target.
            Defaults to ``None``.

        Returns
        -------
        :class:`PlayerAction`
            The generated PlayerAction instance.

        Notes
        -----
        Will pick a different location for each targeted player.


        Examples
        --------
        ::

            p_default.rng_teleport(locs)
            # OR
            Player(PlayerTarget.DEFAULT).rng_teleport(locs)  # TODO: Example
        """
        args = Arguments([
            p_check(loc, typing.Union[Locatable, Listable], f"locs[{i}]") for i, loc in enumerate(locs)
        ], tags=[
            Tag(
                "Keep Current Rotation", option=bool(keep_current_rotation),  # default is False
                action=PlayerActionType.RNG_TELEPORT, block=BlockType.IF_GAME
            )
        ])
        return PlayerAction(
            action=PlayerActionType.RNG_TELEPORT,
            args=args,
            target=self._digest_target(target),
            append_to_reader=True
        )

    def rollback_blocks(
            self, num: typing.Optional[Numeric] = None,
            *, target: typing.Optional[PlayerTarget] = None
    ):
        """Undoes the interactions with blocks by the player.

        .. rank:: Overlord


        Parameters
        ----------
        num : Optional[:attr:`~.Numeric`], optional
            Rollback time. Default is ``None``.

        target : Optional[:class:`~.PlayerTarget`], optional
            The target of this :class:`~.PlayerAction`, or None for the current :class:`Player` instance's target.
            Defaults to ``None``.

        Returns
        -------
        :class:`PlayerAction`
            The generated PlayerAction instance.

        Notes
        -----
        - The rollback time argument specifies how far back in time block changes should be reverted.
        - Please note that the rollback time argument is in SECONDS!


        Examples
        --------
        ::

            p_default.rollback_blocks(num)
            # OR
            Player(PlayerTarget.DEFAULT).rollback_blocks(num)  # TODO: Example
        """
        args = Arguments([
            p_check(num, typing.Optional[Numeric], "num") if num is not None else None
        ])
        return PlayerAction(
            action=PlayerActionType.ROLLBACK_BLOCKS,
            args=args,
            target=self._digest_target(target),
            append_to_reader=True
        )

    def save_inv(self, *, target: typing.Optional[PlayerTarget] = None):
        """Saves the selected player's current inventory. It can be loaded later with 'Load Saved Inventory'.

        .. rank:: Noble


        Parameters
        ----------
        target : Optional[:class:`~.PlayerTarget`], optional
            The target of this :class:`~.PlayerAction`, or None for the current :class:`Player` instance's target.
            Defaults to ``None``.

        Returns
        -------
        :class:`PlayerAction`
            The generated PlayerAction instance.

        Examples
        --------
        ::

            p_default.save_inv()
            # OR
            Player(PlayerTarget.DEFAULT).save_inv()
        """
        return PlayerAction(
            action=PlayerActionType.SAVE_INV,
            args=Arguments(),
            target=self._digest_target(target),
            append_to_reader=True
        )

    def send_advancement(
            self, text: Textable, item: typing.Optional[ItemParam] = None,
            *, toast_type="Advancement",
            target: typing.Optional[PlayerTarget] = None
    ):
        """Sends an advancement popup to the player.

        .. rank:: Mythic


        Parameters
        ----------
        text : :attr:`~.Textable`
            Advancement text.

        item : Optional[:attr:`~.ItemParam`], optional
            Popup icon. Default is ``None``.

        toast_type :
            Advancement, Goal, Challenge

        target : Optional[:class:`~.PlayerTarget`], optional
            The target of this :class:`~.PlayerAction`, or None for the current :class:`Player` instance's target.
            Defaults to ``None``.

        Returns
        -------
        :class:`PlayerAction`
            The generated PlayerAction instance.

        Examples
        --------
        ::

            p_default.send_advancement(text, item)
            # OR
            Player(PlayerTarget.DEFAULT).send_advancement(text, item)  # TODO: Example
        """
        args = Arguments([
            p_check(text, Textable, "text"),
            p_check(item, typing.Optional[ItemParam], "item") if item is not None else None
        ], tags=[
            Tag(
                "Toast Type", option=toast_type,  # default is Advancement
                action=PlayerActionType.SEND_ADVANCEMENT, block=BlockType.IF_GAME
            )
        ])
        return PlayerAction(
            action=PlayerActionType.SEND_ADVANCEMENT,
            args=args,
            target=self._digest_target(target),
            append_to_reader=True
        )

    def send_animation(
            self,
            *, animation_type="Swing Right Arm",
            target: typing.Optional[PlayerTarget] = None
    ):
        """Makes the player perform an animation.

        Parameters
        ----------
        animation_type :
            Swing Right Arm, Swing Left Arm, Hurt Animation, Crit Particles, Enchanted Hit Particles, Wake Up

        target : Optional[:class:`~.PlayerTarget`], optional
            The target of this :class:`~.PlayerAction`, or None for the current :class:`Player` instance's target.
            Defaults to ``None``.

        Returns
        -------
        :class:`PlayerAction`
            The generated PlayerAction instance.

        Examples
        --------
        ::

            p_default.send_animation()
            # OR
            Player(PlayerTarget.DEFAULT).send_animation()  # TODO: Example
        """
        args = Arguments([], tags=[
            Tag(
                "Animation Type", option=animation_type,  # default is Swing Right Arm
                action=PlayerActionType.SEND_ANIMATION, block=BlockType.IF_GAME
            )
        ])
        return PlayerAction(
            action=PlayerActionType.SEND_ANIMATION,
            args=args,
            target=self._digest_target(target),
            append_to_reader=True
        )

    def send_block(
            self, block_type: BlockParam, loc_1: Locatable, loc_2: typing.Optional[Locatable] = None,
            *metadatas: typing.Optional[typing.Union[BlockMetadata, Listable]],
            target: typing.Optional[PlayerTarget] = None
    ):
        """Makes client side, player specific blocks appear at the given location or area.

        .. rank:: Noble


        Parameters
        ----------
        block_type : Union[:class:`Material`, :attr:`~.ItemParam`, :attr:`~.Textable`]
            The type of Block to send.

            The type can be specified either as:

            - an instance of :class:`~.Material` (the material of the block to set);
            - an item (:attr:`~.ItemParam` - the item representing the block to set);
            - text (:attr:`~.Textable` - the material of the block to set as text).

        loc_1 : :attr:`~.Locatable`
            Location.

        loc_2 : Optional[:attr:`~.Locatable`], optional
            Location 2 (region). Default is ``None``.

        metadatas : Optional[Union[:class:`dict`, List[:attr:`~.Textable`], :attr:`~.Listable`]], optional
            Optionally, the metadata of the block to be set (``None`` for none). If not ``None``, can be in two forms:

            1. **As a dictionary:** If this is specified, then:
                - The keys must be strings;
                - The values can be one of:
                    - :class:`str` (the written out option);
                    - :class:`int` (is converted into a string accordingly);
                    - :class:`bool` (is turned into "true"/"false" accordingly);
                    - ``None`` (is turned into "none");
                    - :class:`~.DFVariable` / :class:`~.TextVar` (are turned into "%var(name)" accordingly).
                    - Any other types not mentioned will simply be ``str()``\ ed.
                - Example::

                    {
                        "facing": "east",
                        "drag": True,
                        "west": None,
                        "rotation": 8,
                        "powered": DFVariable("my_var")
                    }

            2. **As a list/iterable:** If this is specified, then it must be a list of valid Textable parameters, whose values DF expects to be formatted in one of the following ways:
                - ``"tag=value"``
                - ``"tag:value"``
                - ``"tag,value"``


            3. **As a** :attr:`~.Listable`\ **:** One can also specify a variable representing a List (in DF) of text values in the format specified in `2`.

        .. note::

            Example: "rotation:9,waterlogged:true"


        target : Optional[:class:`~.PlayerTarget`], optional
            The target of this :class:`~.PlayerAction`, or None for the current :class:`Player` instance's target.
            Defaults to ``None``.

        Returns
        -------
        :class:`PlayerAction`
            The generated PlayerAction instance.

        Notes
        -----
        - Also known as ghost blocks.
        - Can send up to 25 blocks per action.
        - Locations that are outside the plot can be used.


        Examples
        --------
        ::

            p_default.send_block(block_type, loc_1, loc_2, metadatas)
            # OR
            Player(PlayerTarget.DEFAULT).send_block(block_type, loc_1, loc_2, metadatas)  # TODO: Example
        """
        args = Arguments([
            p_check(block_type, typing.Union[ItemParam, Textable], "block_type"),
            p_check(loc_1, Locatable, "loc_1"),
            p_check(loc_2, typing.Optional[Locatable], "loc_2") if loc_2 is not None else None,
            *[p_check(metadata, Textable, f"metadatas[{i}]") for i, metadata in enumerate(metadatas)]
        ])
        return PlayerAction(
            action=PlayerActionType.SEND_BLOCK,
            args=args,
            target=self._digest_target(target),
            append_to_reader=True
        )

    def send_dialogue(
            self, *texts: typing.Union[Textable, Listable], delay: typing.Optional[Numeric] = None,
            target: typing.Optional[PlayerTarget] = None
    ):
        """Sends a series of messages in chat to the player, with a delay after each message.

        .. rank:: Noble


        Parameters
        ----------
        texts : Union[:attr:`~.Textable`, :attr:`~.Listable`]
            Messages to send.

        delay : Optional[:attr:`~.Numeric`], optional
            Message delay ticks. Default is ``None``.

        .. note::

            Default = 60


        target : Optional[:class:`~.PlayerTarget`], optional
            The target of this :class:`~.PlayerAction`, or None for the current :class:`Player` instance's target.
            Defaults to ``None``.

        Returns
        -------
        :class:`PlayerAction`
            The generated PlayerAction instance.

        Examples
        --------
        ::

            p_default.send_dialogue(texts, delay)
            # OR
            Player(PlayerTarget.DEFAULT).send_dialogue(texts, delay)  # TODO: Example
        """
        args = Arguments([
            *[p_check(text, typing.Union[Textable, Listable], f"texts[{i}]") for i, text in enumerate(texts)],
            p_check(delay, typing.Optional[Numeric], "delay") if delay is not None else None
        ])
        return PlayerAction(
            action=PlayerActionType.SEND_DIALOGUE,
            args=args,
            target=self._digest_target(target),
            append_to_reader=True
        )

    def send_hover(
            self, text_1: Textable, text_2: Textable,
            *, target: typing.Optional[PlayerTarget] = None
    ):
        """Sends a message to the player When the player 'hovers' over it with their cursor, a second message appears.

        .. rank:: Mythic


        Parameters
        ----------
        text_1 : :attr:`~.Textable`
            Message to send in chat.

        text_2 : :attr:`~.Textable`
            Message to see on hover.

        target : Optional[:class:`~.PlayerTarget`], optional
            The target of this :class:`~.PlayerAction`, or None for the current :class:`Player` instance's target.
            Defaults to ``None``.

        Returns
        -------
        :class:`PlayerAction`
            The generated PlayerAction instance.

        Examples
        --------
        ::

            p_default.send_hover(text_1, text_2)
            # OR
            Player(PlayerTarget.DEFAULT).send_hover(text_1, text_2)  # TODO: Example
        """
        args = Arguments([
            p_check(text_1, Textable, "text_1"),
            p_check(text_2, Textable, "text_2")
        ])
        return PlayerAction(
            action=PlayerActionType.SEND_HOVER,
            args=args,
            target=self._digest_target(target),
            append_to_reader=True
        )

    def send_message(
            self, *texts: typing.Optional[typing.Union[Textable, Listable]],
            alignment_mode="Regular", text_value_merging="Add Spaces",
            target: typing.Optional[PlayerTarget] = None
    ):
        """Sends a chat message to the player.

        Parameters
        ----------
        texts : Optional[Union[:attr:`~.Textable`, :attr:`~.Listable`]], optional
            Message to send. Default is ``None``.

        alignment_mode :
            Regular, Centered

        text_value_merging :
            Add Spaces, No Spaces

        target : Optional[:class:`~.PlayerTarget`], optional
            The target of this :class:`~.PlayerAction`, or None for the current :class:`Player` instance's target.
            Defaults to ``None``.

        Returns
        -------
        :class:`PlayerAction`
            The generated PlayerAction instance.

        Notes
        -----
        - Multiple text items will be merged into one message, with spaces in between each item.
        - Numbers and locations in the chest will be converted to text.


        Examples
        --------
        ::

            p_default.send_message(texts)
            # OR
            Player(PlayerTarget.DEFAULT).send_message(texts)  # TODO: Example
        """
        args = Arguments([
            p_check(text, typing.Optional[typing.Union[Textable, Listable]], f"texts[{i}]") for i, text in
            enumerate(texts)
        ], tags=[
            Tag(
                "Alignment Mode", option=alignment_mode,  # default is Regular
                action=PlayerActionType.SEND_MESSAGE, block=BlockType.IF_GAME
            ),
            Tag(
                "Text Value Merging", option=text_value_merging,  # default is Add Spaces
                action=PlayerActionType.SEND_MESSAGE, block=BlockType.IF_GAME
            )
        ])
        return PlayerAction(
            action=PlayerActionType.SEND_MESSAGE,
            args=args,
            target=self._digest_target(target),
            append_to_reader=True
        )

    def send_title(
            self, text_1: Textable, text_2: typing.Optional[Textable] = None, duration: typing.Optional[Numeric] = None,
            duration: typing.Optional[Numeric] = None, duration: typing.Optional[Numeric] = None,
            *, target: typing.Optional[PlayerTarget] = None
    ):
        """Sends a title message to the player.

        .. rank:: Emperor


        Parameters
        ----------
        text_1 : :attr:`~.Textable`
            Title text.

        text_2 : Optional[:attr:`~.Textable`], optional
            Subtitle text. Default is ``None``.

        duration : Optional[:attr:`~.Numeric`], optional
            Title duration (ticks, default = 60). Default is ``None``.

        duration : Optional[:attr:`~.Numeric`], optional
            Start fade duration (ticks, default = 20). Default is ``None``.

        duration : Optional[:attr:`~.Numeric`], optional
            End fade duration (ticks, default = 20). Default is ``None``.

        target : Optional[:class:`~.PlayerTarget`], optional
            The target of this :class:`~.PlayerAction`, or None for the current :class:`Player` instance's target.
            Defaults to ``None``.

        Returns
        -------
        :class:`PlayerAction`
            The generated PlayerAction instance.

        Examples
        --------
        ::

            p_default.send_title(text_1, text_2, duration, duration, duration)
            # OR
            Player(PlayerTarget.DEFAULT).send_title(text_1, text_2, duration, duration, duration)  # TODO: Example
        """
        args = Arguments([
            p_check(text_1, Textable, "text_1"),
            p_check(text_2, typing.Optional[Textable], "text_2") if text_2 is not None else None,
            p_check(duration, typing.Optional[Numeric], "duration") if duration is not None else None,
            p_check(duration, typing.Optional[Numeric], "duration") if duration is not None else None,
            p_check(duration, typing.Optional[Numeric], "duration") if duration is not None else None
        ])
        return PlayerAction(
            action=PlayerActionType.SEND_TITLE,
            args=args,
            target=self._digest_target(target),
            append_to_reader=True
        )

    def set_air_ticks(
            self, ticks: Numeric,
            *, target: typing.Optional[PlayerTarget] = None
    ):
        """Sets the player's remaining breath ticks.

        Parameters
        ----------
        ticks : :attr:`~.Numeric`
            Breath ticks.

        target : Optional[:class:`~.PlayerTarget`], optional
            The target of this :class:`~.PlayerAction`, or None for the current :class:`Player` instance's target.
            Defaults to ``None``.

        Returns
        -------
        :class:`PlayerAction`
            The generated PlayerAction instance.

        Notes
        -----
        Each bubble is 30 air ticks.


        Examples
        --------
        ::

            p_default.set_air_ticks(ticks)
            # OR
            Player(PlayerTarget.DEFAULT).set_air_ticks(ticks)  # TODO: Example
        """
        args = Arguments([
            p_check(ticks, Numeric, "ticks")
        ])
        return PlayerAction(
            action=PlayerActionType.SET_AIR_TICKS,
            args=args,
            target=self._digest_target(target),
            append_to_reader=True
        )

    def set_armor(
            self, *items: typing.Union[ItemParam, ItemCollection, typing.Iterable[ItemParam], Listable],
            target: typing.Optional[PlayerTarget] = None
    ):
        """Sets the armor of the player. Place the armor in slots 1-4 of the chest, with 1 being the helmet and 4 being the boots.

        Parameters
        ----------
        items : Optional[Union[:class:`~.ItemParam`, :class:`~.ItemCollection`, Iterable[:class:`~.ItemParam`], :attr:`Listable`]]
            Armor to set. The items can be specified either as:

            - ``None`` for an empty slot;
            - :class:`~.Item` for one item;
            - :attr:`~.Listable` for a variable list of items;
            - :class:`~.ItemCollection` or Iterable[:class:`~.Item`] for a predetermined list of items.

        target : Optional[:class:`~.PlayerTarget`], optional
            The target of this :class:`~.PlayerAction`, or None for the current :class:`Player` instance's target.
            Defaults to ``None``.

        Returns
        -------
        :class:`PlayerAction`
            The generated PlayerAction instance.

        Notes
        -----
        Any block or item can render on the player's head if placed in the 'helmet' slot.


        Examples
        --------
        ::

            p_default.set_armor(items)
            # OR
            Player(PlayerTarget.DEFAULT).set_armor(items)  # TODO: Example
        """
        item_list = flatten(*items, except_iterables=[str], max_depth=1)

        args = Arguments([
            p_check(item, typing.Union[ItemParam, Listable], "items") for item in item_list
        ])
        return PlayerAction(
            action=PlayerActionType.SET_ARMOR,
            args=args,
            target=self._digest_target(target),
            append_to_reader=True
        )

    def set_atk_speed(
            self, speed: Numeric,
            *, target: typing.Optional[PlayerTarget] = None
    ):
        """Sets the player's attack speed.

        .. rank:: Mythic


        Parameters
        ----------
        speed : :attr:`~.Numeric`
            Attack speed.

        target : Optional[:class:`~.PlayerTarget`], optional
            The target of this :class:`~.PlayerAction`, or None for the current :class:`Player` instance's target.
            Defaults to ``None``.

        Returns
        -------
        :class:`PlayerAction`
            The generated PlayerAction instance.

        Notes
        -----
        - The player's attack speed is equal to the number of times they can attack per second.
        - The default attack speed is 4.


        Examples
        --------
        ::

            p_default.set_atk_speed(speed)
            # OR
            Player(PlayerTarget.DEFAULT).set_atk_speed(speed)  # TODO: Example
        """
        args = Arguments([
            p_check(speed, Numeric, "speed")
        ])
        return PlayerAction(
            action=PlayerActionType.SET_ATK_SPEED,
            args=args,
            target=self._digest_target(target),
            append_to_reader=True
        )

    def set_boss_bar(
            self, text: Textable, num_1: typing.Optional[Numeric] = None, num_2: typing.Optional[Numeric] = None,
            *, bar_color="Pink", bar_style="Solid", sky_effect="None", bar_slot="1",
            target: typing.Optional[PlayerTarget] = None
    ):
        """Sets the player's boss bar.

        .. rank:: Mythic


        Parameters
        ----------
        text : :attr:`~.Textable`
            Bossbar title.

        num_1 : Optional[:attr:`~.Numeric`], optional
            Progress. Default is ``None``.

        num_2 : Optional[:attr:`~.Numeric`], optional
            Max (default = 100). Default is ``None``.

        bar_color :
            Pink, Blue, Red, Green, Yellow, Purple, White

        bar_style :
            Solid, Segmented 6, Segmented 10, Segmented 12, Segmented 20

        sky_effect :
            None, Fog, Dark Sky, Fog and Dark Sky

        bar_slot :
            1, 2, 3, 4

        target : Optional[:class:`~.PlayerTarget`], optional
            The target of this :class:`~.PlayerAction`, or None for the current :class:`Player` instance's target.
            Defaults to ``None``.

        Returns
        -------
        :class:`PlayerAction`
            The generated PlayerAction instance.

        Examples
        --------
        ::

            p_default.set_boss_bar(text, num_1, num_2)
            # OR
            Player(PlayerTarget.DEFAULT).set_boss_bar(text, num_1, num_2)  # TODO: Example
        """
        args = Arguments([
            p_check(text, Textable, "text"),
            p_check(num_1, typing.Optional[Numeric], "num_1") if num_1 is not None else None,
            p_check(num_2, typing.Optional[Numeric], "num_2") if num_2 is not None else None
        ], tags=[
            Tag(
                "Bar Color", option=bar_color,  # default is Pink
                action=PlayerActionType.SET_BOSS_BAR, block=BlockType.IF_GAME
            ),
            Tag(
                "Bar Style", option=bar_style,  # default is Solid
                action=PlayerActionType.SET_BOSS_BAR, block=BlockType.IF_GAME
            ),
            Tag(
                "Sky Effect", option=sky_effect,  # default is None
                action=PlayerActionType.SET_BOSS_BAR, block=BlockType.IF_GAME
            ),
            Tag(
                "Bar Slot", option=bar_slot,  # default is 1
                action=PlayerActionType.SET_BOSS_BAR, block=BlockType.IF_GAME
            )
        ])
        return PlayerAction(
            action=PlayerActionType.SET_BOSS_BAR,
            args=args,
            target=self._digest_target(target),
            append_to_reader=True
        )

    def set_chat_tag(
            self, *texts: typing.Optional[typing.Union[Textable, Listable]],
            target: typing.Optional[PlayerTarget] = None
    ):
        """Sets the chat tag for the player.

        .. rank:: Mythic


        Parameters
        ----------
        texts : Optional[Union[:attr:`~.Textable`, :attr:`~.Listable`]], optional
            New chat tag. Default is ``None``.

        target : Optional[:class:`~.PlayerTarget`], optional
            The target of this :class:`~.PlayerAction`, or None for the current :class:`Player` instance's target.
            Defaults to ``None``.

        Returns
        -------
        :class:`PlayerAction`
            The generated PlayerAction instance.

        Notes
        -----
        - Multiple text items will be merged into one chat tag.
        - Leave empty to reset the chat tag.


        Examples
        --------
        ::

            p_default.set_chat_tag(texts)
            # OR
            Player(PlayerTarget.DEFAULT).set_chat_tag(texts)  # TODO: Example
        """
        args = Arguments([
            p_check(text, typing.Optional[typing.Union[Textable, Listable]], f"texts[{i}]") for i, text in
            enumerate(texts)
        ])
        return PlayerAction(
            action=PlayerActionType.SET_CHAT_TAG,
            args=args,
            target=self._digest_target(target),
            append_to_reader=True
        )

    def set_compass(
            self, loc: Locatable,
            *, target: typing.Optional[PlayerTarget] = None
    ):
        """Sets the location compasses point to for the player.

        Parameters
        ----------
        loc : :attr:`~.Locatable`
            New Target.

        target : Optional[:class:`~.PlayerTarget`], optional
            The target of this :class:`~.PlayerAction`, or None for the current :class:`Player` instance's target.
            Defaults to ``None``.

        Returns
        -------
        :class:`PlayerAction`
            The generated PlayerAction instance.

        Examples
        --------
        ::

            p_default.set_compass(loc)
            # OR
            Player(PlayerTarget.DEFAULT).set_compass(loc)  # TODO: Example
        """
        args = Arguments([
            p_check(loc, Locatable, "loc")
        ])
        return PlayerAction(
            action=PlayerActionType.SET_COMPASS,
            args=args,
            target=self._digest_target(target),
            append_to_reader=True
        )

    def set_cursor_item(
            self, item: typing.Optional[ItemParam] = None,
            *, target: typing.Optional[PlayerTarget] = None
    ):
        """Sets the item on the player's cursor.

        Parameters
        ----------
        item : Optional[:attr:`~.ItemParam`], optional
            Item to set. Default is ``None``.

        target : Optional[:class:`~.PlayerTarget`], optional
            The target of this :class:`~.PlayerAction`, or None for the current :class:`Player` instance's target.
            Defaults to ``None``.

        Returns
        -------
        :class:`PlayerAction`
            The generated PlayerAction instance.

        Examples
        --------
        ::

            p_default.set_cursor_item(item)
            # OR
            Player(PlayerTarget.DEFAULT).set_cursor_item(item)  # TODO: Example
        """
        args = Arguments([
            p_check(item, typing.Optional[ItemParam], "item") if item is not None else None
        ])
        return PlayerAction(
            action=PlayerActionType.SET_CURSOR_ITEM,
            args=args,
            target=self._digest_target(target),
            append_to_reader=True
        )

    def set_fall_distance(
            self, distance: Numeric,
            *, target: typing.Optional[PlayerTarget] = None
    ):
        """Sets the player's fall distance, affecting fall damage upon landing.

        Parameters
        ----------
        distance : :attr:`~.Numeric`
            Fall distance (blocks).

        target : Optional[:class:`~.PlayerTarget`], optional
            The target of this :class:`~.PlayerAction`, or None for the current :class:`Player` instance's target.
            Defaults to ``None``.

        Returns
        -------
        :class:`PlayerAction`
            The generated PlayerAction instance.

        Examples
        --------
        ::

            p_default.set_fall_distance(distance)
            # OR
            Player(PlayerTarget.DEFAULT).set_fall_distance(distance)  # TODO: Example
        """
        args = Arguments([
            p_check(distance, Numeric, "distance")
        ])
        return PlayerAction(
            action=PlayerActionType.SET_FALL_DISTANCE,
            args=args,
            target=self._digest_target(target),
            append_to_reader=True
        )

    def set_fire_ticks(
            self, duration: Numeric,
            *, target: typing.Optional[PlayerTarget] = None
    ):
        """Sets the player on fire for a certain number of ticks.

        Parameters
        ----------
        duration : :attr:`~.Numeric`
            Duration (ticks).

        target : Optional[:class:`~.PlayerTarget`], optional
            The target of this :class:`~.PlayerAction`, or None for the current :class:`Player` instance's target.
            Defaults to ``None``.

        Returns
        -------
        :class:`PlayerAction`
            The generated PlayerAction instance.

        Notes
        -----
        Using 'Set On Fire' with a duration of 0 extinguishes the player.


        Examples
        --------
        ::

            p_default.set_fire_ticks(duration)
            # OR
            Player(PlayerTarget.DEFAULT).set_fire_ticks(duration)  # TODO: Example
        """
        args = Arguments([
            p_check(duration, Numeric, "duration")
        ])
        return PlayerAction(
            action=PlayerActionType.SET_FIRE_TICKS,
            args=args,
            target=self._digest_target(target),
            append_to_reader=True
        )

    def set_food_level(
            self, level: Numeric,
            *, target: typing.Optional[PlayerTarget] = None
    ):
        """Sets the player's food level.

        Parameters
        ----------
        level : :attr:`~.Numeric`
            New hunger level (1-20).

        target : Optional[:class:`~.PlayerTarget`], optional
            The target of this :class:`~.PlayerAction`, or None for the current :class:`Player` instance's target.
            Defaults to ``None``.

        Returns
        -------
        :class:`PlayerAction`
            The generated PlayerAction instance.

        Examples
        --------
        ::

            p_default.set_food_level(level)
            # OR
            Player(PlayerTarget.DEFAULT).set_food_level(level)  # TODO: Example
        """
        args = Arguments([
            p_check(level, Numeric, "level")
        ])
        return PlayerAction(
            action=PlayerActionType.SET_FOOD_LEVEL,
            args=args,
            target=self._digest_target(target),
            append_to_reader=True
        )

    def set_hand_item(
            self, item: typing.Optional[ItemParam] = None,
            *, hand_slot="Main Hand",
            target: typing.Optional[PlayerTarget] = None
    ):
        """Sets the item in the player's main hand or off hand.

        Parameters
        ----------
        item : Optional[:attr:`~.ItemParam`], optional
            Item to set. Default is ``None``.

        hand_slot :
            Main Hand, Off Hand

        target : Optional[:class:`~.PlayerTarget`], optional
            The target of this :class:`~.PlayerAction`, or None for the current :class:`Player` instance's target.
            Defaults to ``None``.

        Returns
        -------
        :class:`PlayerAction`
            The generated PlayerAction instance.

        Examples
        --------
        ::

            p_default.set_hand_item(item)
            # OR
            Player(PlayerTarget.DEFAULT).set_hand_item(item)  # TODO: Example
        """
        args = Arguments([
            p_check(item, typing.Optional[ItemParam], "item") if item is not None else None
        ], tags=[
            Tag(
                "Hand Slot", option=hand_slot,  # default is Main Hand
                action=PlayerActionType.SET_HAND_ITEM, block=BlockType.IF_GAME
            )
        ])
        return PlayerAction(
            action=PlayerActionType.SET_HAND_ITEM,
            args=args,
            target=self._digest_target(target),
            append_to_reader=True
        )

    def set_health(
            self, health: Numeric,
            *, heal_type="Regular Health",
            target: typing.Optional[PlayerTarget] = None
    ):
        """Sets the player's health or absorption hearts.

        Parameters
        ----------
        health : :attr:`~.Numeric`
            New health.

        .. note::

            1 health = 0.5 hearts


        heal_type :
            Regular Health, Absorption Health, Combined Health

        target : Optional[:class:`~.PlayerTarget`], optional
            The target of this :class:`~.PlayerAction`, or None for the current :class:`Player` instance's target.
            Defaults to ``None``.

        Returns
        -------
        :class:`PlayerAction`
            The generated PlayerAction instance.

        Examples
        --------
        ::

            p_default.set_health(health)
            # OR
            Player(PlayerTarget.DEFAULT).set_health(health)  # TODO: Example
        """
        args = Arguments([
            p_check(health, Numeric, "health")
        ], tags=[
            Tag(
                "Heal Type", option=heal_type,  # default is Regular Health
                action=PlayerActionType.SET_HEALTH, block=BlockType.IF_GAME
            )
        ])
        return PlayerAction(
            action=PlayerActionType.SET_HEALTH,
            args=args,
            target=self._digest_target(target),
            append_to_reader=True
        )

    def set_inv_name(
            self, name: Textable,
            *, target: typing.Optional[PlayerTarget] = None
    ):
        """Renames the player's currently open plot inventory.

        .. rank:: Emperor


        Parameters
        ----------
        name : :attr:`~.Textable`
            Inventory name.

        target : Optional[:class:`~.PlayerTarget`], optional
            The target of this :class:`~.PlayerAction`, or None for the current :class:`Player` instance's target.
            Defaults to ``None``.

        Returns
        -------
        :class:`PlayerAction`
            The generated PlayerAction instance.

        Examples
        --------
        ::

            p_default.set_inv_name(name)
            # OR
            Player(PlayerTarget.DEFAULT).set_inv_name(name)  # TODO: Example
        """
        args = Arguments([
            p_check(name, Textable, "name")
        ])
        return PlayerAction(
            action=PlayerActionType.SET_INV_NAME,
            args=args,
            target=self._digest_target(target),
            append_to_reader=True
        )

    def set_item_cooldown(
            self, item: ItemParam, ticks: Numeric, sound: typing.Optional[SoundParam] = None,
            *, target: typing.Optional[PlayerTarget] = None
    ):
        """Applies a cooldown visual effect to an item type.

        Parameters
        ----------
        item : :attr:`~.ItemParam`
            Item type to affect.

        ticks : :attr:`~.Numeric`
            Cooldown in ticks.

        sound : Optional[:attr:`~.SoundParam`], optional
            Cooldown refresh sound. Default is ``None``.

        target : Optional[:class:`~.PlayerTarget`], optional
            The target of this :class:`~.PlayerAction`, or None for the current :class:`Player` instance's target.
            Defaults to ``None``.

        Returns
        -------
        :class:`PlayerAction`
            The generated PlayerAction instance.

        Notes
        -----
        The cooldown applies to all items of the given type.


        Examples
        --------
        ::

            p_default.set_item_cooldown(item, ticks, sound)
            # OR
            Player(PlayerTarget.DEFAULT).set_item_cooldown(item, ticks, sound)  # TODO: Example
        """
        args = Arguments([
            p_check(item, ItemParam, "item"),
            p_check(ticks, Numeric, "ticks"),
            p_check(sound, typing.Optional[SoundParam], "sound") if sound is not None else None
        ])
        return PlayerAction(
            action=PlayerActionType.SET_ITEM_COOLDOWN,
            args=args,
            target=self._digest_target(target),
            append_to_reader=True
        )

    def set_items(
            self, *items: typing.Union[ItemParam, ItemCollection, typing.Iterable[ItemParam], Listable],
            target: typing.Optional[PlayerTarget] = None
    ):
        """Changes the player's inventory accordingly to the items in the  parameter chest.

        Parameters
        ----------
        items : Optional[Union[:class:`~.ItemParam`, :class:`~.ItemCollection`, Iterable[:class:`~.ItemParam`], :attr:`Listable`]]
            Item(s) to give, in their corresponding item slots. The items can be specified either as:

            - ``None`` for an empty slot;
            - :class:`~.Item` for one item;
            - :attr:`~.Listable` for a variable list of items;
            - :class:`~.ItemCollection` or Iterable[:class:`~.Item`] for a predetermined list of items.

        .. note::

            The top chest row is the hotbar. The other rows fill the inventory from the top down.


        target : Optional[:class:`~.PlayerTarget`], optional
            The target of this :class:`~.PlayerAction`, or None for the current :class:`Player` instance's target.
            Defaults to ``None``.

        Returns
        -------
        :class:`PlayerAction`
            The generated PlayerAction instance.

        Examples
        --------
        ::

            p_default.set_items(items)
            # OR
            Player(PlayerTarget.DEFAULT).set_items(items)  # TODO: Example
        """
        item_list = flatten(*items, except_iterables=[str], max_depth=1)

        args = Arguments([
            p_check(item, typing.Union[ItemParam, Listable], "items") for item in item_list
        ])
        return PlayerAction(
            action=PlayerActionType.SET_ITEMS,
            args=args,
            target=self._digest_target(target),
            append_to_reader=True
        )

    def set_list_header(
            self, *texts: typing.Optional[typing.Union[Textable, Listable]],
            player_list_field="Header",
            target: typing.Optional[PlayerTarget] = None
    ):
        """Sets the player list header / footer for the player.

        .. rank:: Noble


        Parameters
        ----------
        texts : Optional[Union[:attr:`~.Textable`, :attr:`~.Listable`]], optional
            New header / footer. Default is ``None``.

        player_list_field :
            Header, Footer

        target : Optional[:class:`~.PlayerTarget`], optional
            The target of this :class:`~.PlayerAction`, or None for the current :class:`Player` instance's target.
            Defaults to ``None``.

        Returns
        -------
        :class:`PlayerAction`
            The generated PlayerAction instance.

        Notes
        -----
        Numbers and locations in the chest will be converted to text.


        Examples
        --------
        ::

            p_default.set_list_header(texts)
            # OR
            Player(PlayerTarget.DEFAULT).set_list_header(texts)  # TODO: Example
        """
        args = Arguments([
            p_check(text, typing.Optional[typing.Union[Textable, Listable]], f"texts[{i}]") for i, text in
            enumerate(texts)
        ], tags=[
            Tag(
                "Player List Field", option=player_list_field,  # default is Header
                action=PlayerActionType.SET_LIST_HEADER, block=BlockType.IF_GAME
            )
        ])
        return PlayerAction(
            action=PlayerActionType.SET_LIST_HEADER,
            args=args,
            target=self._digest_target(target),
            append_to_reader=True
        )

    def set_max_health(
            self, health: Numeric,
            *, heal_player_to_max_health: bool = False,
            target: typing.Optional[PlayerTarget] = None
    ):
        """Sets the maximum amount of health that the player can have.

        Parameters
        ----------
        health : :attr:`~.Numeric`
            New maximum health.

        heal_player_to_max_health : :class:`bool`, optional
            Defaults to ``False``.

        target : Optional[:class:`~.PlayerTarget`], optional
            The target of this :class:`~.PlayerAction`, or None for the current :class:`Player` instance's target.
            Defaults to ``None``.

        Returns
        -------
        :class:`PlayerAction`
            The generated PlayerAction instance.

        Examples
        --------
        ::

            p_default.set_max_health(health)
            # OR
            Player(PlayerTarget.DEFAULT).set_max_health(health)  # TODO: Example
        """
        args = Arguments([
            p_check(health, Numeric, "health")
        ], tags=[
            Tag(
                "Heal Player to Max Health", option=bool(heal_player_to_max_health),  # default is False
                action=PlayerActionType.SET_MAX_HEALTH, block=BlockType.IF_GAME
            )
        ])
        return PlayerAction(
            action=PlayerActionType.SET_MAX_HEALTH,
            args=args,
            target=self._digest_target(target),
            append_to_reader=True
        )

    def set_menu_item(
            self, *slots: typing.Union[Numeric, Listable],
            *items: typing.Optional[typing.Union[ItemParam, ItemCollection, typing.Iterable[ItemParam], Listable]],
            target: typing.Optional[PlayerTarget] = None
    ):
        """Sets the specified slot in the player's currently open inventory menu to the specified item.

        .. rank:: Emperor


        Parameters
        ----------
        slots : Union[:attr:`~.Numeric`, :attr:`~.Listable`]
            Slot(s) to set.

        items : Optional[Optional[Union[:class:`~.ItemParam`, :class:`~.ItemCollection`, Iterable[:class:`~.ItemParam`], :attr:`Listable`]]], optional
            Item(s) to display. The items can be specified either as:

            - ``None`` for an empty slot;
            - :class:`~.Item` for one item;
            - :attr:`~.Listable` for a variable list of items;
            - :class:`~.ItemCollection` or Iterable[:class:`~.Item`] for a predetermined list of items.

        target : Optional[:class:`~.PlayerTarget`], optional
            The target of this :class:`~.PlayerAction`, or None for the current :class:`Player` instance's target.
            Defaults to ``None``.

        Returns
        -------
        :class:`PlayerAction`
            The generated PlayerAction instance.

        Examples
        --------
        ::

            p_default.set_menu_item(slots, items)
            # OR
            Player(PlayerTarget.DEFAULT).set_menu_item(slots, items)  # TODO: Example
        """
        item_list = flatten(*items, except_iterables=[str], max_depth=1)

        args = Arguments([
            *[p_check(slot, typing.Union[Numeric, Listable], f"slots[{i}]") for i, slot in enumerate(slots)],
            *[p_check(item, typing.Union[ItemParam, Listable], "items") for item in item_list]
        ])
        return PlayerAction(
            action=PlayerActionType.SET_MENU_ITEM,
            args=args,
            target=self._digest_target(target),
            append_to_reader=True
        )

    def set_name_color(
            self, name: Textable,
            *, target: typing.Optional[PlayerTarget] = None
    ):
        """Sets the color the player's name tag appears in.

        .. rank:: Noble


        Parameters
        ----------
        name : :attr:`~.Textable`
            Name color.

        target : Optional[:class:`~.PlayerTarget`], optional
            The target of this :class:`~.PlayerAction`, or None for the current :class:`Player` instance's target.
            Defaults to ``None``.

        Returns
        -------
        :class:`PlayerAction`
            The generated PlayerAction instance.

        Notes
        -----
        Leave empty to reset the name color.


        Examples
        --------
        ::

            p_default.set_name_color(name)
            # OR
            Player(PlayerTarget.DEFAULT).set_name_color(name)  # TODO: Example
        """
        args = Arguments([
            p_check(name, Textable, "name")
        ])
        return PlayerAction(
            action=PlayerActionType.SET_NAME_COLOR,
            args=args,
            target=self._digest_target(target),
            append_to_reader=True
        )

    def set_saturation(
            self, level: Numeric,
            *, target: typing.Optional[PlayerTarget] = None
    ):
        """Sets the player's saturation level.

        Parameters
        ----------
        level : :attr:`~.Numeric`
            New saturation level (1-20).

        target : Optional[:class:`~.PlayerTarget`], optional
            The target of this :class:`~.PlayerAction`, or None for the current :class:`Player` instance's target.
            Defaults to ``None``.

        Returns
        -------
        :class:`PlayerAction`
            The generated PlayerAction instance.

        Examples
        --------
        ::

            p_default.set_saturation(level)
            # OR
            Player(PlayerTarget.DEFAULT).set_saturation(level)  # TODO: Example
        """
        args = Arguments([
            p_check(level, Numeric, "level")
        ])
        return PlayerAction(
            action=PlayerActionType.SET_SATURATION,
            args=args,
            target=self._digest_target(target),
            append_to_reader=True
        )

    def set_slot(
            self, slot: Numeric,
            *, target: typing.Optional[PlayerTarget] = None
    ):
        """Sets a player's selected hotbar slot.

        Parameters
        ----------
        slot : :attr:`~.Numeric`
            New slot.

        .. note::

            1 (left) to 9 (right)


        target : Optional[:class:`~.PlayerTarget`], optional
            The target of this :class:`~.PlayerAction`, or None for the current :class:`Player` instance's target.
            Defaults to ``None``.

        Returns
        -------
        :class:`PlayerAction`
            The generated PlayerAction instance.

        Examples
        --------
        ::

            p_default.set_slot(slot)
            # OR
            Player(PlayerTarget.DEFAULT).set_slot(slot)  # TODO: Example
        """
        args = Arguments([
            p_check(slot, Numeric, "slot")
        ])
        return PlayerAction(
            action=PlayerActionType.SET_SLOT,
            args=args,
            target=self._digest_target(target),
            append_to_reader=True
        )

    def set_slot_item(
            self, item: typing.Optional[ItemParam] = None, slot: Numeric,
            *, target: typing.Optional[PlayerTarget] = None
    ):
        """Like 'Give Items', but you can control which inventory slot the item goes in.

        Parameters
        ----------
        item : Optional[:attr:`~.ItemParam`], optional
            Item to set. Default is ``None``.

        slot : :attr:`~.Numeric`
            Slot to set.

        .. note::

            Slots 1-9 = Hotbar Slots 10-36 = Inventory (Top to bottom)


        target : Optional[:class:`~.PlayerTarget`], optional
            The target of this :class:`~.PlayerAction`, or None for the current :class:`Player` instance's target.
            Defaults to ``None``.

        Returns
        -------
        :class:`PlayerAction`
            The generated PlayerAction instance.

        Examples
        --------
        ::

            p_default.set_slot_item(item, slot)
            # OR
            Player(PlayerTarget.DEFAULT).set_slot_item(item, slot)  # TODO: Example
        """
        args = Arguments([
            p_check(item, typing.Optional[ItemParam], "item") if item is not None else None,
            p_check(slot, Numeric, "slot")
        ])
        return PlayerAction(
            action=PlayerActionType.SET_SLOT_ITEM,
            args=args,
            target=self._digest_target(target),
            append_to_reader=True
        )

    def set_time(
            self, ticks: Numeric,
            *, target: typing.Optional[PlayerTarget] = None
    ):
        """Sets the time of day for the player only.

        Parameters
        ----------
        ticks : :attr:`~.Numeric`
            Time of day (0-24,000 ticks).

        .. note::

            Morning: 1,000 Ticks Noon: 6,000 Ticks Afternoon: 7,700 Ticks Evening: 13,000 Ticks Midnight: 18,000 Ticks


        target : Optional[:class:`~.PlayerTarget`], optional
            The target of this :class:`~.PlayerAction`, or None for the current :class:`Player` instance's target.
            Defaults to ``None``.

        Returns
        -------
        :class:`PlayerAction`
            The generated PlayerAction instance.

        Examples
        --------
        ::

            p_default.set_time(ticks)
            # OR
            Player(PlayerTarget.DEFAULT).set_time(ticks)  # TODO: Example
        """
        args = Arguments([
            p_check(ticks, Numeric, "ticks")
        ])
        return PlayerAction(
            action=PlayerActionType.SET_TIME,
            args=args,
            target=self._digest_target(target),
            append_to_reader=True
        )

    def set_world_border(
            self, center: Locatable, radius: Numeric,
            *, target: typing.Optional[PlayerTarget] = None
    ):
        """Creates a world border visible to only the player.

        .. rank:: Emperor


        Parameters
        ----------
        center : :attr:`~.Locatable`
            Center position.

        radius : :attr:`~.Numeric`
            Radius in blocks.

        target : Optional[:class:`~.PlayerTarget`], optional
            The target of this :class:`~.PlayerAction`, or None for the current :class:`Player` instance's target.
            Defaults to ``None``.

        Returns
        -------
        :class:`PlayerAction`
            The generated PlayerAction instance.

        Examples
        --------
        ::

            p_default.set_world_border(center, radius)
            # OR
            Player(PlayerTarget.DEFAULT).set_world_border(center, radius)  # TODO: Example
        """
        args = Arguments([
            p_check(center, Locatable, "center"),
            p_check(radius, Numeric, "radius")
        ])
        return PlayerAction(
            action=PlayerActionType.SET_WORLD_BORDER,
            args=args,
            target=self._digest_target(target),
            append_to_reader=True
        )

    def set_xpl_vl(
            self, level: Numeric,
            *, target: typing.Optional[PlayerTarget] = None
    ):
        """Sets the player's experience level.

        Parameters
        ----------
        level : :attr:`~.Numeric`
            Experience level.

        target : Optional[:class:`~.PlayerTarget`], optional
            The target of this :class:`~.PlayerAction`, or None for the current :class:`Player` instance's target.
            Defaults to ``None``.

        Returns
        -------
        :class:`PlayerAction`
            The generated PlayerAction instance.

        Examples
        --------
        ::

            p_default.set_xpl_vl(level)
            # OR
            Player(PlayerTarget.DEFAULT).set_xpl_vl(level)  # TODO: Example
        """
        args = Arguments([
            p_check(level, Numeric, "level")
        ])
        return PlayerAction(
            action=PlayerActionType.SET_XPL_VL,
            args=args,
            target=self._digest_target(target),
            append_to_reader=True
        )

    def set_xpp_rog(
            self, num: Numeric,
            *, target: typing.Optional[PlayerTarget] = None
    ):
        """Sets the XP progress bar to a certain percentage.

        Parameters
        ----------
        num : :attr:`~.Numeric`
            Progress % (0-100).

        target : Optional[:class:`~.PlayerTarget`], optional
            The target of this :class:`~.PlayerAction`, or None for the current :class:`Player` instance's target.
            Defaults to ``None``.

        Returns
        -------
        :class:`PlayerAction`
            The generated PlayerAction instance.

        Examples
        --------
        ::

            p_default.set_xpp_rog(num)
            # OR
            Player(PlayerTarget.DEFAULT).set_xpp_rog(num)  # TODO: Example
        """
        args = Arguments([
            p_check(num, Numeric, "num")
        ])
        return PlayerAction(
            action=PlayerActionType.SET_XPP_ROG,
            args=args,
            target=self._digest_target(target),
            append_to_reader=True
        )

    def shift_world_border(
            self, radius: Numeric, num_2: typing.Optional[Numeric] = None,
            *, target: typing.Optional[PlayerTarget] = None
    ):
        """Changes the player's world border size, if they have one active.

        .. rank:: Emperor


        Parameters
        ----------
        radius : :attr:`~.Numeric`
            New radius.

        num_2 : Optional[:attr:`~.Numeric`], optional
            Blocks per second. Default is ``None``.

        target : Optional[:class:`~.PlayerTarget`], optional
            The target of this :class:`~.PlayerAction`, or None for the current :class:`Player` instance's target.
            Defaults to ``None``.

        Returns
        -------
        :class:`PlayerAction`
            The generated PlayerAction instance.

        Examples
        --------
        ::

            p_default.shift_world_border(radius, num_2)
            # OR
            Player(PlayerTarget.DEFAULT).shift_world_border(radius, num_2)  # TODO: Example
        """
        args = Arguments([
            p_check(radius, Numeric, "radius"),
            p_check(num_2, typing.Optional[Numeric], "num_2") if num_2 is not None else None
        ])
        return PlayerAction(
            action=PlayerActionType.SHIFT_WORLD_BORDER,
            args=args,
            target=self._digest_target(target),
            append_to_reader=True
        )

    def show_disguise(self, *, target: typing.Optional[PlayerTarget] = None):
        """Shows the player's disguise on their screen.

        .. rank:: Overlord


        Parameters
        ----------
        target : Optional[:class:`~.PlayerTarget`], optional
            The target of this :class:`~.PlayerAction`, or None for the current :class:`Player` instance's target.
            Defaults to ``None``.

        Returns
        -------
        :class:`PlayerAction`
            The generated PlayerAction instance.

        Examples
        --------
        ::

            p_default.show_disguise()
            # OR
            Player(PlayerTarget.DEFAULT).show_disguise()
        """
        return PlayerAction(
            action=PlayerActionType.SHOW_DISGUISE,
            args=Arguments(),
            target=self._digest_target(target),
            append_to_reader=True
        )

    def show_inv(
            self,
            *items: typing.Optional[typing.Union[ItemParam, ItemCollection, typing.Iterable[ItemParam], Listable]],
            target: typing.Optional[PlayerTarget] = None
    ):
        """Opens a custom item inventory for the player.

        .. rank:: Emperor


        Parameters
        ----------
        items : Optional[Optional[Union[:class:`~.ItemParam`, :class:`~.ItemCollection`, Iterable[:class:`~.ItemParam`], :attr:`Listable`]]], optional
            Items to display. The items can be specified either as:

            - ``None`` for an empty slot;
            - :class:`~.Item` for one item;
            - :attr:`~.Listable` for a variable list of items;
            - :class:`~.ItemCollection` or Iterable[:class:`~.Item`] for a predetermined list of items.

        target : Optional[:class:`~.PlayerTarget`], optional
            The target of this :class:`~.PlayerAction`, or None for the current :class:`Player` instance's target.
            Defaults to ``None``.

        Returns
        -------
        :class:`PlayerAction`
            The generated PlayerAction instance.

        Examples
        --------
        ::

            p_default.show_inv(items)
            # OR
            Player(PlayerTarget.DEFAULT).show_inv(items)  # TODO: Example
        """
        item_list = flatten(*items, except_iterables=[str], max_depth=1)

        args = Arguments([
            p_check(item, typing.Union[ItemParam, Listable], "items") for item in item_list
        ])
        return PlayerAction(
            action=PlayerActionType.SHOW_INV,
            args=args,
            target=self._digest_target(target),
            append_to_reader=True
        )

    def stop_sound(
            self, *sounds: typing.Optional[typing.Union[SoundParam, Listable]],
            target: typing.Optional[PlayerTarget] = None
    ):
        """Stops all, or specific sound effects for the player.

        Parameters
        ----------
        sounds : Optional[Union[:attr:`~.SoundParam`, :attr:`~.Listable`]], optional
            Sounds to stop. Default is ``None``.

        target : Optional[:class:`~.PlayerTarget`], optional
            The target of this :class:`~.PlayerAction`, or None for the current :class:`Player` instance's target.
            Defaults to ``None``.

        Returns
        -------
        :class:`PlayerAction`
            The generated PlayerAction instance.

        Examples
        --------
        ::

            p_default.stop_sound(sounds)
            # OR
            Player(PlayerTarget.DEFAULT).stop_sound(sounds)  # TODO: Example
        """
        args = Arguments([
            p_check(sound, typing.Optional[typing.Union[SoundParam, Listable]], f"sounds[{i}]") for i, sound in
            enumerate(sounds)
        ])
        return PlayerAction(
            action=PlayerActionType.STOP_SOUND,
            args=args,
            target=self._digest_target(target),
            append_to_reader=True
        )

    def teleport(
            self, loc: Locatable,
            *, keep_current_rotation: bool = False,
            target: typing.Optional[PlayerTarget] = None
    ):
        """Teleports the player to a location.

        Parameters
        ----------
        loc : :attr:`~.Locatable`
            New position.

        keep_current_rotation : :class:`bool`, optional
            Defaults to ``False``.

        target : Optional[:class:`~.PlayerTarget`], optional
            The target of this :class:`~.PlayerAction`, or None for the current :class:`Player` instance's target.
            Defaults to ``None``.

        Returns
        -------
        :class:`PlayerAction`
            The generated PlayerAction instance.

        Examples
        --------
        ::

            p_default.teleport(loc)
            # OR
            Player(PlayerTarget.DEFAULT).teleport(loc)  # TODO: Example
        """
        args = Arguments([
            p_check(loc, Locatable, "loc")
        ], tags=[
            Tag(
                "Keep Current Rotation", option=bool(keep_current_rotation),  # default is False
                action=PlayerActionType.TELEPORT, block=BlockType.IF_GAME
            )
        ])
        return PlayerAction(
            action=PlayerActionType.TELEPORT,
            args=args,
            target=self._digest_target(target),
            append_to_reader=True
        )

    def tp_sequence(
            self, *locs: typing.Union[Locatable, Listable], delay: typing.Optional[Numeric] = None,
            target: typing.Optional[PlayerTarget] = None
    ):
        """Teleports the player to multiple locations, with a delay between each teleport.

        .. rank:: Noble


        Parameters
        ----------
        locs : Union[:attr:`~.Locatable`, :attr:`~.Listable`]
            Locations to teleport to.

        delay : Optional[:attr:`~.Numeric`], optional
            Teleport delay (ticks, default = 60). Default is ``None``.

        target : Optional[:class:`~.PlayerTarget`], optional
            The target of this :class:`~.PlayerAction`, or None for the current :class:`Player` instance's target.
            Defaults to ``None``.

        Returns
        -------
        :class:`PlayerAction`
            The generated PlayerAction instance.

        Examples
        --------
        ::

            p_default.tp_sequence(locs, delay)
            # OR
            Player(PlayerTarget.DEFAULT).tp_sequence(locs, delay)  # TODO: Example
        """
        args = Arguments([
            *[p_check(loc, typing.Union[Locatable, Listable], f"locs[{i}]") for i, loc in enumerate(locs)],
            p_check(delay, typing.Optional[Numeric], "delay") if delay is not None else None
        ])
        return PlayerAction(
            action=PlayerActionType.TP_SEQUENCE,
            args=args,
            target=self._digest_target(target),
            append_to_reader=True
        )

    def undisguise(self, *, target: typing.Optional[PlayerTarget] = None):
        """Removes the player's disguise.

        .. rank:: Overlord


        Parameters
        ----------
        target : Optional[:class:`~.PlayerTarget`], optional
            The target of this :class:`~.PlayerAction`, or None for the current :class:`Player` instance's target.
            Defaults to ``None``.

        Returns
        -------
        :class:`PlayerAction`
            The generated PlayerAction instance.

        Examples
        --------
        ::

            p_default.undisguise()
            # OR
            Player(PlayerTarget.DEFAULT).undisguise()
        """
        return PlayerAction(
            action=PlayerActionType.UNDISGUISE,
            args=Arguments(),
            target=self._digest_target(target),
            append_to_reader=True
        )

    def walk_speed(
            self, speed: Numeric,
            *, target: typing.Optional[PlayerTarget] = None
    ):
        """Sets the player's walk speed.

        .. rank:: Noble


        Parameters
        ----------
        speed : :attr:`~.Numeric`
            % of normal walk speed (0 to 500).

        target : Optional[:class:`~.PlayerTarget`], optional
            The target of this :class:`~.PlayerAction`, or None for the current :class:`Player` instance's target.
            Defaults to ``None``.

        Returns
        -------
        :class:`PlayerAction`
            The generated PlayerAction instance.

        Examples
        --------
        ::

            p_default.walk_speed(speed)
            # OR
            Player(PlayerTarget.DEFAULT).walk_speed(speed)  # TODO: Example
        """
        args = Arguments([
            p_check(speed, Numeric, "speed")
        ])
        return PlayerAction(
            action=PlayerActionType.WALK_SPEED,
            args=args,
            target=self._digest_target(target),
            append_to_reader=True
        )

    def weather_clear(self, *, target: typing.Optional[PlayerTarget] = None):
        """Sets the weather to clear weather for the player only.

        Parameters
        ----------
        target : Optional[:class:`~.PlayerTarget`], optional
            The target of this :class:`~.PlayerAction`, or None for the current :class:`Player` instance's target.
            Defaults to ``None``.

        Returns
        -------
        :class:`PlayerAction`
            The generated PlayerAction instance.

        Examples
        --------
        ::

            p_default.weather_clear()
            # OR
            Player(PlayerTarget.DEFAULT).weather_clear()
        """
        return PlayerAction(
            action=PlayerActionType.WEATHER_CLEAR,
            args=Arguments(),
            target=self._digest_target(target),
            append_to_reader=True
        )

    def weather_rain(self, *, target: typing.Optional[PlayerTarget] = None):
        """Sets the weather to downfall (rain) for the player only.

        Parameters
        ----------
        target : Optional[:class:`~.PlayerTarget`], optional
            The target of this :class:`~.PlayerAction`, or None for the current :class:`Player` instance's target.
            Defaults to ``None``.

        Returns
        -------
        :class:`PlayerAction`
            The generated PlayerAction instance.

        Examples
        --------
        ::

            p_default.weather_rain()
            # OR
            Player(PlayerTarget.DEFAULT).weather_rain()
        """
        return PlayerAction(
            action=PlayerActionType.WEATHER_RAIN,
            args=Arguments(),
            target=self._digest_target(target),
            append_to_reader=True
        )

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
        to the location the entity should be standing on, use :class:`~.LocationVar`.

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
            loc_2 = LocationVar("my var")
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

#     def cmd_equals(
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

#         def item_equals(
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

#     def cmd_arg_equals(
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


remove_u200b_from_doc(Player)
