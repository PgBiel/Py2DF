from .enum_util import AutoSnakeToCapitalizedWordsEnum
from enum import auto, unique


@unique
class SoundType(AutoSnakeToCapitalizedWordsEnum):
    pass  # TODO: Sound type (get display names from each sound as SNAKE_CASE instead of Capitalized Words)


@unique
class ParticleType(AutoSnakeToCapitalizedWordsEnum):
    pass  # TODO: Particle type (get display names from each sound as SNAKE_CASE instead of Capitalized Words)


@unique
class CustomSpawnEggType:  # <- still don't know which enum type to use! Snake->Words? Snake->Pascal?
    pass  # TODO: Use in Minecraft and find out its json; Ender Dragon, Giant, Iron/Snow Golem, etc
