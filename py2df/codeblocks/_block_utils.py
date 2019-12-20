import typing
import collections
from ..classes import DFVariable, DFText
from ..typings import Material, ItemParam, Textable

BlockParam = typing.Union[
    Material, ItemParam, Textable
]


BlockMetadata = typing.Union[
    typing.Dict[str, typing.Optional[typing.Union[str, int, bool, DFVariable]]],
    typing.Iterable[Textable]
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

    elif (metadata is not None) if allow_none else True:
        raise TypeError("Metadata must either be a dictionary or an iterable of Textables.")

    return true_metadata


def _load_btype(block_type: BlockParam, allow_none: bool = False) -> typing.Union[ItemParam, Textable]:
    if block_type is None and not allow_none:
        raise TypeError("Block type must not be 'None'.")

    if isinstance(block_type, (Material, str, DFText, collections.UserString)):  # check for material validity
        block_type = Material(str(block_type) if isinstance(block_type, DFText) else block_type).value

    return block_type


def _load_btypes(block_types: typing.Iterable[BlockParam]) -> typing.List[typing.Union[ItemParam, Textable]]:
    return [_load_btype(b_t) for b_t in block_types]
