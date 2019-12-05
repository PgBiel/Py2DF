"""
Dataclasses.
"""
from .. import constants
from dataclasses import dataclass, field
from ..enums import Enchantments
from ..utils import remove_u200b_from_doc


@dataclass
class Enchantment:
    """
    Represents an Enchantment to be used within :class:`~py2df.classes.mc_types.Item`.
    
    Attributes\u200b
    -----------
        id : :class:`~py2df.enums.misc_mc_enums.Enchantments`
            Type of enchantment.
        
        level : :class:`int`
            The level of this enchantment. (Cannot surpass **`{0}`**)
    """
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


Enchantment.__doc__ = str(Enchantment.__doc__).format(constants.MAX_ENCHANTMENT_LEVEL)


remove_u200b_from_doc(Enchantment)
