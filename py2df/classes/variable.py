import collections
import typing

from ..constants import SMALL_CHEST_SIZE
from .abc import DFType
from .mc_types import DFText
from .collections import Arguments
from .dataclass import Tag
from ..utils import remove_u200b_from_doc, flatten
from ..enums import SetVarType, VariableScope, BlockType
from ..constants import ITEM_ID_DYNAMIC_VAR, DEFAULT_VAL
from ..errors import LimitReachedError

if typing.TYPE_CHECKING:
    from .. import typings as _tp
    from ..codeblocks.utilityblock import SetVar  # lazy import in Var init
    from ..typings import Param, Numeric, Locatable


_VarOpEl = typing.Union["Numeric", "DFVariable", "Locatable"]


class VarOp:  # TODO: fix doc to include numeric; locatable
    """Represents an operation between 2+ variables. Note that they are applied within DiamondFire, using a SetVar
    block. Use this as the parameter of :meth:`DFVariable.set`.

    Parameters
    ----------\u200b
    setv_type : :class:`~.SetVarType`
        The type of :class:`~.SetVar` that this operation will produce.

    vars : Union[:class:`DFVariable`, Iterable[:class:`DFVariable`]]
        Variables that participate in this operation.

    tags : Iterable[:class:`~.Tag`]
        Any tags used in this operation's set var block.

    Warnings
    --------
    Instantiating this is only done internally; to obtain this class, realize operations between variables.

    Attributes
    ----------\u200b
    setv_type : :class:`~.SetVarType`
        The type of :class:`~.SetVar` that this operation will produce.

    vars : List[:class:`DFVariable`]
        Variables that participate in this operation.

    tags : List[:class:`~.Tag`]
        Any tags used in this operation's set var block.
    """
    __slots__ = ("setv_type", "vars", "tags")

    setv_type: SetVarType
    vars: typing.List[_VarOpEl]
    tags: typing.List[Tag]

    def __init__(
        self, setv_type: SetVarType, *vars: typing.Union[_VarOpEl, typing.Iterable[_VarOpEl]],
        tags: typing.Iterable[Tag] = tuple()
    ):
        self.setv_type = SetVarType(setv_type)
        self.vars = flatten(vars, except_iterables=[], max_depth=1)
        self.tags = list(tags)

    def _add_var(self, var: typing.Union["DFVariable", "VarOp"], op: SetVarType):
        """Adds a variable to participate in this operation.

        Parameters
        ----------
        var : Union[:class:`DFVariable`, :class:`VarOp`, :attr:`~.Numeric`]
            The variable(s) to add.

        op : :class:`~.SetVarType`
            The operation that was done, in order to check for mismatches/mixed ops.

        Returns
        -------
        ``None``
            ``None``

        Raises
        ------
        :exc:`~.LimitReachedError`
            If there was an attempt to execute an operation between more variables than a chest can contain.
        """
        if (
            op != self.setv_type
                or (
                    isinstance(var, VarOp)
                    and (
                        var.setv_type != self.setv_type
                        or var.setv_type != op
                    )
                )
        ):
            raise TypeError("Cannot have different types of operations between variables at the same time.")

        if (
            not isinstance(var, (DFVariable, VarOp))  # not a variable; or
                and not _tp.p_bool_check(var, _tp.Numeric)  # not a number
                and (
                    not _tp.p_bool_check(var, _tp.Locatable)  # + and - can also accept locations
                    if op in (SetVarType.SET_TO_ADDITION, SetVarType.SET_TO_SUBTRACTION) else True
                )
        ):
            return NotImplemented

        if len(self.vars) >= SMALL_CHEST_SIZE:
            raise LimitReachedError(f"Cannot execute an operation between more than {SMALL_CHEST_SIZE} vars.")

        self.vars.append(var)

        return self

    def __iter__(self):
        for x in self.vars:
            yield x

    def __add__(self, other: typing.Union["Numeric", "Locatable"]):
        return self._add_var(other, SetVarType.SET_TO_ADDITION)

    def __sub__(self, other: typing.Union["Numeric", "Locatable"]):
        return self._add_var(other, SetVarType.SET_TO_SUBTRACTION)

    def __mul__(self, other: "Numeric"):
        return self._add_var(other, SetVarType.SET_TO_PRODUCT)

    def __pow__(self, power: "Numeric", modulo=None):
        return self._add_var(power, SetVarType.SET_TO_POWER)

    def __mod__(self, other: "Numeric"):
        return self._add_var(other, SetVarType.SET_TO_MOD)

    def __truediv__(self, other: "Numeric"):
        return self._add_var(other, SetVarType.SET_TO_QUOTIENT)
        # [Tag("Divison Mode", option="Default", action=SetVarType.SET_TO_QUOTIENT, block=BlockType.SET_VAR)]

    def __floordiv__(self, other: "Numeric"):
        return self._add_var(other, SetVarType.SET_TO_QUOTIENT)
        # [Tag("Divison Mode", option="Round to Integer", action=SetVarType.SET_TO_QUOTIENT, block=BlockType.SET_VAR)]


class DFVariable(DFType):
    """Represents a DiamondFire variable. **Note that all variables with same 'name' attribute represent the same
    var.**

    Parameters
    ----------\u200b
    name : :class:`str`
        The name of this variable. This uniquely identifies it, along with its scope.

    init_value : Optional[:attr:`~.Param`], optional
        An optional value for this variable. **WARNING: This will create a Set Var '=' block.** (This simply
        invokes :meth:`Variable.set`.) Defaults to ``None`` (i.e., doesn't set a value).

    scope : :class:`~.VariableScope`, optional
        The scope of this variable. This can also be set through the kwargs ``unsaved``, ``saved`` and ``local`` .
        Defaults to :attr:`~.VariableScope.UNSAVED`.

    unsaved : :class:`bool`, optional
        If ``True``, the variable's scope is set to :attr:`~.VariableScope.UNSAVED` - i.e., the value does not persist
        between successive plot uses (when the amount of players reaches 0, the variable is reset).


    """
    __slots__ = ("name", "scope")

    name: str
    scope: VariableScope

    def __init__(
        self, name: typing.Union[str, DFText], init_value: typing.Optional["Param"] = None,
        *, scope: VariableScope = DEFAULT_VAL, unsaved: bool = True,
        saved: bool = False, local: bool = False
    ):
        global _SetVar, _tp
        from ..codeblocks.utilityblock import SetVar  # lazy import to avoid cyclic imports
        from .. import typings                # ^

        self.name: str = str(name)

        if scope != DEFAULT_VAL:
            self.scope: VariableScope = VariableScope(scope)
        elif unsaved:
            self.scope: VariableScope = VariableScope.UNSAVED
        elif saved:
            self.scope: VariableScope = VariableScope.SAVED
        elif local:
            self.scope: VariableScope = VariableScope.LOCAL

        _SetVar = SetVar
        _tp = typings

        if init_value:
            self.set(init_value)

    def set(self, value: "Param") -> "SetVar":
        """
        Set this variable. Note that this simply creates a Set Var block and returns it.

        Parameters
        ----------
        value : :attr:`~.Param`
            The value. Can be of any type.

        Returns
        -------
        :class:`~.SetVar`
            The generated SetVar block.
        """
        setv_type = SetVarType.SET_TO
        args: Arguments
        if isinstance(value, VarOp):
            setv_type = SetVarType(value.setv_type)
            args = Arguments([])

        return SetVar(
            action=SetVarType.SET_TO,
            args=Arguments([_tp.p_check(value, Param)]),
            append_to_reader=True
        )

    def as_json_data(self) -> dict:
        return dict(
            id=ITEM_ID_DYNAMIC_VAR,
            data=dict(
                name=self.name,
                scope=self.scope.value
            )
        )

    @classmethod
    def from_json_data(cls, data: dict) -> "DFVariable":
        """Obtain a DFVariable from pre-existing parsed JSON data (as a dict).

        Must have, at least, the following keys with the following format::

            { "data": { "name": str, "scope": str } }

        Parameters
        ----------
        data : :class:`dict`
            The parsed JSON :class:`dict`.


        Returns
        -------
        :class:`DFVariable`
            :class:`DFVariable` instance.

        """
        if (
            not isinstance(data, dict)
            # or "id" not in data  # not really required
            or "data" not in data
            or not isinstance(data["data"], dict)
            or "name" not in data["data"]
            or type(data["data"]["name"]) != str
            or "scope" not in data["scope"]
            or type(data["data"]["scope"]) != str
        ):
            raise TypeError(
                "Malformed Variable parsed JSON data! Must be a dict with, at least, a 'data' dict and 'name' and"
                "'scope' str values."
            )

        return cls(data["data"]["name"], scope=VariableScope(data["data"]["scope"]))

    # region:var_ops

    def __add__(self, other):
        if not isinstance(other, (DFVariable, VarOp)) and not _tp.p_bool_check(
            other, typing.Union[_tp.Numeric, _tp.Locatable]
        ):
            return NotImplemented

        return VarOp(SetVarType.SET_TO_ADDITION, other)

    def __sub__(self, other):
        if not isinstance(other, (DFVariable, VarOp)) and not _tp.p_bool_check(
            other, typing.Union[_tp.Numeric, _tp.Locatable]
        ):
            return NotImplemented

        return VarOp(SetVarType.SET_TO_SUBTRACTION, other)

    def __mul__(self, other):
        if not isinstance(other, (DFVariable, VarOp)) and not _tp.p_bool_check(other, _tp.Numeric):
            return NotImplemented

        return VarOp(SetVarType.SET_TO_PRODUCT, other)

    def __pow__(self, power, modulo=None):
        if not isinstance(power, (DFVariable, VarOp)) and not _tp.p_bool_check(power, _tp.Numeric):
            return NotImplemented

        return VarOp(SetVarType.SET_TO_POWER, power)

    def __mod__(self, other):  # TODO: 2 params stuffffff
        if not isinstance(other, DFVariable) and not _tp.p_bool_check(other, _tp.Numeric):
            return NotImplemented

        return VarOp(SetVarType.SET_TO_MOD, other)

    def __truediv__(self, other):
        if not isinstance(other, (DFVariable, VarOp)) and not _tp.p_bool_check(other, _tp.Numeric):
            return NotImplemented

        return VarOp(
            SetVarType.SET_TO_QUOTIENT, other,
            tags=[Tag("Divison Mode", option="Default", action=SetVarType.SET_TO_QUOTIENT, block=BlockType.SET_VAR)]
        )

    def __floordiv__(self, other):
        if not isinstance(other, (DFVariable, VarOp)) and not _tp.p_bool_check(other, _tp.Numeric):
            return NotImplemented

        return VarOp(
            SetVarType.SET_TO_QUOTIENT, other,
            tags=[Tag(
                "Divison Mode", option="Round to Integer", action=SetVarType.SET_TO_QUOTIENT, block=BlockType.SET_VAR
            )]
        )

    def __iadd__(self, other):
        if not isinstance(other, (DFVariable, VarOp)) and not _tp.p_bool_check(other, _tp.Numeric):
            return NotImplemented

        return SetVar(
            action=SetVarType.ADD,
            args=Arguments(
                [_tp.p_check(o, _tp.Numeric) for o in other.vars] if isinstance(other, VarOp) else [
                    _tp.p_check(other, _tp.Numeric)
                ]
            ),
            append_to_reader=True
        )

    def __isub__(self, other):
        if not isinstance(other, (DFVariable, VarOp)) and not _tp.p_bool_check(other, _tp.Numeric):
            return NotImplemented

        return SetVar(
            action=SetVarType.SUBTRACT,
            args=Arguments(
                [_tp.p_check(o, _tp.Numeric) for o in other.vars] if isinstance(other, VarOp) else [
                    _tp.p_check(other, _tp.Numeric)
                ]
            ),
            append_to_reader=True
        )

    def __imul__(self, other):
        return self.set(self.__mul__(other))

    def __ipow__(self, power, modulo=None):
        return self.set(self.__pow__(other))

    def __imod__(self, other):
        return self.set(self.__mod__(other))

    def __itruediv__(self, other):
        return self.set(self.__truediv__(other))
        # [Tag("Divison Mode", option="Default", action=SetVarType.SET_TO_QUOTIENT, block=BlockType.SET_VAR)]

    def __ifloordiv__(self, other):
        return self.set(self.__floordiv__(other))
        # [Tag("Divison Mode", option="Round to Integer", action=SetVarType.SET_TO_QUOTIENT, block=BlockType.SET_VAR)]

    # endregion:var_ops


remove_u200b_from_doc(DFVariable, VarOp)
