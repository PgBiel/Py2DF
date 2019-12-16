import typing

from .actions import PlayerAction, EntityAction
from ..enums import PlayerTarget, EntityTarget


class Player:
    """Represents a DiamondFire Player. Used for Player Action and If Player humanized methods.

    Parameters
    ----------\u200b
    target : Optional[:class:`~.PlayerTarget`], optional
        The target that this instance represents (Default Player, Killer, Victim etc.) or None for default. Defaults
        to ``None``

    Attributes
    ----------\u200b
    target : Optional[:class:`~.PlayerTarget`]
        The target that this instance represents (Default Player, Killer, Victim etc.) or None for default.
    """
    __slots__ = ("target",)
    target: typing.Optional[PlayerTarget]

    def __init__(self, target: typing.Optional[PlayerTarget]):
        self.target: typing.Optional[PlayerTarget] = PlayerTarget(target) if target else None
    
    def _digest_target(self, target: typing.Optional[PlayerTarget]) -> typing.Optional[PlayerTarget]:
        """Checks a given player target for validity.
        
        Parameters
        ----------
        target : Optional[:class:`~.PlayerTarget`]
            The target to check.

        Returns
        -------
        Optional[:class:`~.PlayerTarget`]
            Returns the given target as a valid PlayerTarget, or None.
        """
        return PlayerTarget(target) if target else None
    
    # region:playeractions
    
    # endregion:playeractions
    
    # region:ifplayer
    
    # endregion:ifplayer


class Entity:
    """Represents a DiamondFire Entity. Used for Entity Action and If Entity humanized methods.

    Parameters
    ----------\u200b
    target : Optional[:class:`~.EntityTarget`], optional
        The target that this instance represents (Default Entity, Last Mob, Victim etc.) or None for default. Defaults
        to ``None``

    Attributes
    ----------\u200b
    target : Optional[:class:`~.EntityTarget`]
        The target that this instance represents (Default Entity, Last Mob, Victim etc.) or None for default.
    """
    __slots__ = ("target",)
    target: typing.Optional[EntityTarget]

    def __init__(self, target: typing.Optional[EntityTarget]):
        self.target: typing.Optional[EntityTarget] = EntityTarget(target) if target else None

    def _digest_target(self, target: typing.Optional[EntityTarget]) -> typing.Optional[EntityTarget]:
        """Checks a given entity target for validity.

        Parameters
        ----------
        target : Optional[:class:`~.EntityTarget`]
            The target to check.

        Returns
        -------
        Optional[:class:`~.EntityTarget`]
            Returns the given target as a valid EntityTarget, or None.
        """
        return EntityTarget(target) if target else None

    # region:entityactions

    # endregion:entityactions

    # region:ifentity

    # endregion:ifentity
