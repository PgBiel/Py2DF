from .enum_util import AutoSnakeToPascalCaseNameEnum, EventType
from enum import auto, unique


@unique
class PlayerEventType(EventType, AutoSnakeToPascalCaseNameEnum):
    """Contains all types of Player Event blocks."""
    BREAK_BLOCK = auto()  #: Executes code when a player breaks a block.
    BREAK_ITEM = auto()  #: Executes code when a player breaks an item.
    CHANGE_SLOT = auto()  #: Executes code when a player changes their hotbar slot.
    CLICK_ENTITY = auto()  #: Executes code when a player right clicks an entity.
    CLICK_ITEM = auto()  #: Executes code when a player clicks an item in an inventory menu.
    CLICK_OWN_INV = auto()  #: Executes code when a player clicks an item inside their inventory.
    CLICK_PLAYER = auto()  #: Executes code when a player clicks another player.
    CLOSE_INV = auto()  #: Executes code when a player closes an inventory.
    COMMAND = auto()  #: Executes code when a player types a command on the plot.
    CONSUME = auto()  #: Executes code when a player eats or drinks an item.
    DAMAGE_ENTITY = auto()  #: Executes code when a player damages an entity.
    DEATH = auto()  #: Executes code when a player dies, not as a result of another player or entity.
    DISMOUNT = auto()  #: Executes code when a player dismounts a vehicle or other entity.
    DROP_ITEM = auto()  #: Executes code when a player drops an item.
    ENTITY_DMG_PLAYER = auto()  #: Executes code when an entity damages a player.
    FALL_DAMAGE = auto()  #: ???
    JOIN = auto()  #: Executes code when a player joins the plot.
    JUMP = auto()  #: Executes code when a player jumps.
    KILL_MOB = auto()  #: Executes code when a player kills a mob.
    KILL_PLAYER = auto()  #: Executes code when a player kills another player.
    LEFT_CLICK = auto()  #: Executes code when a player left clicks.
    LOOP_EVENT = auto()  #:
    MOB_KILL_PLAYER = auto()  #: Executes code when a mob kills a player.
    PICKUP_ITEM = auto()  #: Executes code when a player picks up an item.
    PLACE_BLOCK = auto()  #: Executes code when a player places a block.
    PLAYER_DMG_PLAYER = auto()  #: Executes code when a player damages another player.
    PLAYER_TAKE_DMG = auto()  #: Executes code when a player takes damage.
    PROJ_DMG_PLAYER = auto()  #: Executes code when a projectile damages a player.
    PROJ_HIT = auto()  #: Executes code when a projectile launched by a player hits a block/an entity/another player.
    QUIT = auto()  #: Executes code when a player leaves the plot.
    RESPAWN = auto()  #: Executes code when a player respawns.
    RIGHT_CLICK = auto()  #: Executes code when a player right clicks while looking at a block or holding an item.
    RIPTIDE = auto()  #: Executes code when a player throws a riptide trident.
    SHOOT_BOW = auto()  #: Executes code when a player fires an arrow with a bow.
    SNEAK = auto()  #: Executes code when a player sneaks.
    START_FLY = auto()  #: Executes code when a player starts flying.
    START_SPRINT = auto()  #: Executes code when a player starts sprinting.
    STOP_FLY = auto()  #: Executes code when a player stops flying.
    STOP_SPRINT = auto()  #: Executes code when a player stops sprinting.
    SWAP_HANDS = auto()  #: Executes code when a player swaps an item or items between their main hand and off hand.
    UNSNEAK = auto()  #: Executes code when a player stops sneaking.
    WALK = auto()  #: Executes code while a player is walking.


@unique
class EntityEventType(EventType, AutoSnakeToPascalCaseNameEnum):
    """Contains all types of Entity Event blocks."""
    BLOCK_FALL = auto()  #: Executes code when a block affected by gravity turns into a falling block.
    ENTITY_DEATH = auto()  #: Executes code when an entity dies by natural causes.
    ENTITY_DMG = auto()  #: Executes code when an entity takes damage.
    ENTITY_DMG_ENTITY = auto()  #: Executes code when an entity damages another entity.
    ENTITY_KILL_ENTITY = auto()  #: Executes code when an entity kills another entity.
    FALLING_BLOCK_LAND = auto()  #: Executes code when a falling block lands on the ground.
    PROJ_DMG_ENTITY = auto()  #: Executes code when a projectile damages an entity.
    PROJ_KILL_ENTITY = auto()  #: Executes code when a projectile kills an entity.
    VEHICLE_DAMAGE = auto()  #: Executes code when a vehicle entity (minecart or boat) is damaged.
