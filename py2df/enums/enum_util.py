from enum import Enum


class AutoNameEnum(Enum):
    """
    An enum whose auto values are the respective names of the constants.
    """

    def _generate_next_value_(name, start, count, last_values):
        return name


class AutoLowerNameEnum(Enum):
    """
    An enum whose auto values are the respective *lowercase* names of the constants.
    """

    def _generate_next_value_(name, start, count, last_values):
        return name.lower()


class AutoUpperNameEnum(Enum):
    """
    An enum whose auto values are the respective *uppercase* names of the constants.
    """

    def _generate_next_value_(name, start, count, last_values):
        return name.upper()
