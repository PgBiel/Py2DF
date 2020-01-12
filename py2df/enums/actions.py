"""
All types of actions and their individual tags.
"""
from .enum_util import AutoSnakeToPascalCaseNameEnum, ActionType, TagType
from enum import auto, unique

# region:types


@unique
class PlayerActionType(ActionType, AutoSnakeToPascalCaseNameEnum):
    """Contains all types of Player Action blocks."""
    ACTION_BAR = auto()  #: Sends a message on the action bar for the selected player.
    ADD_INV_ROW = auto()  #: Adds a row to the bottom of the currently open inventory.
    ALLOW_DROPS = auto()  #: Allows the player to drop items from their inventory.
    BLOCK_DISGUISE = auto()  #: Disguises the player as a block.
    BREAK_ANIMATION = auto()  #: Makes the player see block fractures on the given blocks.
    CHAT_COLOR = auto()  #: Sets the color of all future messages in chat for the player.
    CLEAR_CHAT = auto()  #: Clears all messages on the player's chat window.
    CLEAR_EFFECTS = auto()  #: Removes all potion effects from the player.
    CLEAR_INV = auto()  #: Empties the player's inventory.
    CLEAR_ITEM = auto()  #: Removes all of a certain item from the player.
    CLOSE_INV = auto()  #: Closes the player's currently open inventory menu.
    DAMAGE = auto()  #: Damages the player.
    DEATH_DROPS = auto()  #: The player will now drop the contents of their inventory when they die.
    DISABLE_BLOCKS = auto(
    )  #: Prevents the player from placing and breaking certain blocks, or all if none are specified.
    DISABLE_FLIGHT = auto()  #: Prevents the player from flying.
    DISABLE_PVP = auto()  #: Prevents the player from damaging other players.
    DISALLOW_DROPS = auto()  #: Prevents the player from dropping items from their inventory.
    ENABLE_BLOCKS = auto()  #: Allows the player to place and break certain blocks (or all, if none are specified).
    ENABLE_FLIGHT = auto()  #: Allows the player to fly.
    ENABLE_PVP = auto()  #: Allows the player to damage other players.
    EXPAND_INV = auto(
    )  #: If an inventory menu is open for the player, this adds 3 more rows using the contents of the chest.
    FLIGHT_SPEED = auto()  #: Sets the player's flight speed.
    FORCE_FLIGHT = auto()  #: Forces the player to start or stop flying.
    FORCE_GLIDE = auto()  #: Forces the player to start or stop gliding.
    GIVE_EFFECT = auto()  #: Gives the player one or more potion effects.
    GIVE_ITEMS = auto()  #: Gives the player all of the items in the chest.
    GIVE_RNG_ITEM = auto()  #: Gives the player a random item or stack of items from the chest.
    GM_ADVENTURE = auto()  #: Sets the player's gamemode to adventure mode.
    GM_SURVIVAL = auto()  #: Sets the player's gamemode to survival mode.
    HEAL = auto()  #: Restores the player's health fully or by an amount.
    HIDE_DISGUISE = auto()  #: Hides the player's disguise on their screen.
    KEEP_INV = auto()  #: The player will now keep the contents of their inventory when they die.
    KICK = auto()  #: Kicks the player from the plot.
    LAUNCH_FWD = auto()  #: Launches the player a certain amount forward or backward.
    LAUNCH_PROJ = auto()  #: Launches a projectile from the player.
    LAUNCH_TOWARD = auto()  #: Launches the player toward a certain location.
    LAUNCH_UP = auto(
    )  #: Launches the player a certain amount up or down. Positive amount is up; negative amount is down.
    LIGHTNING_EFFECT = auto()  #: Plays a thunderbolt effect to the player that is silent and deals no damage.
    LOAD_INV = auto()  #: Loads the selected saved inventory.
    MOB_DISGUISE = auto()  #: Disguises the player as a mob.
    NAT_REGEN = auto()  #: Allows the player's health to regenerate naturally.
    NO_DEATH_DROPS = auto()  #: The player will no longer drop the contents of their inventory when they die.
    NO_KEEP_INV = auto()  #: The player will no longer keep the contents of their inventory when they die.
    NO_NAT_REGEN = auto()  #: Prevents the player's health from regenerating naturally.
    NO_PROJ_COLL = auto()  #: Prevents projectiles from hitting the player.
    OPEN_BLOCK_INV = auto()  #: Opens a container inventory. Also works with crafting tables.
    OPEN_BOOK = auto()  #: Opens a written book menu.
    PARTICLE_EFFECT = auto()  #: Plays one or more of the particle to the player.
    PLAY_SOUND = auto()  #: Plays a sound effect for the player.
    PLAY_SOUND_SEQ = auto()  #: Plays a sequence of sounds for the player, with a delay after each sound.
    PLAYER_DISGUISE = auto()  #: Disguises the player as another player.
    PROJ_COLL = auto()  #: Allows projectiles to hit the player.
    REMOVE_BOSS_BAR = auto()  #: Removes the given boss bar from the player if there is one.
    REMOVE_EFFECT = auto()  #: Removes 1 or more potion effects from the player.
    REMOVE_INV_ROW = auto()  #: Removes the given number of rows from the bottom of the currently open inventory.
    REMOVE_ITEM = auto()  #: Removes certain items from the player.
    REPLACE_ITEM = auto()  #: Replaces the specified items with the given item in the player's inventory.
    REPLACE_PROJ = auto()  #: Replaces the projectile fired in the Shoot Bow Event.
    RESPAWN = auto()  #: Respawns the player if they are dead.
    RIDE_ENTITY = auto()  #: Mounts the player on top of another player or entity.
    RM_ARROWS = auto()  #: Clears any arrows stuck  in the player's body.
    RM_WORLD_BORDER = auto()  #: Removes the world border for this player.
    RNG_TELEPORT = auto()  #: Teleports the player to a random location in the chest.
    ROLLBACK_BLOCKS = auto()  #: Undoes the interactions with blocks by the player.
    SAVE_INV = auto(
    )  #: Saves the selected player's current inventory, which can be loaded later with 'Load Saved Inventory'.
    SEND_ADVANCEMENT = auto()  #: Sends an advancement popup to the player.
    SEND_BLOCK = auto()  #: Makes client side, player specific blocks appear at the given location or area.
    SEND_DIALOGUE = auto()  #: Sends a series of messages in chat to the player, with a delay after each message.
    SEND_HOVER = auto()  #: Sends a message to the player, with a second one that appears when the player 'hovers' over.
    SEND_MESSAGE = auto()  #: Sends a chat message to the player.
    SEND_TITLE = auto()  #: Sends a title message to the player.
    SET_AIR_TICKS = auto()  #: Sets the player's remaining breath ticks.
    SET_ARMOR = auto(
    )  #: Sets the armor of the player. Specify the armor in slots 1-4, with 1 being the helmet and 4 being the boots.
    SET_ATK_SPEED = auto()  #: Sets the player's attack speed.
    SET_BOSS_BAR = auto()  #: Sets the player's boss bar.
    SET_CHAT_TAG = auto()  #: Sends a chat message to the player.
    SET_COMPASS = auto()  #: Sets the location compasses point to for the player.
    SET_CURSOR_ITEM = auto()  #: Sets the item on the player's cursor.
    SET_FALL_DISTANCE = auto()  #: Sets the player's fall distance, affecting fall damage upon landing.
    SET_FIRE_TICKS = auto()  #: Sets the player on fire for a certain number of ticks.
    SET_FOOD_LEVEL = auto()  #: Sets the player's food level.
    SET_HAND_ITEM = auto()  #: Sets the item in the player's main hand or off hand.
    SET_HEALTH = auto()  #: Sets the player's health or absorption hearts.
    SET_INV_NAME = auto()  #: Renames the player's currently open plot inventory.
    SET_ITEM_COOLDOWN = auto()  #: Applies a cooldown visual effect to an item type.
    SET_ITEMS = auto()  #: Changes the player's inventory accordingly to the items in the  parameter chest.
    SET_LIST_HEADER = auto()  #: Sets the player list header / footer for the player.
    SET_MAX_HEALTH = auto()  #: Sets the maximum amount of health that the player can have.
    SET_MENU_ITEM = auto()  #: Sets the specified slot in the player's currently open inventory menu to the given item.
    SET_NAME_COLOR = auto()  #: Sets the color the player's name tag appears in.
    SET_SATURATION = auto()  #: Sets the player's saturation level.
    SET_SLOT = auto()  #: Sets a player's selected hotbar slot.
    SET_SLOT_ITEM = auto()  #: Like 'Give Items', but you can control which inventory slot the item goes in.
    SET_TIME = auto()  #: Sets the time of day for the player only.
    SET_WORLD_BORDER = auto()  #: Creates a world border visible to only the player.
    SET_XP_LVL = auto()  #: Sets the player's experience level.
    SET_XP_PROG = auto()  #: Sets the XP progress bar to a certain percentage.
    SHIFT_WORLD_BORDER = auto()  #: Changes the player's world border size, if they have one active.
    SHOW_DISGUISE = auto()  #: Shows the player's disguise on their screen.
    SHOW_INV = auto()  #: Opens a custom item inventory for the player.
    STOP_SOUND = auto()  #: Stops all, or specific sound effects for the player.
    TELEPORT = auto()  #: Teleports the player to a location.
    TP_SEQUENCE = auto()  #: Teleports the player to multiple locations, with a delay between each teleport.
    UNDISGUISE = auto()  #: Removes the player's disguise.
    WALK_SPEED = auto()  #: Sets the player's walk speed.
    WEATHER_CLEAR = auto()  #: Sets the weather to clear weather for the player only.
    WEATHER_RAIN = auto()  #: Sets the weather to downfall (rain) for the player only.


@unique
class EntityActionType(ActionType, AutoSnakeToPascalCaseNameEnum):
    """Contains all types of Entity Action blocks."""
    ARMOR_STAND_TAGS = auto()  #: Changes the settings of an armor stand, such as visibility.
    BLOCK_DISGUISE = auto()  #: Disguises the entity as a block.
    CREEPER_CHARGED = auto()  #: Sets whether a creeper has the charged effect.
    CREEPER_IGNITED = auto()  #: Sets whether a creeper is currently ignited. (getting ready to explode)
    CREEPER_MAX_FUSE = auto()  #: Sets the starting amount of fuse ticks of a creeper.
    CREEPER_RADIUS = auto()  #: Sets the explosion radius of a creeper.
    DAMAGE = auto()  #: Damages the mob.
    DISABLE_GLOWING = auto()  #: Makes the entity no longer glow.
    DROP_ITEMS = auto()  #: After this code block is executed, the mob will drop their equipment and loot when they die.
    ENABLE_AI = auto()  #: Enables the AI of the mob.
    ENABLE_GLOWING = auto()  #: Makes the entity glow.
    END_CRYSTAL_TARGET = auto()  #: Sets an end crystal's beam target.
    EXPLODE_CREEPER = auto()  #: Causes a creeper to instantly explode.
    GIVE_EFFECT = auto()  #: Gives the mob one or more potion effects.
    GRAVITY = auto()  #: Enables gravity for the entity.
    HEAL = auto()  #: Restores the mob's health fully or by an amount.
    HIDE_NAME = auto()  #: Hides the name tag of the entity.
    HORSE_APPEARANCE = auto()  #: Sets the appearance (the variant) of a horse.
    JUMP_STRENGTH = auto()  #: Sets the jump strength of a horse.
    LAUNCH_FWD = auto()  #: Launches the entity a certain amount forward or backward.
    LAUNCH_PROJ = auto()  #: Launches a projectile from the mob.
    LAUNCH_TOWARD = auto()  #: Launches the entity toward a certain location.
    LAUNCH_UP = auto()  #: Launches the entity some amount up or down. Positive amount is up; negative amount is down.
    MOB_DISGUISE = auto()  #: Disguises the entity as a mob.
    MOOSHROOM_VARIANT = auto()  #: Sets the skin type of a mooshroom.
    MOVE_TO = auto()  #: Instructs the mob's AI to always pathfind to a certain location at a certain speed.
    NO_AI = auto()  #: Disables the AI of the mob.
    NO_DROPS = auto()  #: The mob will no longer drop their equipment and loot when they die.
    NO_GRAVITY = auto()  #: Disables gravity for the entity.
    NO_PROJ_COLL = auto()  #: Prevents projectiles from hitting the mob.
    PLAYER_DISGUISE = auto()  #: Disguises the entity as a player.
    PROJ_COLL = auto()  #: Allows projectiles to hit the mob.
    PROJECTILE_ITEM = auto()  #: Sets the item the projectile displays as.
    REMOVE = auto()  #: Deletes the entity.
    REMOVE_EFFECT = auto()  #: Removes one or more potion effects from the mob.
    RIDE_ENTITY = auto()  #: Mounts the entity on top of another player or entity.
    SET_AGEOR_SIZE = auto()  #: Sets whether a mob should age.
    SET_ARMOR = auto(
    )  #: Sets the armor of the mob. Specify the armor in slots 1-4, with 1 being the helmet and 4 being the boots.
    SET_CAT_TYPE = auto()  #: Sets the skin type of a cat.
    SET_COLOR = auto()  #: Sets the color of a mob.
    SET_FALL_DISTANCE = auto()  #: Sets the entity's fall distance, affecting fall damage upon landing.
    SET_FIRE_TICKS = auto()  #: Sets the entity on fire for a certain number of ticks.
    SET_FOX_TYPE = auto()  #: Sets the fur type of a fox.
    SET_HAND_ITEM = auto()  #: Sets the item in the mob's main hand or off hand.
    SET_HORSE_ARMOR = auto()  #: Sets the armor of a horse.
    SET_HORSE_CHEST = auto()  #: Sets whether a horse has a chest equipped.
    SET_ITEM_OWNER = auto()  #: Sets an item's owner.
    SET_MAX_HEALTH = auto()  #: Sets the maximum amount of health that the mob can have.
    SET_NAME = auto()  #: Changes the name of the entity.
    SET_PANDA_GENES = auto()  #: Sets the genes (traits) of a panda.
    SET_PARROT_VARIANT = auto()  #: Sets the skin variant of a parrot.
    SET_PICKUP_DELAY = auto()  #: Sets an item's pickup delay.
    SET_POSE = auto()  #: Sets the three-dimensional rotation of an armor stand part.
    SET_RABBIT_TYPE = auto()  #: Sets the skin type of a rabbit.
    SET_SADDLE = auto()  #: Sets the saddle or carpet item of a mob.
    SET_SHEEP_SHEARED = auto()  #: Sets whether a sheep is currently sheared.
    SET_SLIME_AI = auto(
    )  #: Allows a slime's AI to be enabled/disabled, but unlike the disable AI action, the slime can still be moved.
    SET_SNOWMAN_PUMP = auto()  #: Sets whether a snowman is wearing a pumpkin.
    SET_TARGET = auto()  #: Instructs the mob's AI to target a specific mob or player.
    SET_TROP_FISH_TYPE = auto()  #: Sets the skin type of a tropical fish.
    SET_VILLAGER_PROF = auto()  #: Sets a villager's profession.
    SET_VILLAGER_TYPE = auto()  #: Sets the biome type of a villager.
    SET_WOLF_ANGRY = auto()  #: Sets whether a wolf is angry.
    SHEAR_SHEEP = auto()  #: Causes a sheep to be sheared.
    SHEEP_EAT = auto()  #: Causes a sheep to eat grass.
    SHOW_NAME = auto()  #: Shows the name tag of the entity.
    SILENCE = auto()  #: Prevents the entity from making any sounds.
    SNOWMAN_PUMPKIN = auto() #: Sets whether a snowman is wearing a pumpkin.
    TAME = auto()  #: Tames the mob (if possible).
    TELEPORT = auto()  #: Teleports the entity to a specified location.
    TP_SEQUENCE = auto()  #: Teleports the entity to multiple locations, with a delay between each teleport.
    UNDISGUISE = auto()  #: Removes the entity's disguise.
    UNSILENCE = auto()  #: Allows the entity to make sounds.


@unique
class ControlType(ActionType, AutoSnakeToPascalCaseNameEnum):
    """Contains all types of Control blocks."""
    END = auto()  #: Stops reading all code after the control block.
    RETURN = auto(
    )  #: Returns to the Call Function block the current Function was called from, and continues code from there.
    SKIP = auto()  #: Skips the rest of this repeat statement's code and continues to the next repetition.
    STOP_REPEAT = auto()  #: Stops a repeating sequence and continues to the next code block.
    WAIT = auto()  #: Pauses the current line of code for a certain amount of ticks seconds, or minutes.


@unique
class GameActionType(ActionType, AutoSnakeToPascalCaseNameEnum):
    """Contains all types of Game Action blocks."""
    BLOCK_DROPS_OFF = auto()  #: Disables blocks dropping as items when broken.
    BLOCK_DROPS_ON = auto()  #: Enables blocks dropping as items when broken.
    BONE_MEAL = auto()  #: Applies bone meal to a block.
    BREAK_BLOCK = auto()  #: Breaks a block at a certain location as if it was broken by a player.
    CANCEL_EVENT = auto()  #: Cancels the initial event that triggered this line of code.
    CHANGE_SIGN = auto()  #: Changes a line of text on a sign.
    CLEAR_SC_BOARD = auto()  #: Removes all scores from the scoreboard.
    COPY_BLOCKS = auto()  #: Copies a region of blocks to another region, including air blocks.
    CREATE_ANIMATED_PARTICLE_CIRCLE = "PFX Circle [A]"  #: Creates an animated circle of particles at a certain location.
    CREATE_ANIMATED_PARTICLE_LINE = "PFX Line [A]"  #: Creates a line of particles between two locations.
    CREATE_ANIMATED_PARTICLE_SPIRAL = "PFX Spiral [A]"  #: Creates an animated spiral of particles at a certain location.
    CREATE_HOLOGRAM = auto()  #: Creates a hologram (floating text) at a certain location.
    CREATE_PARTICLE_CIRCLE = "PFX Circle"  #: Creates a circle of particles at a certain location.
    CREATE_PARTICLE_CLUSTER = "PFX Cluster"  #: Randomly spawns particles around a certain location.
    CREATE_PARTICLE_LINE = "PFX Line"  #: Creates a line of particles between two locations.
    CREATE_PARTICLE_PATH = "PFX Path"  #: Creates a path of particles that goes through each location in the chest from first to last.
    CREATE_PARTICLE_RAY = "PFX Ray"  #: Creates a ray of particles starting at a certain location.
    CREATE_PARTICLE_SPHERE = "PFX Sphere"  #: Creates a sphere of particles at a certain location.
    CREATE_PARTICLE_SPIRAL = "PFX Spiral"  #: Creates a spiral of particles at a certain location.
    DROP_BLOCK = auto()  #: Spawns a falling block at the specified location.
    EMPTY_CONTAINER = auto()  #: Empties a container.
    EXPLOSION = auto()  #: Creates an explosion at a certain location.
    FILL_CONTAINER = auto()  #: Fills a container with items.
    FIREWORK = auto()  #: Launches a firework at a certain location.
    FIREWORK_EFFECT = auto()  #: Creates a firework explosion at a certain location.
    HIDE_SIDEBAR = auto()  #: Disables the scoreboard sidebar on the plot.
    LAUNCH_PROJ = auto()  #: Launches a projectile.
    LOCK_CONTAINER = auto()  #: Sets a container's lock key.
    PLAY_PARTICLE_EFFECT = "Particle FX"  #: Plays a particle effect at a certain location.
    REMOVE_HOLOGRAM = auto()  #: Removes a hologram.
    REMOVE_SCORE = auto()  #: Removes a score from the scoreboard.
    SET_BLOCK = auto()  #: Sets the block at a certain location or region.
    SET_BLOCK_DATA = auto()  #: Sets a metadata tag for a certain block.
    SET_CONTAINER = auto()  #: Sets a container's contents.
    SET_CONTAINER_NAME = auto()  #: Sets the custom name of a container (e.g. chests).
    SET_FURNACE_SPEED = auto()  #: Sets the cook time multiplier of a furnace.
    SET_SC_OBJ = auto()  #: Sets the objective name of the scoreboard on your plot.
    SET_SCORE = auto()  #: Sets a score on the scoreboard.
    SHOW_SIDEBAR = auto()  #: Enables the scoreboard sidebar on the plot.
    SPAWN_ARMOR_STAND = auto()  #: Creates an armor stand at a certain location.
    SPAWN_CRYSTAL = auto()  #: Spawns an End Crystal at a certain location.
    SPAWN_EXP_ORB = auto()  #: Spawns an experience orb at a certain location.
    SPAWN_FANGS = auto()  #: Spawns Evoker Fangs at a certain location.
    SPAWN_ITEM = auto()  #: Spawns an item at a certain location.
    SPAWN_MOB = auto()  #: Spawns a mob at a certain location.
    SPAWN_RNG_ITEM = auto()  #: Randomly spawns an item at a certain location.
    SPAWN_TNT = auto()  #: Spawns primed TNT at a certain location.
    SPAWN_VEHICLE = auto()  #: Spawns a vehicle at a certain location.
    START_LOOP = auto()  #: Activates your plot's Loop Block if it has one.
    STOP_LOOP = auto()  #: Deactivates your plot's Loop Block if it has one.
    SUMMON_LIGHTNING = auto()  #: Strikes lightning at a certain location, damaging players in a radius.
    TICK_BLOCK = auto()  #: Causes a block to get random ticked.
    UNCANCEL_EVENT = auto()  #: Uncancels the initial event that triggered this line of code.

# endregion:types


# region:tags

    # region:player_action_tags


@unique
class PARowPos(TagType):
    """Tag for :meth:`~.Player.add_inv_row` and :meth:`~.Player.remove_inv_row`."""
    TOP = "Top Row"
    BOTTOM = "Bottom Row"


@unique
class PAClearInvMode(TagType):
    """Tag for :meth:`~.Player.clear_inv`."""
    ENTIRE_INVENTORY = auto()
    UPPER_INVENTORY = auto()
    HOTBAR = auto()
    ARMOR = auto()


@unique
class AdvancementType(TagType):
    """Tag for :meth:`~.Player.send_advancement`."""
    ADVANCEMENT = auto()
    GOAL = auto()
    CHALLENGE = auto()


@unique
class BossBarColor(TagType):
    """Tag for :meth:`~.Player.set_boss_bar`."""
    PINK = auto()
    BLUE = auto()
    RED = auto()
    GREEN = auto()
    YELLOW = auto()
    PURPLE = auto()
    WHITE = auto()


@unique
class BossBarStyle(TagType):
    """Tag for :meth:`~.Player.set_boss_bar`."""
    SOLID = "Solid"
    SIX_SEGMENTS = "Segmented 6"
    TEN_SEGMENTS = "Segmented 10"
    TWELVE_SEGMENTS = "Segmented 12"
    TWENTY_SEGMENTS = "Segmented 20"


@unique
class PlayerAnimation(TagType):
    """Tag of :meth:`~.Player.send_animation`."""
    SWING_RIGHT_ARM = auto()
    SWING_LEFT_ARM = auto()
    HURT_ANIMATION = auto()
    CRIT_PARTICLES = auto()
    ENCHANTED_HIT_PARTICLES = auto()
    WAKE_UP = auto()

# endregion:player_action_tags

    # region:entity_action_tags

@unique
class HorseColor(TagType):
    WHITE = auto()
    CREAMY = auto()
    CHESTNUT = auto()
    BROWN = auto()
    BLACK = auto()
    GRAY = auto()
    DARK_BROWN = auto()


@unique
class HorseVariant(TagType):
    NONE = auto()
    WHITE = auto()
    WHITEFIELD = auto()
    WHITE_DOTS = auto()
    BLACK_DOTS = auto()


@unique
class EffectParticleMode(TagType):
    """Tag for :meth:`.Entity.give_effect` and :meth:`.Player.give_effect`."""
    SHOWN = auto()
    BEACON = auto()
    HIDDEN = auto()


@unique
class MooshroomVariant(TagType):
    RED = auto()
    BROWN = auto()


@unique
class EntityAnimation(TagType):
    """Tag of :meth:`~.Entity.send_animation`."""
    SWING_RIGHT_ARM = auto()
    SWING_LEFT_ARM = auto()
    HURT_ANIMATION = auto()
    CRIT_PARTICLES = auto()
    ENCHANTED_HIT_PARTICLES = auto()


@unique
class CatType(TagType):
    """Tag of :meth:`~.Entity.set_cat_type`."""
    TABBY = auto()
    BLACK = auto()
    RED_AKA_GARFIELD = "Red (Garfield)"
    SIAMESE = auto()
    BRITISH_SHORTHAIR = auto()
    CALICO = auto()
    PERSIAN = auto()
    RAGDOLL = auto()
    WHITE = auto()
    JELLIE = auto()
    ALL_BLACK = auto()


@unique
class FoxType(TagType):
    """Tag of :meth:`~.Entity.set_fox_type`."""
    RED = auto()
    SNOW = auto()


@unique
class RabbitType(TagType):
    """Tag of :meth:`~.Entity.set_rabbit_type`."""
    BROWN = auto()
    WHITE = auto()
    BLACK = auto()
    BLACK_AND_WHITE = "Black and White"
    GOLD = auto()
    SALT_AND_PEPPER = "Salt and Pepper"


@unique
class TropicalFishPattern(TagType):
    """Tag of :meth:`~.Entity.set_tropical_fish_type`."""
    KOB = auto()
    SUNSTREAK = auto()
    SNOOPER = auto()
    DASHER = auto()
    BRINELY = auto()
    SPOTTY = auto()
    FLOPPER = auto()
    STRIPEY = auto()
    GLITTER = auto()
    BLOCKFISH = auto()
    BETTY = auto()
    CLAYFISH = auto()


@unique
class PandaGene(TagType):
    """Tag of :meth:`~.Entity.set_panda_genes`."""
    LAZY = auto()
    WORRIED = auto()
    PLAYFUL = auto()
    BROWN = auto()
    WEAK = auto()
    AGGRESSIVE = auto()


@unique
class ParrotVariant(TagType):
    """Tag of :meth:`~.Entity.set_parrot_variant`."""
    RED = auto()
    BLUE = auto()
    GREEN = auto()
    CYAN = auto()
    GRAY = auto()


@unique
class VillagerProfession(TagType):
    """Tag of :meth:`~.Entity.set_villager_profession`."""
    NONE = auto()
    ARMORER = auto()
    BUTCHER = auto()
    CARTOGRAPHER = auto()
    CLERIC = auto()
    FARMER = auto()
    FISHERMAN = auto()
    FLETCHER = auto()
    LEATHERWORKER = auto()
    LIBRARIAN = auto()
    MASON = auto()
    NITWIT = auto()
    SHEPHERD = auto()
    TOOLSMITH = auto()
    WEAPONSMITH = auto()


@unique
class VillagerBiome(TagType):
    """Tag of :meth:`~.Entity.set_villager_biome`."""
    DESERT = auto()
    JUNGLE = auto()
    PLAINS = auto()
    SAVANNA = auto()
    SNOW = auto()
    SWAMP = auto()
    TAIGA = auto()


@unique
class ArmorStandPart(TagType):
    """Tag of :meth:`~.Entity.set_armorstand_pose`."""
    HEAD = auto()
    BODY = auto()
    LEFT_ARM = auto()
    RIGHT_ARM = auto()
    LEFT_LEG = auto()
    RIGHT_LEG = auto()


class EntityColor(TagType):
    """Tag of :meth:`~.Entity.set_color` and :meth:`~.Entity.set_tropical_fish_type`."""
    WHITE = auto()
    ORANGE = auto()
    MAGENTA = auto()
    LIGHT_BLUE = auto()
    YELLOW = auto()
    LIME = auto()
    PINK = auto()
    GRAY = auto()
    LIGHT_GRAY = auto()
    CYAN = auto()
    PURPLE = auto()
    BLUE = auto()
    BROWN = auto()
    GREEN = auto()
    RED = auto()
    BLACK = auto()

# endregion:entity_action_tags

# region:control_tags


@unique
class CWaitTag(TagType):
    """For :meth:`~py2df.codeblocks.actions.Control.wait`; the time unit to use when specifying the wait duration."""
    TICKS = auto()
    SECONDS = auto()
    MINUTES = auto()


TimeUnit = CWaitTag  # alias

# endregion:control_tags

# endregion:tags
