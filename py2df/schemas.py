import nbtlib as nbt
from nbtlib import String, Int, List, Byte, Compound, Double, Long

# region:item_schemas

# region:--main_item_schemas

ItemDisplaySchema = nbt.schema("ItemDisplaySchema", dict(
    color=Int,
    Name=String,
    Lore=List[String]
))

ItemEnchantmentSchema = nbt.schema("ItemEnchantmentSchema", dict(
    id=String,
    lvl=Int
))

ItemAttributeModifierSchema = nbt.schema("ItemAttributeModifierSchema", dict(
    AttributeName=String,
    Name=String,
    Slot=String,
    Operation=Int,
    Amount=Double,
    UUIDMost=Long,
    UUIDLeast=Long
))

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

ItemSchema = nbt.schema("ItemSchema", dict(
    id=String,
    Count=Byte,
    Slot=Byte,
    tag=ItemTagSchema
), strict=False)

# endregion:--main_item_schemas

# endregion:item_schemas
