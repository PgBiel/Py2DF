from dataclasses import dataclass


@dataclass
class NBTWrapper:
    __slots__ = ("value",)
    value: str


def nbt_dict_to_str(nbt_dict: dict) -> str:
    pass  # TODO: NBT Dict to str


def remove_u200b_from_doc(cls: type):
    the_doc = cls.__doc__
    if "\u200b" in the_doc:
        cls.__doc__ = the_doc.replace("\u200b", "")
