from .enum_util import AutoSnakeToCapitalizedWordsEnum
from enum import auto, unique

@unique
class SoundType(AutoSnakeToCapitalizedWordsEnum):
    pass  # TODO: Sound type (get display names from each sound as SNAKE_CASE instead of Capitalized Words)
