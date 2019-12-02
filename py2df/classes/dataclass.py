from .. import constants
from dataclasses import dataclass, field
from ..enums import Enchantments


@dataclass
class Enchantment:
    id: Enchantments
    level: int = 1

    def __post_init__(self):
        if self.level > constants.MAX_ENCHANTMENT_LEVEL:
            raise OverflowError(f"Enchantment level too big (max {constants.MAX_ENCHANTMENT_LEVEL})")

        if (
            type(self.id) != Enchantments
                and type(self.id) != str
                and self.id.upper() not in Enchantments._member_names_  # not a valid "Enchantments"
        ):
            raise TypeError("'id' attribute must be instance of Enchantments.")

        if type(self.id) == str:
            self.id = Enchantments(self.id.lower())
