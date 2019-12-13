import nbtlib as nbt
from nbtlib import String, Int, List, Byte, Compound, Double, Long

# region:item_schemas

# region:--main_item_schemas

ItemDisplaySchema = nbt.schema("ItemDisplaySchema", dict(
    color=Int,
    Name=String,
    Lore=List[String]
))
"""Represents the 'display' key of :class:`ItemTagSchema`."""
ItemDisplaySchema.__doc__ = """Represents the 'display' key of :class:`ItemTagSchema`."""

ItemEnchantmentSchema = nbt.schema("ItemEnchantmentSchema", dict(
    id=String,
    lvl=Int
))
"""Represents an enchantment, within the 'Enchantments' key of :class:`ItemTagSchema`."""
ItemEnchantmentSchema.__doc__ = """Represents an enchantment, within the 'Enchantments' key of \
:class:`ItemTagSchema`."""

ItemAttributeModifierSchema = nbt.schema("ItemAttributeModifierSchema", dict(
    AttributeName=String,
    Name=String,
    Slot=String,
    Operation=Int,
    Amount=Double,
    UUIDMost=Long,
    UUIDLeast=Long
))
"""Represents an attribute modifier, within the 'AttributeModifiers' key of :class:`ItemTagSchema`."""
ItemAttributeModifierSchema.__doc__ = """Represents an attribute modifier, within the 'AttributeModifiers' key of \
:class:`ItemTagSchema`."""

ItemTagSchema = nbt.schema("ItemTagSchema", dict(
    Damage=Int,
    Unbreakable=Byte,
    EntityTag=Compound,
    display=ItemDisplaySchema,
    HideFlags=Int,
    AttributeModifiers=List[ItemAttributeModifierSchema],

    # enchantments
    Enchantments=List[ItemEnchantmentSchema],
    StoredEnchantments=List[ItemEnchantmentSchema],  # for enchantment books
    RepairCost=Int,
))
"""Represents the NBT structure of the 'tag' key of :class:`ItemSchema`."""
ItemTagSchema.__doc__ = """Represents the NBT structure of the 'tag' key of :class:`ItemSchema`."""

ItemSchema = nbt.schema("ItemSchema", dict(
    id=String,
    Count=Byte,
    Slot=Byte,
    tag=ItemTagSchema
), strict=False)
"""Represents the NBT structure of an :class:`~.Item`."""
ItemSchema.__doc__ = """Represents the NBT structure of an :class:`~.Item`."""

# endregion:--main_item_schemas

# endregion:item_schemas
