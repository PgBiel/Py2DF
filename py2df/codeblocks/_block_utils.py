import typing
import collections
from ..classes import DFVariable, DFText, TextVar, NumberVar
from ..typings import Material, ItemParam, Textable, Listable, p_bool_check

BlockParam = typing.Union[
    Material, ItemParam, Textable
]


BlockMetadata = typing.Union[
    typing.Dict[str, typing.Optional[typing.Union[str, int, bool, DFVariable, TextVar, NumberVar]]],
    typing.Iterable[Textable],
    Listable
]


def _load_metadata(metadata: BlockMetadata, allow_none: bool = True):
    true_metadata: typing.List[Textable] = []
    if isinstance(metadata, dict):
        for k, v in metadata.items():
            val_str: str
            if isinstance(v, bool):
                val_str = "true" if v else "false"
            elif v is None:
                val_str = "none"
            else:
                val_str = str(v)

            separator: str = "="
            if "=" in val_str:
                separator = "," if ":" in val_str else ":"

            true_metadata.append(DFText(f"{k}{separator}{val_str}"))

    elif isinstance(metadata, collections.Iterable):
        true_metadata.extend(list(metadata))

    elif p_bool_check(metadata, Listable):
        true_metadata.extend(metadata)

    elif (metadata is not None) if allow_none else True:
        raise TypeError("Metadata must either be a dictionary or an iterable of Textables.")

    return true_metadata


def _load_btype(block_type: BlockParam, allow_none: bool = False) -> typing.Union[ItemParam, Textable]:
    if block_type is None and not allow_none:
        raise TypeError("Block type must not be 'None'.")

    if isinstance(block_type, (Material, str, DFText, collections.UserString)):  # check for material validity
        block_type = Material(str(block_type) if isinstance(block_type, DFText) else block_type).value

    return block_type


def _load_btypes(
    block_types: typing.Union[typing.Iterable[BlockParam], Listable]
) -> typing.List[typing.Union[ItemParam, Textable, Listable]]:
    return [block_types] if p_bool_check(block_types, Listable) else [_load_btype(b_t) for b_t in block_types]
