import constants
import typing
import re


class Item:
    """
    Represents a Minecraft item.
    """
    __slots__ = ()

    def __init__(self):
        pass  # TODO - Material, quantity, multiplication override to set item stack amount, lore...

    def as_json_data(self) -> dict:
        pass  # TODO - returns dict

    def to_item(self) -> "Item":
        return self  # # #


class DFText:
    """
    Represents Minecraft Text variable. (note: this is not a dynamic variable.)

    `Attributes`:
        value: The value of the text variable. String.

        convert_color: Whether or not should convert "&" to "§" (section sign) to allow easier color code writing.
            Defaults to True.
    """
    __slots__ = ("value", "convert_color")
    value: str
    convert_color: bool

    def __init__(self, text: str = "", *, convert_color: bool = True):
        """
        Init text variable.
        :param text: Text, defaults to "" (empty str).
        :param convert_color: Boolean; whether or not should convert &x to color codes (§x). (Defaults to True)
        """
        self.value = text
        self.convert_color = bool(convert_color)

    def set(self, new_text: str):
        """
        Set the value of this text variable.
        :param new_text: The new text.
        """
        self.value = new_text

    def as_json_data(self) -> dict:
        """
        Obtain this variable represented as a JSON object (dict).
        :return: Dict.
        """
        converted_str: str = re.sub(
            constants.STR_COLOR_CODE_REGEX, constants.SECTION_SIGN + r"\1", self.value
        ) if self.convert_color else self.value  # convert color

        return dict(
            id=constants.ITEM_ID_TEXT_VAR,
            data=dict(
                name=converted_str
            )
        )

    def to_item(self) -> Item:
        pass  # TODO: implement this as book and stuff


AnyNumber = typing.Union[int, float]


class DFNumber:
    """
        Represents Minecraft Number variable.

        `Attributes`:
            value: The value of the number variable. Float.
        """
    __slots__ = ("_value", "value")
    _value: float

    def __init__(self, value: AnyNumber = 0.0):
        """
        Init number variable.
        :param value: Integer or float, defaults to 0
        """
        self.value = value

    @property
    def value(self) -> float:
        """
        The value of this number variable.
        :return: Float representing the value.
        """
        return self._value

    @value.setter
    def value(self, new_value: AnyNumber):
        """
        Set the value of this number variable.
        :param new_value: The new value.
        """
        self._value = float(new_value)

    def set(self, new_value: AnyNumber):
        """
        Set the value of this number variable.
        :param new_value: The new value.
        """
        self._value = float(new_value)

    def as_json_data(self) -> dict:
        """
        Obtain this variable represented as a JSON object (dict).
        :return: Dict.
        """
        return dict(
            id=constants.ITEM_ID_NUMBER_VAR,
            data=dict(
                name=str(self.value)
            )
        )

    def to_item(self) -> Item:
        pass  # TODO: implement this as slimeball and stuff


# TODO: Loc; Dynamic Var

DFType = typing.Union[Item, DFText, DFNumber]  # TODO: Add rest here

