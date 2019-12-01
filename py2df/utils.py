from dataclasses import dataclass


@dataclass
class NBTWrapper:
    __slots__ = ("value",)
    value: str


def nbt_dict_to_str(nbt_dict: dict) -> str:
    pass  # TODO: NBT Dict to str
