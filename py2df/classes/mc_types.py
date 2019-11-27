import constants
import typing
import math
import re
import collections
import numpy as np
import json
from enums import Material
from .subcollections import Lore

DEFAULT_VAL = constants.DEFAULT_VAL


class Item:
    """
    Represents a Minecraft Item stack.
    """
    __slots__ = ("material", "_amount")

    # TODO - Material, quantity, multiplication override to set item stack amount, lore...
    def __init__(
            self, material: Material, amount: int = 1,
            *, lore: typing.Union[Lore, collections.Iterable] # TODO: more arguments
    ):
        pass

    @property
    def amount(self):
        return self._amount

    @amount.setter
    def amount(self, new_amt: int):
        i_n_amt = int(new_amt)
        if i_n_amt > constants.MAX_ITEM_STACK_SIZE:
            raise ValueError(f"Maximum item stack size is {constants.MAX_ITEM_STACK_SIZE}!")

        if i_n_amt < constants.MIN_ITEM_STACK_SIZE:
            raise ValueError(f"Minimum item stack size is {constants.MIN_ITEM_STACK_SIZE}!")

        self._amount = i_n_amt

    def as_json_data(self) -> dict:
        return dict(
            id=constants.ITEM_ID_ITEM,
            data=dict(
                item=json.dumps(dict(
                    id=self.material,  # TODO: DF_NBT = ???; Count = 1b -> is this the amount? Gotta test more
                ))
            )
        )

    def from_json_data(self) -> "Item":
        pass  # TODO

    def to_item(self) -> "Item":
        return self  #

    def copy(self) -> "Item":
        return Item(self.material, self.amount)

    def __eq__(self, other: "Item"):
        attrs_to_compare = set(self.__class__.__slots__) - {"_amount", }  # compare all except amount

        return type(self) == type(other) and all(
            getattr(self, attr) == getattr(other, attr) for attr in attrs_to_compare
        )

    def __ne__(self, other: "Item"):
        return not self.__eq__(other)

    def __gt__(self, other: "Item"):
        if self != other:
            raise TypeError("Cannot compare different items (must be equal)")

        return self.amount > other.amount

    def __ge__(self, other: "Item"):
        if self != other:
            raise TypeError("Cannot compare different items (must be equal)")

        return self.amount >= other.amount

    def __lt__(self, other: "Item"):
        if self != other:
            raise TypeError("Cannot compare different items (must be equal)")

        return self.amount < other.amount

    def __le__(self, other: "Item"):
        if self != other:
            raise TypeError("Cannot compare different items (must be equal)")

        return self.amount <= other.amount

    def __mul__(self, other: typing.Union[int, "Item"]):  # can be an Item if it is == to current instance.
        new = self.copy()
        new.amount *= other.amount if self == other else int(other)
        return new

    def __rmul__(self, other: typing.Union[int, "Item"]):
        return self.__mul__(other)

    def __add__(self, other: typing.Union[int, "Item"]):
        new = self.copy()
        new.amount += other.amount if self == other else int(other)
        return new

    def __radd__(self, other: typing.Union[int, "Item"]):
        return self.__add__(other)

    def __pow__(self, power: typing.Union[int, "Item"]):
        new = self.copy()
        new.amount **= power.amount if self == power else int(power)
        return new

    def __truediv__(self, other: typing.Union[int, "Item"]):  # always rounded.
        return self.__floordiv__(other)

    def __floordiv__(self, other: typing.Union[int, "Item"]):
        new = self.copy()
        new.amount //= other.amount if self == other else int(other)
        return new

    def __sub__(self, other: typing.Union[int, "Item"]):
        new = self.copy()
        new.amount -= other.amount if self == other else int(other)
        return new

    def __ceil__(self):
        return self

    def __floor__(self):
        return self

    def __abs__(self):
        return self

    def __pos__(self):
        return self


class DFText(collections.UserString):
    """
    Represents a DiamondFire Text variable. (note: this is not a dynamic variable.)

    Subclasses `collections.UserString`; therefore, supports all str operations.

    `Attributes`:
        data: The value of the text variable. String.

        convert_color: Whether or not should convert "&" to "§" (section sign) to allow easier color code writing.
            Defaults to True.
    """
    __slots__ = ("convert_color",)
    convert_color: bool

    def __init__(self, text: str = "", *, convert_color: bool = True):
        """
        Init text variable.

        :param text: Text, defaults to "" (empty str).
        :param convert_color: Boolean; whether or not should convert &x to color codes (§x). (Defaults to True)
        """
        super().__init__(text)
        self.data = text
        self.convert_color = bool(convert_color)

    def set(self, new_text: str):
        """
        Set the value of this text variable.

        :param new_text: The new text.
        """
        self.data = new_text

    def as_json_data(self) -> dict:
        """
        Obtain this variable represented as a JSON object (dict).

        :return: Dict.
        """
        converted_str: str = re.sub(
            constants.STR_COLOR_CODE_REGEX, constants.SECTION_SIGN + r"\1", self.data
        ) if self.convert_color else self.data  # convert color

        return dict(
            id=constants.ITEM_ID_TEXT_VAR,
            data=dict(
                name=converted_str
            )
        )

    @classmethod
    def from_json_data(cls, data: dict):
        """
        Obtain variable from pre-existing parsed JSON data.

        :param data: The parsed JSON dict.
        :return: DFText instance.
        """
        if (
            not isinstance(data, dict)
            # or "id" not in data  # not really required
            or "data" not in data
            or not isinstance(data["data"], dict)
            or "name" not in data["data"]
            or not type("name") == str
        ):
            raise TypeError(
                "Malformed DFText parsed JSON data! Must be a dict with, at least, a 'data' dict and a name str value."
            )

        return cls(data["data"]["name"])

    def to_item(self) -> Item:
        pass  # TODO: implement this as book and stuff

    def __repr__(self):
        return f"<{self.__class__.__name__} data='{self.data}'>"


AnyNumber = typing.Union[int, float]


class DFNumber:
    """
    Represents a DiamondFire Number variable.

    Supports practically all int/float-related operations and comparisons.

    `Attributes`:
        value: The value of the number variable. Float.
    """
    __slots__ = ("_value",)
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

    @classmethod
    def from_json_data(cls, data: dict):
        """
        Obtain variable from pre-existing parsed JSON data.
        :param data: The parsed JSON dict.
        :return: DFNumber instance.
        """
        if (
            not isinstance(data, dict)
            # or "id" not in data  # not really required
            or "data" not in data
            or not isinstance(data["data"], dict)
            or "name" not in data["data"]
            or not type("name") in (int, float, str)
        ):
            raise TypeError(
                "Malformed DFNumber parsed JSON data! Must be a dict with, at least, a 'data' dict and a name value."
            )

        return cls(float(data["data"]["name"]))

    def to_item(self) -> Item:
        pass  # TODO: implement this as slimeball and stuff

    @staticmethod
    def _extract_val(possible_num: typing.Union[int, float, "DFNumber"]):
        if isinstance(possible_num, DFNumber):
            return possible_num.value

        return possible_num

    def __repr__(self):
        return f"<{self.__class__.__name__} value={self.value}>"

    def __str__(self):
        return str(self.value)

    def __eq__(self, other):
        return type(self) == type(other) and self.value == other.value

    def __ne__(self, other):
        return not self.__eq__(other)

    def __gt__(self, other):
        return self.value > DFNumber._extract_val(other)

    def __ge__(self, other):
        return self.value >= DFNumber._extract_val(other)

    def __lt__(self, other):
        return self.value < DFNumber._extract_val(other)

    def __le__(self, other):
        return self.value <= DFNumber._extract_val(other)

    def __add__(self, other):
        return DFNumber(self.value + DFNumber._extract_val(other))

    def __radd__(self, other):
        return self.__add__(other)

    def __sub__(self, other):
        return DFNumber(self.value - DFNumber._extract_val(other))

    def __rsub__(self, other):
        return DFNumber((+other) - self.value)

    def __mul__(self, other):
        return DFNumber(self.value * DFNumber._extract_val(other))

    def __rmul__(self, other):
        return self.__mul__(other)

    def __mod__(self, other):
        return DFNumber(self.value % DFNumber._extract_val(other))

    def __rmod__(self, other):
        return other % self.value

    def __truediv__(self, other):
        return DFNumber(self.value / DFNumber._extract_val(other))

    def __floordiv__(self, other):
        return DFNumber(self.value // DFNumber._extract_val(other))

    def __pow__(self, power):
        return DFNumber(self.value ** DFNumber._extract_val(other))

    def __neg__(self):
        return DFNumber(-self.value)

    def __pos__(self):
        return self

    def __abs__(self):
        return DFNumber(abs(self.value))

    def __ceil__(self):
        return DFNumber(math.ceil(self.value))

    def __floor__(self):
        return DFNumber(math.floor(self.value))


class DFLocation:
    """
    Represents a DiamondFire Location.

    `Attributes`:
        x: The value of the x position (float).

        y: The value of the y position (float).

        z: The value of the z position (float).

        pitch: The pitch value (float).

        yaw: The yaw value (float).

        is_block: Whether or not this location represents a solid (non-air) block. (bool) Defaults to False.

        world_least: A constant int related to DF; this shouldn't need to be defined by the library user.

        world_most: A constant int related to DF; this shouldn't need to be defined by the library user.

    `Supported comparisons`:
        `a == b`: True if `a` and `b` have the same x,y,z,pitch,yaw, False if at least one is different.

        `a != b`: Negation of `a == b`.

        `a > b`: True if at least one of the coordinates x,y,z of a is bigger than the respective coordinate in b;
            False otherwise.

        `a < b`: True if at least one of the coordinates x,y,z of a is smaller than the respective coordinate in b;
            False otherwise.

        `a >= b`: Applies `>=` between each coordinate x,y,z of a and b.

        `a <= b`: Applies `<=` between each coordinate x,y,z of a and b.


    `Supported operations`: (Note: They are all applied in-place with given values, not dynamically in DiamondFire!)
        `a + b`: Adds two locations' x, y, z; pitch, yaw (mod 360 degrees). If `b` is an iterable (tuple, list etc.),
            then the respective items 0-4 are added as x,y,z;pitch,yaw. If `b` is an int/float, it is added to x,y,z.

        `a - b`: Follows same rules as addition, except that it is a subtraction.

        `a * b`: Again, same rules as addition, but multiplication.

        `a / b`: Same rules as addition, but division.

        `a // b`: Same rules as division, but floors.

        `a ** b`: Same rules as addition, but as exponentiation.

        `-a`: Applies -1 times x,y,z; pitch, yaw of a.

        `abs(a)`: Applies abs() to x,y,z,pitch,yaw of a.

        `+a`: Returns a.
    """
    __slots__ = ("x", "y", "z", "pitch", "yaw", "is_block", "world_least", "world_most")

    x: float
    y: float
    z: float
    pitch: float
    yaw: float
    is_block: bool
    world_least: typing.Optional[int]
    world_most: typing.Optional[int]

    def __init__(
        self, x: AnyNumber = 0.0, y: AnyNumber = 0.0, z: AnyNumber = 0.0, pitch: AnyNumber = 0.0,
        yaw: AnyNumber = 0.0,
        *, is_block: bool = False, world_least: typing.Optional[int] = None, world_most: typing.Optional[int] = None
    ):
        """
        Init the location.

        :param x: The value of the x position (float).
        :param y: The value of the y position (float).
        :param z: The value of the z position (float).
        :param pitch: The pitch value (float).
        :param yaw: The yaw value (float).
        :param is_block: Whether or not this location represents a solid (non-air) block. (bool) Defaults to False.
        :param world_least: A constant int related to DF; this shouldn't need to be defined by the library user. None
          to let the library handle it.
        :param world_most: A constant int related to DF; this shouldn't need to be defined by the library user. None
          to let the library handle it.
        """
        self.x = float(x)
        self.y = float(y)
        self.z = float(z)
        self.pitch = float(pitch)
        self.yaw = float(yaw)
        self.is_block = bool(is_block)
        self.world_least = None if world_least is None else int(world_least)
        self.world_most = None if world_most is None else int(world_most)

    def set(
        self, x: AnyNumber = DEFAULT_VAL, y: AnyNumber = DEFAULT_VAL, z: AnyNumber = DEFAULT_VAL,
        pitch: AnyNumber = DEFAULT_VAL, yaw: AnyNumber = DEFAULT_VAL,
        *, is_block: bool = DEFAULT_VAL,
        world_least: typing.Optional[int] = DEFAULT_VAL, world_most: typing.Optional[int] = DEFAULT_VAL
    ) -> "DFLocation":
        """
        Set the location.

        :param x: The value of the x position (float).
        :param y: The value of the y position (float).
        :param z: The value of the z position (float).
        :param pitch: The pitch value (float).
        :param yaw: The yaw value (float).
        :param is_block: Whether or not this location represents a solid (non-air) block. (bool) Defaults to False.
        :param world_least: A constant int related to DF; this shouldn't need to be defined by the library user. None
          to let the library handle it.
        :param world_most: A constant int related to DF; this shouldn't need to be defined by the library user. None
          to let the library handle it.
        :return: self to allow chaining
        """
        self.x = self.x if x == DEFAULT_VAL else float(x)
        self.y = self.y if y == DEFAULT_VAL else float(y)
        self.z = self.z if z == DEFAULT_VAL else float(z)
        self.pitch = self.pitch if pitch == DEFAULT_VAL else float(pitch)
        self.yaw = self.yaw if yaw == DEFAULT_VAL else float(yaw)
        self.is_block = self.is_block if is_block == DEFAULT_VAL else bool(is_block)
        self.world_least = self.world_least if world_least == DEFAULT_VAL else (
            None if world_least is None else int(world_least)
        )
        self.world_least = self.world_most if world_most == DEFAULT_VAL else (
            None if world_most is None else int(world_most)
        )

        return self

    def set_to_other(self, loc: "DFLocation") -> "DFLocation":
        """
        Imports another location's values into this one, making it identical.

        :param loc: Other location to set.
        :return: self
        """
        return self.set(
            loc.x, loc.y, loc.z, loc.pitch, loc.yaw, is_block=loc.is_block,
            world_least=loc.world_least, world_most=loc.world_most
        )

    def as_json_data(self) -> dict:
        """
        Obtain this location represented as a JSON object (dict).

        :return: Dict.
        """
        return dict(
            id=constants.ITEM_ID_LOCATION,
            data=dict(
                isBlock=self.is_block,
                x=self.x,
                y=self.y,
                z=self.z,
                pitch=self.pitch,
                yaw=self.yaw,
                worldLeast=constants.LOC_DEFAULT_WORLD_LEAST if self.world_least is None else int(self.world_least),
                worldMost=constants.LOC_DEFAULT_WORLD_MOST if self.world_most is None else int(self.world_most)
            )
        )

    @classmethod
    def from_json_data(cls, data: dict) -> "DFLocation":
        """
        Obtain variable from pre-existing parsed JSON data.

        :param data: The parsed JSON dict.
        :return: DFNumber instance.
        """
        required_attrs = ("x", "y", "z", "isBlock", "pitch", "yaw", "worldLeast", "worldMost")
        if (
                not isinstance(data, dict)
                # or "id" not in data
                or "data" not in data
                or not isinstance(data["data"], dict)
                or not all(attr in data["data"] for attr in required_attrs)
        ):
            raise TypeError(
                f"Malformed DFLocation parsed JSON data! Must be a dict with a 'data' dict including the \
                following attributes: {', '.join(required_attrs)}."
            )

        d_dict = data["data"]

        return cls(
            d_dict.x, d_dict.y, d_dict.z, d_dict.pitch, d_dict.yaw,
            is_block=d_dict.isBlock,
            world_least=None if int(d_dict.worldLeast) == constants.LOC_DEFAULT_WORLD_LEAST else d_dict.worldLeast,
            world_most=None if int(d_dict.worldMost) == constants.LOC_DEFAULT_WORLD_MOST else d_dict.worldMost
        )

    def copy(self):
        """
        Creates an identical copy of this location.
        :return: Copied location.
        """
        new_loc = DFLocation()
        new_loc.set_to_other(self)
        return new_loc

    def _exec_arithmetic(
        self, other: typing.Union[
            "DFLocation",
            typing.Iterable[typing.Optional[AnyNumber]],
            AnyNumber
        ], arithmetic: typing.Callable, *, op_name: str
    ):
        """
        Executes some arithmetic within the Location and returns a new one.

        :param other: The other DFLocation, an iterable with x,y,z,pitch,yaw (or None to keep),
            or a float that is distributed upon x,y,z.
        :param arithmetic: The function that executes the operation.
        :param op_name: The operation name, to be used in the Error message.
        :return: New DFLocation.
        :raises TypeError: Invalid type provided for arithmetic.
        """
        new_loc = self.copy()

        if type(other) == DFLocation:
            x, y, z, pitch, yaw = map(float, (other.x, other.y, other.z, other.pitch, other.yaw))

        elif isinstance(other, collections.Iterable):
            attr_list = [None] * 5  # initialize an empty array
            for i, value in enumerate(other):
                if i > len(attr_list) - 1:
                    break  # we don't need more values.

                attr_list[i] = value

            x, y, z, pitch, yaw = attr_list

        elif type(other) in (int, float):
            num = float(other)
            x, y, z = [num] * 3
            pitch, yaw = [None] * 2

        else:
            raise TypeError(f"Invalid type for DFLocation {op_name}: {type(other)}!")

        for attr, val in zip(("x", "y", "z"), (x, y, z)):
            if val is None:
                continue  # keep current value

            old_val = getattr(new_loc, attr)

            if op_name == "division" and old_val == val == 0:
                continue  # nope; division by zero

            setattr(new_loc, attr, float(arithmetic(float(old_val), float(val))))

        for mod_attr, val in zip(("pitch", "yaw"), (pitch, yaw)):  # gotta do this mod 360, they're rotation values.
            if val is None:
                continue  # keep current value

            old_val = getattr(new_loc, mod_attr)

            if op_name == "division" and old_val == val == 0:
                continue  # nope; division by zero

            result_val = float(
                arithmetic(float(old_val), float(val))
            )
            setattr(
                new_loc, mod_attr, np.sign(result_val) * (abs(result_val) % constants.MAX_DEGREES)
            )                                                       # mod 360 degrees, while keeping the sign (- or +).

        return new_loc

    def __eq__(self, other: "DFLocation") -> bool:
        """
        Check if this DFLocation is STRICTLY equal to another, except for world_least and world_most (which depend on
        the world).

        :param other: Other DFLocation to compare.
        :return: True if equal, False otherwise.
        """

        attrs_to_check = set(self.__class__.__slots__) - {"world_least", "world_most"}
        return type(self) == type(other) and all(getattr(self, attr) == getattr(other, attr) for attr in attrs_to_check)

    def __ne__(self, other: "DFLocation"):
        return not self.__eq__(other)

    def __gt__(self, other: "DFLocation") -> bool:
        """
        Checks if at least one of the coordinates of this location is higher than the other's.

        :param other: Other DFLocation to compare.
        :return: Bool.
        """
        positional_attrs = ("x", "y", "z")
        return any(getattr(self, attr) > getattr(other, attr) for attr in positional_attrs)

    def __ge__(self, other: "DFLocation") -> bool:
        """
        Checks if at least one of the coordinates of this location is higher than the other's, or if they are all
        equal.

        :param other: Other DFLocation to compare.
        :return: Bool.
        """
        positional_attrs = ("x", "y", "z")
        return all(getattr(self, attr) >= getattr(other, attr) for attr in positional_attrs)

    def __lt__(self, other: "DFLocation") -> bool:
        """
        Checks if at least one of the coordinates of this location is lower than the other's.

        :param other: Other DFLocation to compare.
        :return: Bool.
        """
        positional_attrs = ("x", "y", "z")
        return any(getattr(self, attr) < getattr(other, attr) for attr in positional_attrs)

    def __le__(self, other: "DFLocation") -> bool:
        """
        Checks if at least one of the coordinates of this location is lower than the other's, or if they are all equal.

        :param other: Other DFLocation to compare.
        :return: Bool.
        """
        positional_attrs = ("x", "y", "z")
        return all(getattr(self, attr) <= getattr(other, attr) for attr in positional_attrs)

    def __repr__(self):
        return f"<{self.__class__.__name__} x={self.x} y={self.y} z={self.z} pitch={self.pitch} yaw={self.yaw}>"

    def __str__(self):
        return str((self.x, self.y, self.z, self.pitch, self.yaw))

    def __getitem__(self, item: typing.Union[int, str, slice]):
        if item in self.__class__.__slots__:  # ["x"]
            return getattr(self, item)  # give them self.x

        positional_attrs = (self.x, self.y, self.z)
        return positional_attrs[item]  # [0] = x ; [1] = y ; [2] = z

    def __setitem__(self, key: typing.Union[int, str, slice], value: typing.Union[int, float]):
        fl_val = float(value)
        if key in self.__class__.__slots__:
            return setattr(self, key, fl_val)

        pos_attrs = ("x", "y", "z")
        attr_s_to_set = pos_attrs[key]
        if type(attr_s_to_set) == str:
            setattr(self, attr_s_to_set, fl_val)
        else:
            for attr_name in attr_s_to_set:
                setattr(self, attr_name, fl_val)

    def __iter__(self):
        for coord in (self.x, self.y, self.z):
            yield coord

    def __add__(
        self,
        other: typing.Union[
            "DFLocation",
            typing.Iterable[typing.Optional[AnyNumber]],
            AnyNumber
        ]
    ) -> "DFLocation":
        """
        Adds up the coordinates (x,y,z) of two locations and their respective pitches and yaws (mod 360).

        :param other: Other location to add to this one, an iterable with x,y,z, pitch, yaw, or a float that will
            be added to all of the x, y, z.
        :return: Added up location.
        """
        return self._exec_arithmetic(other, np.add, op_name="addition")

    def __radd__(
        self,
        other: typing.Union[
            "DFLocation",
            typing.Iterable[typing.Optional[AnyNumber]],
            AnyNumber
        ]
    ) -> "DFLocation":
        return self.__add__(other)

    def __sub__(
        self,
        other: typing.Union[
            "DFLocation",
            typing.Iterable[typing.Optional[AnyNumber]],
            AnyNumber
        ]
    ) -> "DFLocation":
        """
        Subtracts the coordinates (x,y,z) of two locations and their respective pitches and yaws (mod 360).

        :param other: Other location to subtract from this, an iterable x,y,z, pitch, yaw, or a float that will
            be subtracted from all of the x, y, z.
        :return: New location.
        """
        return self._exec_arithmetic(other, np.subtract, op_name="subtraction")

    def __rsub__(
        self,
        other: typing.Union[
            "DFLocation",
            typing.Iterable[typing.Optional[AnyNumber]],
            AnyNumber
        ]
    ) -> "DFLocation":
        return DFLocation.__add__(-self, other)

    def __mul__(
        self,
        other: typing.Union[
            "DFLocation",
            typing.Iterable[typing.Optional[AnyNumber]],
            AnyNumber
            ]
    ) -> "DFLocation":
        """
        Multiplies the coordinates (x,y,z) of two locations and their respective pitches and yaws (mod 360).

        :param other: Other location to multiply by this, an iterable x,y,z, pitch, yaw to mult., or a float that will
            multiply each of x, y, z.
        :return: New location.
        """
        return self._exec_arithmetic(other, np.multiply, op_name="multiplication")

    def __rmul__(
            self,
            other: typing.Union[
                "DFLocation",
                typing.Iterable[typing.Optional[AnyNumber]],
                AnyNumber
            ]
    ) -> "DFLocation":
        return self.__mul__(other)

    def __truediv__(
        self,
        other: typing.Union[
            "DFLocation",
            typing.Iterable[typing.Optional[AnyNumber]],
            AnyNumber
        ]
    ) -> "DFLocation":
        """
        Divides the coordinates (x,y,z) of one location from another and their respective pitches and yaws (mod 360).

        :param other: Other location to divide this, an iterable x,y,z, pitch, yaw to divide, or a float that will
            divide each of x, y, z.
        :return: New location.
        """
        return self._exec_arithmetic(other, np.true_divide, op_name="division")

    def __floordiv__(
        self,
        other: typing.Union[
            "DFLocation",
            typing.Iterable[typing.Optional[AnyNumber]],
            AnyNumber
        ]
    ) -> "DFLocation":
        """
        Divides the coordinates (x,y,z) of one location from another and their respective pitches and yaws (mod 360).

        :param other: Other location to divide this, an iterable x,y,z, pitch, yaw to divide, or a float that will
            divide each of x, y, z.
        :return: New location.
        """
        return self._exec_arithmetic(other, np.floor_divide, op_name="division")

    def __pow__(
        self,
        other: typing.Union[
            "DFLocation",
            typing.Iterable[typing.Optional[AnyNumber]],
            AnyNumber
            ]
    ) -> "DFLocation":
        """
        Powers the coordinates (x,y,z) of two locations and their respective pitches and yaws (mod 360).

        :param other: Other location as power this will be taken to, an iterable x,y,z, pitch, yaw to power this to,
            or a float that will be the power for each of x, y, z.
        :return: New location.
        """
        return self._exec_arithmetic(other, np.float_power, op_name="power")

    def __neg__(self):
        """
        Applies -1 • every single coordinate and pitch/yaw.

        :return: New location.
        """
        new_loc = self.copy()
        for attr in ("x", "y", "z", "pitch", "yaw"):
            setattr(new_loc, attr, -1 * (getattr(self, attr)))

        return new_loc

    def __pos__(self):
        return self

    def __abs__(self):
        """
        Returns abs() applied to every coordinate and pitch/yaw.

        :return: New location.
        """
        new_loc = self.copy()
        for attr in ("x", "y", "z", "pitch", "yaw"):
            setattr(new_loc, attr, abs(getattr(self, attr)))

        return new_loc

    def __ceil__(self):
        """
        Returns `math.ceil()` applied to every coordinate and pitch/yaw.

        :return: New location.
        """
        new_loc = self.copy()
        for attr in ("x", "y", "z", "pitch", "yaw"):
            setattr(new_loc, attr, float(math.ceil(getattr(self, attr))))

        return new_loc

    def __floor__(self):
        """
        Returns `math.floor()` applied to every coordinate and pitch/yaw.

        :return: New location.
        """
        new_loc = self.copy()
        for attr in ("x", "y", "z", "pitch", "yaw"):
            setattr(new_loc, attr, float(math.floor(getattr(self, attr))))

        return new_loc

# TODO: Loc; Dynamic Var


DFType = typing.Union[Item, DFText, DFNumber, DFLocation]  # TODO: Add rest here

