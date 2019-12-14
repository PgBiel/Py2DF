import abc
import collections
import typing
import json

from collections import deque

from .. import constants
from ..constants import SMALL_CHEST_SIZE
from .abc import DFType
from .mc_types import DFText
from .collections import Arguments
from .dataclass import Tag
from ..utils import remove_u200b_from_doc, flatten, TrueLiteral, FalseLiteral, all_attr_eq
from ..enums import SetVarType, VariableScope, BlockType, IfVariableType, PlayerTarget, EntityTarget, GameValueType, \
    Target, IfVItemEqComparisonMode
from ..constants import ITEM_ID_DYNAMIC_VAR, DEFAULT_VAL
from ..errors import LimitReachedError

if typing.TYPE_CHECKING:
    from .. import typings as _tp
    from ..codeblocks.ifs import IfVariable, IfVariable as _IfVariable
    from ..codeblocks.utilityblock import SetVar  # lazy import in Var init
    from ..typings import Param, Numeric, Locatable, Textable, Listable, ItemParam


_VarOpEl = typing.Union["Numeric", "DFVariable", "Locatable", "VarOp"]

op_to_expr = {
    SetVarType.SET_TO: "=",
    SetVarType.SET_TO_ADDITION: "+",
    SetVarType.SET_TO_SUBTRACTION: "-",
    SetVarType.SET_TO_QUOTIENT: "/",
    SetVarType.SET_TO_MOD: "%",
    SetVarType.SET_TO_POWER: "**",
    SetVarType.SET_TO_PRODUCT: "*"
}


def _heavy_imports() -> bool:
    global _SetVar, _tp, _IfVariable
    try:
        _a = _SetVar
        _b = _tp
        _c = _IfVariable

        return False

    except NameError:
        from ..codeblocks.utilityblock import SetVar  # lazy import to avoid cyclic imports
        from .. import typings  # ^
        from ..codeblocks.ifs import IfVariable  # ^

        _SetVar = SetVar
        _tp = typings
        _IfVariable = IfVariable

        return True


class VarOp:
    """Represents an operation between 2+ variables. Note that they are applied within DiamondFire, using a SetVar
    block. Use this as the parameter of :meth:`DFVariable.set`.

    Parameters
    ----------\u200b
    setv_type : :class:`~.SetVarType`
        The type of :class:`~.SetVar` that this operation will produce.

    vars : Union[Union[:attr:`~.Numeric`, :attr:`~.Locatable`, :class:`VarOp`], \
Iterable[:attr:`~.Numeric`, :attr:`~.Locatable`, :class:`VarOp`]]
        Variables that participate in this operation. One of Numeric, Locatable or VarOp. (Any iterables will be
        flattened.)

        .. note::

            The variables can only be a Locatable (i.e., a Location) alongside with Numeric if the operation in
            question is **addition** (+) or **subtraction** (-); otherwise, it can only be a param of Numeric type.

    tags : Iterable[:class:`~.Tag`]
        All tags used in this operation's set var block (if any). At the moment, this is only used for division.

    Warnings
    --------
    Instantiation of this class is only done internally; to obtain an instance, realize operations between variables.


    .. container:: operations

        .. describe:: a + b, a - b, a * b, a ** b, a / b, a // b, a % b

            Adds `b`, of :attr:`~.Numeric` type, to the list of variables that partake in this operation.

            .. warning::

                **You cannot mix operations.** For example, ``a + b - c * d ** e`` will raise. Stick to only one
                at once, and have one :meth:`set` call for each kind. (There is only one Set Var for each kind.)
                (However, operations with multiple variables, up to 27, work: ``a + b + c + ... + z``)

                If there is an attempt to mix operations, a :exc:`TypeError` is raised.

                Similarly, if there is an attempt to have an operation with more than 26 variables (chest size is
                up to 27 items, while 1 slot is the variable being set), then a :exc:`~.LimitReachedError` is raised
                instead.

            .. note::
                If the operation is addition or subtraction, `b` can also be a :attr:`~.Locatable` parameter (represent
                a location), besides Numeric.

    Attributes
    ----------\u200b
    setv_type : :class:`~.SetVarType`
        The type of :class:`~.SetVar` that this operation will produce.

    vars : Deque[Union[:attr:`~.Numeric`, :attr:`~.Locatable`]]
        Variables that participate in this operation.

    tags : List[:class:`~.Tag`]
        Any tags used in this operation's set var block.
    """
    __slots__ = ("setv_type", "vars", "tags")

    setv_type: SetVarType
    vars: typing.Deque[_VarOpEl]
    tags: typing.List[Tag]

    def __init__(
        self, setv_type: SetVarType, *vars: typing.Union[_VarOpEl, typing.Iterable[_VarOpEl]],
        tags: typing.Iterable[Tag] = tuple()
    ):
        _heavy_imports()
        self.setv_type = SetVarType(setv_type)

        self.tags = list(tags)

        valid_types = typing.Union[_tp.Numeric, _tp.Locatable] if setv_type in (
            SetVarType.SET_TO_ADDITION, SetVarType.SET_TO_SUBTRACTION
        ) else _tp.Numeric

        if any(map(lambda v_op: v_op.setv_type != setv_type, filter(lambda o: isinstance(o, VarOp), vars))):
            raise TypeError(
                "Cannot have different types of operations between variables at the same time; each kind "
                "should be evaluated in its own .set()."
            )  # different kind of operation found.

        self.vars = deque(_tp.p_check(o, valid_types) for o in flatten(vars, except_iterables=[str], max_depth=2))

    @typing.overload
    def _add_var(
        self, var: typing.Iterable[_VarOpEl], op: SetVarType,
        *, append_left: bool = False, is_rsub: bool = False, allow_other_iters: TrueLiteral,
        error_incompatible: bool = False, modify_self: bool = False
    ) -> typing.List["VarOp"]: ...

    @typing.overload
    def _add_var(
        self, var: _VarOpEl, op: SetVarType,
        *, append_left: bool = False, is_rsub: bool = False, allow_other_iters: bool = False,
        error_incompatible: bool = False, modify_self: bool = False
    ) -> "VarOp": ...

    def _add_var(
        self, var: typing.Union[_VarOpEl, typing.Iterable[_VarOpEl]], op: SetVarType,
        *, append_left: bool = False, is_rsub: bool = False, allow_other_iters: bool = False,
        error_incompatible: bool = False, modify_self: bool = False
    ) -> typing.Union["VarOp", typing.List["VarOp"]]:
        """Adds a variable to participate in this operation.

        Parameters
        ----------
        var : Union[:class:`DFVariable`, :class:`VarOp`, :attr:`~.Numeric`]
            The variable(s) to add.

        op : :class:`~.SetVarType`
            The operation that was done, in order to check for mismatches/mixed ops.

        append_left : :class:`bool`, optional
            If the variable(s) should, instead, be appended to the left. Used in __rsub__. Defaults to ``False``.

        is_rsub : :class:`bool`, optional
            If this is an __rsub__ operation, for more specific type checks. Defaults to ``False``.

        allow_other_iters : :class:`bool`, optional
            If iterables other than VarOp should be accepted. Defaults to ``False``.

        error_incompatible : :class:`bool`, optional
            If `self` should be modified instead of generating a new VarOp. Defaults to ``False``.

        Returns
        -------
        ``None``
            ``None``

        Raises
        ------
        :exc:`~.LimitReachedError`
            If there was an attempt to execute an operation between more variables than a chest can contain.

        :exc:`~.TypeError`
            Either if there was an attempt to mix operations (e.g. A + B * C) or if ``error_incompatible=True`` and
            an invalid Numeric/Locatable was given.
        """
        if (
            not isinstance(var, (DFVariable, VarOp))  # not a variable; or
                and not _tp.p_bool_check(var, _tp.Numeric)  # not a number
                and (
                    not _tp.p_bool_check(var, _tp.Locatable)  # + and - can also accept locations
                    if op in (SetVarType.SET_TO_ADDITION, SetVarType.SET_TO_SUBTRACTION) else True
                )
        ):
            if allow_other_iters and isinstance(var, collections.Iterable):
                return [
                    self._add_var(v, op, append_left=append_left, is_rsub=is_rsub, allow_other_iters=True)
                    for v in var
                ]
            else:
                if error_incompatible:
                    raise TypeError(f"Cannot realize variable operation with '{type(var)}'")
                return NotImplemented

        own_type = self.setv_type
        valid_rsub_ops = (SetVarType.SET_TO_ADDITION, SetVarType.SET_TO_SUBTRACTION)
        inverted_own_type = SetVarType.SET_TO_ADDITION if own_type == SetVarType.SET_TO_SUBTRACTION \
            else SetVarType.SET_TO_SUBTRACTION

        if (
            (  # if this is a __rsub__ and the current op is not an addition/subtraction...
                is_rsub and (
                    own_type not in valid_rsub_ops
                    or isinstance(var, VarOp) and (
                        var.setv_type not in valid_rsub_ops
                        or var.setv_type != inverted_own_type
                    )
                )
            )
            or not is_rsub and (  # or it isn't and we are trying to mix types...
                op != own_type
                or (
                    isinstance(var, VarOp)
                    and (
                        var.setv_type != own_type
                        or var.setv_type != op
                    )
                )
            )
        ):
            raise TypeError(
                "Cannot have different types of operations between variables at the same time; each kind "
                "should be evaluated in its own .set()."
            )

        vars = self.vars if modify_self else self.vars.copy()

        if len(vars) >= (SMALL_CHEST_SIZE - 1):  # There's also the variable that is going to be set, so -1
            raise LimitReachedError(f"Cannot execute an operation between more than {SMALL_CHEST_SIZE - 1} vars.")

        if isinstance(var, collections.Iterable):
            if append_left:
                vars.extendleft(var)
            else:
                vars.extend(var)
        else:
            if append_left:
                vars.appendleft(var)
            else:
                vars.append(var)

        return self if modify_self else VarOp(inverted_own_type if is_rsub else self.setv_type, vars, tags=self.tags)

    def __iter__(self):
        for x in self.vars:
            yield x

    def __repr__(self):
        return f"<{self.__class__.__name__}: {f' {op_to_expr[self.setv_type]} '.join(map(repr, self.vars))}>"

    def __str__(self):
        return f" {op_to_expr[self.setv_type]} ".join(map(str, self.vars))

    def __add__(self, other: typing.Union["Numeric", "Locatable", "VarOp"]) -> "VarOp":
        return self._add_var(other, SetVarType.SET_TO_ADDITION)

    def __radd__(self, other: typing.Union["Numeric", "Locatable", "VarOp"]) -> "VarOp":
        return self.__add__(other)

    def __sub__(self, other: typing.Union["Numeric", "Locatable", "VarOp"]) -> "VarOp":
        return self._add_var(other, SetVarType.SET_TO_SUBTRACTION)

    def __rsub__(self, other: typing.Union["Numeric", "Locatable", "VarOp"]) -> "VarOp":
        return self._add_var(other, SetVarType.SET_TO_SUBTRACTION, append_left=True, is_rsub=True)

    def __mul__(self, other: typing.Union["Numeric", "VarOp"]) -> "VarOp":
        return self._add_var(other, SetVarType.SET_TO_PRODUCT)

    def __rmul__(self, other: typing.Union["Numeric", "VarOp"]) -> "VarOp":
        return self.__mul__(other)

    def __pow__(self, power: typing.Union["Numeric", "VarOp"], modulo=None) -> "VarOp":
        if len(self.vars) >= 2:
            raise LimitReachedError("Cannot realize operation '**' between more than two variables.")

        return self._add_var(power, SetVarType.SET_TO_POWER)

    def __mod__(self, other: typing.Union["Numeric", "VarOp"]) -> "VarOp":
        if len(self.vars) >= 2:
            raise LimitReachedError("Cannot realize operation '%' between more than two variables.")

        return self._add_var(other, SetVarType.SET_TO_MOD)

    def __truediv__(self, other: typing.Union["Numeric", "VarOp"]) -> "VarOp":
        return self._add_var(other, SetVarType.SET_TO_QUOTIENT)
        # [Tag("Divison Mode", option="Default", action=SetVarType.SET_TO_QUOTIENT, block=BlockType.SET_VAR)]

    def __floordiv__(self, other: typing.Union["Numeric", "VarOp"]) -> "VarOp":
        return self._add_var(other, SetVarType.SET_TO_QUOTIENT)
        # [Tag("Divison Mode", option="Round to Integer", action=SetVarType.SET_TO_QUOTIENT, block=BlockType.SET_VAR)]


class VarOperable(metaclass=abc.ABCMeta):
    """An ABC for classes that support variable-related operations (i.e., :class:`DFGameValue` and :class:`DFVariable`).

    This class is used to hold operations and functions that are common to :class:`DFGameValue` and :class:`DFVariable`.
    Note that each implement their own operations as well; see the documentation for each.

    Implements all the If Variable humanized methods.

    .. container:: comparisons

        .. describe:: a == b, a != b

            Returns the equivalent :class:`~.IfVariable` block for equals/not equals. Has two uses:

            1. **Is used to compare the variables with an If Var.** Example usage::

                with var_a == var_b:
                    # code that is only executed in DiamondFire if 'var_a' and 'var_b' are equal in value.

                with var_c != var_d:
                    # code that is only executed in DiamondFire if 'var_c' and 'var_d' are different in value.

            2. **Is used to compare, IN PYTHON, the variables' attributes** (by calling :func:`bool` on the \
            generated IfVariable block). Note that DFGameValue and DFVariable implement this differently; see their
            respective documentations.

        .. describe:: a > b, a >= b, a < b, a <= b

            Returns the equivalent :class:`~.IfVariable` block for the given comparison. **Its only usage is as
            a Codeblock** (in a `with`).
            For example::

                with var_a > var_b:
                    # code that is only executed in DiamondFire if 'var_a' is bigger than 'var_b' in value.

                with var_c < var_d:
                    # code that is only executed in DiamondFire if 'var_c' is less than 'var_d' in value.

            .. note::

                Those comparisons are not usable in Python if's; if a :func:`bool` is attempted on the resulting
                IfVariable block, it will always return True. This mechanism is only implemented for ``==`` and ``!=``.

            .. warning::

                Assuming that one of them is a DFVariable, the other has to be a valid :attr:`~.Numeric` parameter.
                Otherwise, a TypeError may be raised (if the given type does not support operations with DFVariable,
                which is likely).


    .. container:: operations

        .. describe:: a + b, a - b, a * b, a ** b, a / b, a // b, a % b

            Creates a :class:`VarOp` instance representing this operation between different variables/variables
            and values/etc.
            It is meant to be given as the parameter for :meth:`DFVariable.set`, which will then place the appropriate
            Set Variable type (setting the variable instance to this operation)

            `a` is the :class:`VarOperable` instance, while `b`, in this case, is the :attr:`~.Numeric` to realize this
            operation with.

            .. note::

                If the operation is addition or subtraction, `b` can also be a :attr:`~.Locatable` parameter (represent
                a location), besides Numeric.

            .. warning::

                **You cannot mix operations.** For example, ``a + b - c * d ** e`` will raise. Stick to only one
                at once, and have one :meth:`DFVariable.set` call for each kind.
                (There is only one Set Var for each kind.)
                (However, operations with multiple variables, up to 27, work: ``a + b + c + ... + z``)

                If there is an attempt to mix operations, a :exc:`TypeError` is raised.

                Similarly, if there is an attempt to have an operation with more than 26 variables (chest size is
                up to 27 items, while 1 slot is the variable being set), then a :exc:`~.LimitReachedError` is raised
                instead.
    """

    def __new__(cls, *args, **kwargs):
        _heavy_imports()
        return object.__new__(cls)

    # region:var_comparison

    def __eq__(self, other: "Param") -> "IfVariable":
        if not _tp.p_bool_check(other, _tp.Param):
            return NotImplemented

        gen_if = _IfVariable(  # allow "with var_a == var_b:"
            action=IfVariableType.EQUALS,
            args=Arguments([self, _tp.p_check(other, _tp.Param, "other")]),
            append_to_reader=False
        )
        gen_if._called_by_var = True  # allow "if var_a == var_b"

        return gen_if

    def __ne__(self, other: "Param") -> "IfVariable":
        if not _tp.p_bool_check(other, _tp.Param):
            return NotImplemented

        gen_if = _IfVariable(  # allow "with var_a != var_b:"
            action=IfVariableType.NOT_EQUALS,
            args=Arguments([self, _tp.p_check(other, _tp.Param, "other")]),
            append_to_reader=False
        )
        gen_if._called_by_var = True  # allow "if var_a != var_b"

        return gen_if

    def __gt__(self, other: "Numeric") -> "IfVariable":
        if not _tp.p_bool_check(other, _tp.Numeric, error_on_gameval=True):
            return NotImplemented

        return _IfVariable(
            action=IfVariableType.GREATER_THAN,
            args=Arguments([self, _tp.p_check(other, _tp.Numeric, "other")]),
            append_to_reader=False
        )

    def __ge__(self, other: "Numeric") -> "IfVariable":
        if not _tp.p_bool_check(other, _tp.Numeric, error_on_gameval=True):
            return NotImplemented

        return _IfVariable(
            action=IfVariableType.GREATER_THAN_OR_EQUAL_TO,
            args=Arguments([self, _tp.p_check(other, _tp.Param, "other")]),
            append_to_reader=False
        )

    def __lt__(self, other: "Numeric") -> "IfVariable":
        if not _tp.p_bool_check(other, _tp.Numeric, error_on_gameval=True):
            return NotImplemented

        return _IfVariable(
            action=IfVariableType.LESS_THAN,
            args=Arguments([self, _tp.p_check(other, _tp.Numeric, "other")]),
            append_to_reader=False
        )

    def __le__(self, other: "Numeric") -> "IfVariable":
        if not _tp.p_bool_check(other, _tp.Numeric, error_on_gameval=True):
            return NotImplemented

        return _IfVariable(
            action=IfVariableType.LESS_THAN_OR_EQUAL_TO,
            args=Arguments([self, _tp.p_check(other, _tp.Numeric, "other")]),
            append_to_reader=False
        )

    # endregion:var_comparison

    # region:var_ops

    def __add__(self, other: typing.Union["Numeric", "Locatable", VarOp, "DFVariable"]):

        if not isinstance(other, (DFVariable, VarOp)) and not _tp.p_bool_check(
            other, typing.Union[_tp.Numeric, _tp.Locatable], error_on_gameval=True
        ):
            return NotImplemented

        return VarOp(SetVarType.SET_TO_ADDITION, self, other)

    def __radd__(self, other: typing.Union["Numeric", "Locatable", VarOp, "DFVariable"]):
        return self.__add__(other)

    def __sub__(self, other: typing.Union["Numeric", "Locatable", VarOp, "DFVariable"]):
        if not isinstance(other, (DFVariable, VarOp)) and not _tp.p_bool_check(
            other, typing.Union[_tp.Numeric, _tp.Locatable], error_on_gameval=True
        ):
            return NotImplemented

        return VarOp(SetVarType.SET_TO_SUBTRACTION, self, other)

    def __rsub__(self, other: typing.Union["Numeric", "Locatable", VarOp, "DFVariable"]):
        if not isinstance(other, (DFVariable, VarOp)) and not _tp.p_bool_check(
            other, typing.Union[_tp.Numeric, _tp.Locatable], error_on_gameval=True
        ):
            return NotImplemented

        res = VarOp(SetVarType.SET_TO_SUBTRACTION, self)
        res._add_var(
            other, SetVarType.SET_TO_SUBTRACTION, append_left=True, is_rsub=True, allow_other_iters=False,
            error_incompatible=True, modify_self=True
        )

    def __mul__(self, other: typing.Union["Numeric", VarOp, "DFVariable"]):
        if not isinstance(other, (DFVariable, VarOp)) and not _tp.p_bool_check(
            other, _tp.Numeric, error_on_gameval=True
        ):
            return NotImplemented

        return VarOp(SetVarType.SET_TO_PRODUCT, self, other)

    def __rmul__(self, other: typing.Union["Numeric", VarOp, "DFVariable"]) -> VarOp:
        return self.__mul__(other)

    def __pow__(self, power: typing.Union["Numeric", VarOp, "DFVariable"], modulo=None) -> VarOp:
        if isinstance(power, VarOp):
            vars = power.vars
            if len(vars) > 1:
                raise LimitReachedError("Cannot realize operation '**' between more than two variables.")

            if power.setv_type != SetVarType.SET_TO_POWER:
                raise TypeError(
                    "Cannot have different types of operations between variables at the same time; each kind "
                    "should be evaluated in its own .set()."
                )

            power = vars[0]

        if not isinstance(power, DFVariable) and not _tp.p_bool_check(
            power, _tp.Numeric, error_on_gameval=True
        ):
            return NotImplemented

        return VarOp(SetVarType.SET_TO_POWER, self, power)

    def __rpow__(self, other: typing.Union["Numeric", VarOp, "DFVariable"]) -> VarOp:
        if isinstance(other, VarOp):
            vars = other.vars
            if len(vars) > 1:
                raise LimitReachedError("Cannot realize operation '**' between more than two variables.")

            if other.setv_type != SetVarType.SET_TO_POWER:
                raise TypeError(
                    "Cannot have different types of operations between variables at the same time; each kind "
                    "should be evaluated in its own .set()."
                )

            other = vars[0]

        if not isinstance(other, DFVariable) and not _tp.p_bool_check(
            other, _tp.Numeric, error_on_gameval=True
        ):
            return NotImplemented

        return VarOp(SetVarType.SET_TO_POWER, other, self)

    def __mod__(self, other: typing.Union["Numeric", VarOp, "DFVariable"]) -> VarOp:
        if isinstance(other, VarOp):
            vars = other.vars
            if len(vars) > 1:
                raise LimitReachedError("Cannot realize operation '%' between more than two variables.")

            if other.setv_type != SetVarType.SET_TO_MOD:
                raise TypeError(
                    "Cannot have different types of operations between variables at the same time; each kind "
                    "should be evaluated in its own .set()."
                )

            other = vars[0]

        if not isinstance(other, DFVariable) and not _tp.p_bool_check(
            other, _tp.Numeric, error_on_gameval=True
        ):
            return NotImplemented

        return VarOp(SetVarType.SET_TO_MOD, self, other)

    def __rmod__(self, other: typing.Union["Numeric", VarOp, "DFVariable"]) -> VarOp:
        if isinstance(other, VarOp):
            vars = other.vars
            if len(vars) > 1:
                raise LimitReachedError("Cannot realize operation '%' between more than two variables.")

            if other.setv_type != SetVarType.SET_TO_MOD:
                raise TypeError(
                    "Cannot have different types of operations between variables at the same time; each kind "
                    "should be evaluated in its own .set()."
                )

            other = vars[0]

        if not isinstance(other, DFVariable) and not _tp.p_bool_check(
            other, _tp.Numeric, error_on_gameval=True
        ):
            return NotImplemented

        return VarOp(SetVarType.SET_TO_MOD, other, self)  # notice the change in order.

    def __truediv__(self, other: typing.Union["Numeric", VarOp, "DFVariable"]) -> VarOp:
        if not isinstance(other, (DFVariable, VarOp)) and not _tp.p_bool_check(
            other, _tp.Numeric, error_on_gameval=True
        ):
            return NotImplemented

        return VarOp(
            SetVarType.SET_TO_QUOTIENT, self, other,
            tags=[
                Tag("Division Mode", option="Default", action=SetVarType.SET_TO_QUOTIENT, block=BlockType.SET_VAR)]
        )

    def __rtruediv__(self, other: typing.Union["Numeric", VarOp, "DFVariable"]) -> VarOp:
        if not isinstance(other, (DFVariable, VarOp)) and not _tp.p_bool_check(
            other, _tp.Numeric, error_on_gameval=True
        ):
            return NotImplemented

        return VarOp(
            SetVarType.SET_TO_QUOTIENT, other, self,
            tags=[
                Tag("Division Mode", option="Default", action=SetVarType.SET_TO_QUOTIENT, block=BlockType.SET_VAR)]
        )

    def __floordiv__(self, other: typing.Union["Numeric", VarOp, "DFVariable"]) -> VarOp:
        if not isinstance(other, (DFVariable, VarOp)) and not _tp.p_bool_check(
            other, _tp.Numeric, error_on_gameval=True
        ):
            return NotImplemented

        return VarOp(
            SetVarType.SET_TO_QUOTIENT, self, other,
            tags=[Tag(
                "Division Mode", option="Round to Integer", action=SetVarType.SET_TO_QUOTIENT,
                block=BlockType.SET_VAR
            )]
        )

    def __rfloordiv__(self, other: typing.Union["Numeric", VarOp, "DFVariable"]) -> VarOp:
        if not isinstance(other, (DFVariable, VarOp)) and not _tp.p_bool_check(
            other, _tp.Numeric, error_on_gameval=True
        ):
            return NotImplemented

        return VarOp(
            SetVarType.SET_TO_QUOTIENT, other, self,
            tags=[Tag(
                "Division Mode", option="Round to Integer", action=SetVarType.SET_TO_QUOTIENT,
                block=BlockType.SET_VAR
            )]
        )

    # endregion:var_ops

    def text_contains(self) -> "IfVariable":
        """Checks if a text variable contains another text item.

        Returns
        -------
        :class:`IfVariable`
            The generated IfVariable codeblock for this condition.
        """

        args = Arguments([_tp.p_check(self)])

        return _IfVariable(
            action=IfVariableType.CONTAINS,
            args=args,
            append_to_reader=False,
            invert=False
        )

    @typing.overload
    def in_range(
        self, min_val: "Numeric", max_val: "Numeric"
    ) -> "IfVariable": ...

    @typing.overload
    def in_range(
        self, min_val: "Locatable", max_val: "Locatable"
    ) -> "IfVariable": ...

    def in_range(
        self, min_val: typing.Union["Numeric", "Locatable"], max_val: typing.Union["Numeric", "Locatable"]
    ) -> "IfVariable":
        """Checks if this number var is within 2 other numbers, or if this location var is within the region of 2 other
        locations. Note that this method is also implemented within :class:`~.DFNumber` and :class:`~.DFLocation`.

        Parameters
        ----------
        min_val : Union["Numeric", "Locatable"]
            The minimum value for this number, or the first location (one of the two corners of the region to check),
            if this is a Locatable.

        max_val : Union["Numeric", "Locatable"]
            The maximum value for this number, or the second location (the other corner, determining that `self` has
            to be a location staying inbetween `min_val` and `max_val`), if this is a Locatable.

        Returns
        -------
        :class:`IfVariable`
            The generated IfVariable codeblock for this condition.
        """

        args = Arguments(
            [
                _tp.p_check(self, typing.Union[_tp.Numeric, _tp.Locatable], "self"),
                _tp.p_check(min_val, typing.Union[_tp.Numeric, _tp.Locatable], "min_val"),
                _tp.p_check(max_val, typing.Union[_tp.Numeric, _tp.Locatable], "max_val")
            ]
        )

        return _IfVariable(
            action=IfVariableType.IN_RANGE,
            args=args,
            append_to_reader=False,
            invert=False
        )

    def is_near(
        self, center_val: typing.Union["Numeric", "Locatable"], valid_range: "Numeric"
    ) -> "IfVariable":
        """Checks if this :attr:`~.Numeric` is within a certain range of another number or if
        this :attr:`~.Locatable` is near another location. Note that this method is also implemented
        within :class:`~.DFNumber` and :class:`~.DFLocation`.

        Parameters
        ----------
        center_val : Union[:attr:`~.Numeric`, :attr:`~.Locatable`]
            The value to be compared with `self`.

        valid_range : :attr:`~.Numeric`
            The accepted distance between `self` and `center_val`.

        Returns
        -------
        :class:`IfVariable`
            The generated IfVariable codeblock for this condition.
        """

        args = Arguments(
            [
                _tp.p_check(self, typing.Union[_tp.Numeric, _tp.Locatable], "self"),
                _tp.p_check(center_val, typing.Union[_tp.Numeric, _tp.Locatable], "center_val"),
                _tp.p_check(valid_range, _tp.Numeric, "valid_range"),
            ]
        )

        return _IfVariable(
            action=IfVariableType.IS_NEAR,
            args=args,
            append_to_reader=False,
            invert=False
        )

    def item_equals(
        self, item: "ItemParam",
        *, mode: IfVItemEqComparisonMode = IfVItemEqComparisonMode.EXACTLY_EQUAL
    ) -> "IfVariable":
        """Works the same as Variable = but has a few extra options for item comparison.

        Parameters
        ----------
        item : :attr:`~.ItemParam`
            The item to compare self (which must be a valid :attr:`~.ItemParam` as well) to.

        mode : :class:`~.IfVItemEqComparisonMode`, optional
            The mode of comparison that will determine the equality between self and
            the given item. Defaults to :attr:`~.EXACTLY_EQUAL`.

        Returns
        -------
        :class:`IfVariable`
            The generated IfVariable codeblock for this condition.

        Todo
        ----
        Verify the default tag value.
        """

        args = Arguments(
            [_tp.p_check(self, _tp.ItemParam, "self"), _tp.p_check(item, _tp.ItemParam, "item")],
            tags=[
                Tag(
                    "Comparison Mode", option=IfVItemEqComparisonMode(mode),
                    action=IfVariableType.ITEM_EQUALS, block=BlockType.IF_VAR
                )
            ]
        )

        return _IfVariable(
            action=IfVariableType.ITEM_EQUALS,
            args=args,
            append_to_reader=False,
            invert=False
        )

    def item_has_tag(self, *tags: "Textable") -> "IfVariable":
        """Checks if this instance (has to be a valid :attr:`~.ItemParam`) has the given custom item tag(s).

        Parameters
        ----------
        tags : :attr:`~.Textable`
            The tags to have their presence within the item (self) checked.

        Returns
        -------
        :class:`IfVariable`
            The generated IfVariable codeblock for this condition.
        """

        args = Arguments(
            [_tp.p_check(self, _tp.ItemParam, "self")] + [_tp.p_check(o, _tp.Textable, "tags") for o in tags]
        )

        return _IfVariable(
            action=IfVariableType.ITEM_HAS_TAG,
            args=args,
            append_to_reader=False,
            invert=False
        )

    def list_contains(self, obj: "Param") -> "IfVariable":
        """Checks if any of a list's contents match the given value. Note that this instance (self)
        must be a valid :attr:`~.Listable` (i.e., the type of the Game Value, or the type of the Variable, if using
        typed var classes).

        Parameters
        ----------
        obj : :attr:`~.Param`
            The object that will be checked for being inside the list (i.e., if the list contains it).

        Returns
        -------
        :class:`IfVariable`
            The generated IfVariable codeblock for this condition.
        """

        args = Arguments([
            _tp.p_check(self, _tp.Listable, arg_name="self"),
            _tp.p_check(obj, _tp)
        ])

        return _IfVariable(
            action=IfVariableType.LIST_CONTAINS,
            args=args,
            append_to_reader=False,
            invert=False
        )

    def list_value_eq(self, index: "Numeric", value: "Param") -> "IfVariable":
        """Checks if a list's value at an index is equal to a given value. Note that `self` has to be a
        valid :attr:`~.Listable`.

        Note
        ----
        Using this method
        shouldn't be necessary; by using :class:`ListVar`, using ``var[i] == val`` (which is much more readable)
        should produce the same result; if using a :class:`DFGameValue`, then this should be available by default.

        Parameters
        ----------
        index : :attr:`~.Numeric`
            The index of the list element to compare.

        value : :attr:`~.Param`
            The value to be compared to the element at the given list index.

        Returns
        -------
        :class:`IfVariable`
            The generated IfVariable codeblock for this condition.
        """

        args = Arguments([
            _tp.p_check(self, _tp.Listable, "self"),
            _tp.p_check(index, _tp.Numeric, "index"),
            _tp.p_check(value, _tp.Param, "value")
        ])

        return _IfVariable(
            action=IfVariableType.LIST_VALUE_EQ,
            args=args,
            append_to_reader=False,
            invert=False
        )

    def text_matches(self) -> "IfVariable":  # TODO
        """Checks if this text matches another text.

        Returns
        -------
        :class:`IfVariable`
            The generated IfVariable codeblock for this condition.
        """

        args = Arguments([_tp.p_check(self)])

        return _IfVariable(
            action=IfVariableType.TEXT_MATCHES,
            args=args,
            append_to_reader=False,
            invert=False
        )

    def var_is_type(self) -> "IfVariable":  # TODO ...
        """Checks if a variable is a certain type of variable.

        Returns
        -------
        :class:`IfVariable`
            The generated IfVariable codeblock for this condition.
        """

        args = Arguments([self])

        return _IfVariable(
            action=IfVariableType.VAR_IS_TYPE,
            args=args,
            append_to_reader=False,
            invert=False
        )



class DFGameValue(DFType, VarOperable):
    """Used for game values, that change depending on the plot's state.

    Parameters
    ----------\u200b
    gval_type : :class:`~py2df.enums.dftypes.GameValueType`
        The type of Game Value this is.

    target : Optional[:class:`~py2df.enums.targets.Target`], optional
        The target of this Game Value, or None. Defaults to None.


    .. container:: comparisons

        .. describe:: a == b, a != b

            Returns the equivalent :class:`~.IfVariable` block for equals/not equals. Has two uses:

            1. **Is used to compare the variables with an If Var.** Example usage::

                with val_a == val_b:
                    # code that is only executed in DiamondFire if 'val_a' and 'val_b' are equal in value.

                with val_c != val_d:
                    # code that is only executed in DiamondFire if 'val_c' and 'val_d' are different in value.

            2. **Is used to compare, IN PYTHON, the values'** :attr:`gval_type` **and** :attr:`target` attrs \
(by calling :func:`bool` on the generated IfVariable block). Example usage::

                if val_a == val_b:
                    # code that is only read, IN PYTHON, if 'val_a' and 'val_b' have the same 'gval_type' and 'target' \
attrs.

                if val_c != val_d:
                    # code that is only read, IN PYTHON, if 'val_c' and 'val_b' have a different 'gval_type' or \
'target' attr.

        .. describe:: a > b, a >= b, a < b, a <= b

            Returns the equivalent :class:`~.IfVariable` block for the given comparison. **Its only usage is as
            a Codeblock** (in a `with`).
            For example::

                with var_a > var_b:
                    # code that is only executed in DiamondFire if 'var_a' is bigger than 'var_b' in value.

                with var_c < var_d:
                    # code that is only executed in DiamondFire if 'var_c' is less than 'var_d' in value.

            .. note::

                Those comparisons are not usable in Python if's; if a :func:`bool` is attempted on the resulting
                IfVariable block, it will always return True. This mechanism is only implemented for ``==`` and ``!=``.

            .. warning::

                Assuming that one of them is a DFVariable, the other has to be a valid :attr:`~.Numeric` parameter.
                Otherwise, a TypeError may be raised (if the given type does not support operations with DFVariable,
                which is likely).


    .. container:: operations

        .. describe:: a + b, a - b, a * b, a ** b, a / b, a // b, a % b

            Creates a :class:`VarOp` instance representing this operation between different variables/variables
            and values/etc.
            It is meant to be given as the parameter for :meth:`DFVariable.set`, which will then place the appropriate
            Set Variable type (setting the variable instance to this operation)

            `a` is the :class:`VarOperable` instance, while `b`, in this case, is the :attr:`~.Numeric` to realize this
            operation with.

            .. note::

                If the operation is addition or subtraction, `b` can also be a :attr:`~.Locatable` parameter (represent
                a location), besides Numeric.

            .. warning::

                **You cannot mix operations.** For example, ``a + b - c * d ** e`` will raise. Stick to only one
                at once, and have one :meth:`DFVariable.set` call for each kind.
                (There is only one Set Var for each kind.)
                (However, operations with multiple variables, up to 27, work: ``a + b + c + ... + z``)

                If there is an attempt to mix operations, a :exc:`TypeError` is raised.

                Similarly, if there is an attempt to have an operation with more than 26 variables (chest size is
                up to 27 items, while 1 slot is the variable being set), then a :exc:`~.LimitReachedError` is raised
                instead.

        .. describe:: str(a)

            Returns ``a.gval_type.value`` (the type of Game Value).

        .. describe:: hash(a)

            Returns an unique hash identifying this Game Value by its Game Value type and its target.


    Attributes
    ----------\u200b
        gval_type : :class:`~py2df.enums.dftypes.GameValueType`
            The type of Game Value this is.

        target : Optional[:class:`~py2df.enums.targets.Target`], optional
            The target of this Game Value, or None. Defaults to None.
    """
    __slots__ = ("gval_type", "target")

    gval_type: GameValueType
    target: typing.Optional[Target]

    def __init__(self, gval_type: GameValueType, target: typing.Optional[Target] = None):
        """
        Initializes the Game Value.

        Parameters
        ----------
        gval_type : :class:`~py2df.enums.dftypes.GameValueType`
            The type of Game Value this is.

        target : Optional[:class:`~py2df.enums.targets.Target`], optional
            The target of this Game Value, or None. Defaults to None.
        """

        self.gval_type = GameValueType(gval_type)
        self.target = target or None

    def set(
        self, gval_type: GameValueType = DEFAULT_VAL, target: typing.Optional[Target] = DEFAULT_VAL
    ) -> "DFGameValue":
        """Configures this Game Value. Note that this does not create a Set Var like with DFVariable; instead, it
        changes, IN PYTHON, the attributes of this Game Value.

        Parameters
        ----------
        gval_type : :class:`~py2df.enums.dftypes.GameValueType`
            The type of Game Value this is.

        target : Optional[:class:`~py2df.enums.targets.Target`], optional
            The target of this Game Value, or None.

        Returns
        -------
        :class:`DFGameValue`
            self to allow chaining.
        """

        if gval_type != DEFAULT_VAL:
            self.gval_type = GameValueType(gval_type)

        if target != DEFAULT_VAL:
            self.target = target or None

        return self

    def __repr__(self):
        return f"<{self.__class__.__name__} gval_type={repr(self.gval_type.value)} \
target={repr(str(self.target) if self.target else self.target)}>"

    def __str__(self):
        return self.gval_type.value

    def as_json_data(self) -> dict:
        """Obtains a JSON-serializable dict representation of this Game Value.

        Returns
        -------
        :class:`dict`
            A JSON-serializable dict.
        """
        return dict(
            id=constants.ITEM_ID_GAME_VALUE,
            data=dict(
                type=self.gval_type.value,
                target=self.target.value if self.target else None
            )
        )

    @classmethod
    def from_json_data(cls, data: dict):
        """Obtain a Game Value from pre-existing parsed JSON data.

        Must be of the form (have at least those keys)::

            { "data": { "type": str, "target": str } }

        Where ``str`` would be the type of the value.

        Parameters
        ----------
        data : :class:`dict`
            The parsed JSON :class:`dict`.

        Returns
        -------
        :class:`DFGameValue`
            :class:`DFGameValue` instance.

        Raises
        ------
        :exc:`TypeError`
            If the data is malformed (does not follow the structure detailed above).
        """
        if (
                not isinstance(data, dict)
                # or "id" not in data  # not really required
                or "data" not in data
                or not isinstance(data["data"], dict)
                or "type" not in data["data"]
                or type(data["data"]["type"]) != str
                or "target" not in data["data"]
                or type(data["data"]["target"]) != str
        ):
            raise TypeError(
                "Malformed DFGameValue parsed JSON data! Must be a dict with, at least, a 'data' dict containing"
                "'type' and 'target' str values."
            )

        in_data = data["data"]
        target_str = in_data["target"]
        target_instance = None
        if target_str.lower() != "none":
            try:
                target_instance = PlayerTarget(target_str)
            except ValueError:
                try:
                    target_instance = EntityTarget(target_str)
                except ValueError as e:
                    raise ValueError("Invalid target specified in Game Value JSON data.") from e

        return cls(GameValueType(in_data["type"]), target_instance)

    # def to_item(self) -> "Item":
    #     pass  # TODO: Apple

    def __hash__(self):
        return hash((self.__class__.__name__, self.gval_type, str(self.target)))


class DFVariable(DFType, VarOperable):
    """Represents a DiamondFire variable. **Note that all variables with same 'name' attribute represent the same
    var.**

    Parameters
    ----------\u200b
    name : :class:`str`
        The name of this variable. This uniquely identifies it, along with its scope.

    init_value : Optional[Union[:attr:`~.Param`, :class:`VarOp`]], optional
        An optional initial value for this variable. Defaults to ``None`` (i.e., doesn't set a value).

        .. warning:

            If any value is specified, **this will create a Set Var block**.

    scope : :class:`~.VariableScope`, optional
        The scope of this variable. This can also be set through the kwargs ``unsaved``, ``saved`` and ``local`` .
        Defaults to :attr:`~.VariableScope.UNSAVED`.

    unsaved : :class:`bool`, optional
        If ``True``, the variable's scope is set to :attr:`~.VariableScope.UNSAVED` - i.e., the value does not persist
        between successive plot uses (when the amount of players reaches 0, the variable is reset).


    .. container:: comparisons

        .. describe:: a == b, a != b

            Returns the equivalent :class:`~.IfVariable` block for equals/not equals. Has two uses:

            1. **Is used to compare the variables with an If Var.** Example usage::

                with var_a == var_b:
                    # code that is only executed in DiamondFire if 'var_a' and 'var_b' are equal in value.

                with var_c != var_d:
                    # code that is only executed in DiamondFire if 'var_c' and 'var_d' are different in value.

            2. **Is used to compare, IN PYTHON, the variables' names and scopes** (by calling :func:`bool` on the \
generated IfVariable block). Example usage::

                if var_a == var_b:
                    # code that is only read, IN PYTHON, if 'var_a' and 'var_b' have the same 'name' and 'scope' attrs.

                if var_c != var_d:
                    # code that is only read, IN PYTHON, if 'var_c' and 'var_b' have a different 'name' or 'scope' attr.

        .. describe:: a > b, a >= b, a < b, a <= b

            Returns the equivalent :class:`~.IfVariable` block for the given comparison. **Its only usage is as
            a Codeblock** (in a `with`).
            For example::

                with var_a > var_b:
                    # code that is only executed in DiamondFire if 'var_a' is bigger than 'var_b' in value.

                with var_c < var_d:
                    # code that is only executed in DiamondFire if 'var_c' is less than 'var_d' in value.

            .. note::

                Those comparisons are not usable in Python if's; if a :func:`bool` is attempted on the resulting
                IfVariable block, it will always return True. This mechanism is only implemented for ``==`` and ``!=``.

            .. warning::

                Assuming that one of them is a DFVariable, the other has to be a valid :attr:`~.Numeric` parameter.
                Otherwise, a TypeError may be raised (if the given type does not support operations with DFVariable,
                which is likely).


    .. container:: operations

        .. describe:: a + b, a - b, a * b, a ** b, a / b, a // b, a % b

            Creates a :class:`VarOp` instance representing this operation between different variables/variables
            and values/etc.
            It is meant to be given as the parameter for :meth:`set`, which will then place the appropriate
            Set Variable type.

            `a` is the :class:`DFVariable`, while `b`, in this case, is the :attr:`~.Numeric` to realize this
            operation with.

            .. warning::

                **You cannot mix operations.** For example, ``a + b - c * d ** e`` will raise. Stick to only one
                at once, and have one :meth:`set` call for each kind. (There is only one Set Var for each kind.)
                (However, operations with multiple variables, up to 27, work: ``a + b + c + ... + z``)

                If there is an attempt to mix operations, a :exc:`TypeError` is raised.

                Similarly, if there is an attempt to have an operation with more than 26 variables (chest size is
                up to 27 items, while 1 slot is the variable being set), then a :exc:`~.LimitReachedError` is raised
                instead.

            .. note::

                If the operation is addition or subtraction, `b` can also be a :attr:`~.Locatable` parameter (represent
                a location), besides Numeric.

        .. describe:: a += b, a -= b, a *= b, a **= b. a /= b, a //= b, a %= b

            Same behavior as ``a.set(a ? b)``, where ``?`` is the given operation (`b` must be :attr:`~.Numeric`).

            .. note::

                If the operation given is either ``+=`` or ``-=``, then it will place the respective
                ``+=`` and ``-=`` Set Var blocks instead of ``a.set(a +/- b)``. This is because those are
                the only ones that have a SetVar equivalent.

        .. describe:: str(a)

            Returns this variable as a string in the form ``%var(name)``, where `name` is the variable's name.
            When used in a string, DiamondFire replaces it with the variable's value.

        .. describe:: hash(a)

            Returns an unique hash identifying this variable by name and scope.


    Attributes
    ----------\u200b
    name : :class:`str`
        The name of this variable. This uniquely identifies it, along with its scope.

    scope : :class:`~.VariableScope`
        The scope of this variable (:attr:`~.UNSAVED`, :attr:`~.SAVED` or :attr:`~.LOCAL`).
    """
    __slots__ = ("name", "scope")

    name: str
    scope: VariableScope

    def __init__(
        self, name: typing.Union[str, DFText], init_value: typing.Optional["Param"] = None,
        *, scope: VariableScope = DEFAULT_VAL, unsaved: bool = True,
        saved: bool = False, local: bool = False
    ):
        _heavy_imports()

        self.name: str = str(name)

        if scope != DEFAULT_VAL:
            self.scope: VariableScope = VariableScope(scope)
        elif saved:
            self.scope: VariableScope = VariableScope.SAVED
        elif local:
            self.scope: VariableScope = VariableScope.LOCAL
        elif unsaved:
            self.scope: VariableScope = VariableScope.UNSAVED

        if init_value:
            self.set(init_value)

    def set(self, value: typing.Union["Param", VarOp, typing.Iterable["Param"]]) -> "SetVar":
        """
        Set this variable. Note that this simply creates a Set Var block and returns it. Example usage::

            var_a.set(var_b)  # SetVar (=): Sets a's value to b's
            var_a.set(var_b + var_c + 5)  # SetVar (+): Adds the values of var_b, var_c and 5
            var_a.set(["hello", 5, var_b])  # SetVar (Create List): Creates a list var with those values.

        See the 'Supported Operations' section for more info on operations. Note that they cannot be mixed (i.e.,
        can only set one kind of operation at a time - 'a + b * c' is not allowed, for example).

        Parameters
        ----------
        value : Union[:attr:`~.Param`, :class:`VarOp`, Iterable[:attr:`~.Param`]]
            The value. Can consist of any valid Param type, a var operation or an iterable of Params.
            The codeblock creation relation is as follows:

            +---------------------------+------------------------------------------------------------------------+
            |       Type(s) given       |                           Codeblock created                            |
            +===========================+========================================================================+
            | :attr:`~.Param`           | Set Var: = (:attr:`~.SET_TO`)                                          |
            +---------------------------+------------------------------------------------------------------------+
            | :class:`VarOp`            | One of: Set Var: +, -, %, x, Exponent, Divide (depending on operation) |
            +---------------------------+------------------------------------------------------------------------+
            | Iterable[:attr:`~.Param`] | Set Var: Create List (:attr:`~.CREATE_LIST`)                           |
            +---------------------------+------------------------------------------------------------------------+


        Returns
        -------
        :class:`~.SetVar`
            The generated SetVar block.
        """
        setv_type = SetVarType.SET_TO
        args: Arguments
        if isinstance(value, VarOp):  # a var operation was given
            setv_type = SetVarType(value.setv_type)
            tp_to_check = typing.Union[_tp.Numeric, _tp.Locatable] if setv_type in (
                SetVarType.SET_TO_ADDITION, SetVarType.SET_TO_SUBTRACTION
            ) else _tp.Numeric

            args = Arguments(
                [self] + [_tp.p_check(o, tp_to_check, "value") for o in value.vars],
                tags=value.tags or []
            )

        elif _tp.p_bool_check(value, _tp.Param):  # a parameter was given
            args = Arguments([self] + [_tp.p_check(value, _tp.Param, "value")])

        elif isinstance(value, collections.Iterable):  # an iterable of parameters was given
            setv_type = SetVarType.CREATE_LIST
            args = Arguments([self] + [_tp.p_check(o, _tp.Param, "value") for o in value])

        else:
            _tp.p_check(value, _tp.Param, "value")  # this will error
            raise TypeError

        return _SetVar(
            action=setv_type,
            args=args,
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

    def __repr__(self):
        return f"<{self.__class__.__name__} name={json.dumps(self.name)} scope=\"{self.scope.value}\">"

    def __str__(self):
        return f"%var({self.name})"

    def __iadd__(self, other: typing.Union["Numeric", VarOp, "DFVariable"]) -> "DFVariable":
        if not isinstance(other, (DFVariable, VarOp)) and not _tp.p_bool_check(
            other, _tp.Numeric, error_on_gameval=True
        ):
            return NotImplemented

        _SetVar(
            action=SetVarType.ADD,
            args=Arguments(
                [_tp.p_check(o, _tp.Numeric) for o in other.vars] if isinstance(other, VarOp) else [
                    _tp.p_check(other, _tp.Numeric)
                ]
            ),
            append_to_reader=True
        )

        return self

    def __isub__(self, other: typing.Union["Numeric", VarOp, "DFVariable"]) -> "DFVariable":
        if not isinstance(other, (DFVariable, VarOp)) and not _tp.p_bool_check(
            other, _tp.Numeric, error_on_gameval=True
        ):
            return NotImplemented

        _SetVar(
            action=SetVarType.SUBTRACT,
            args=Arguments(
                [_tp.p_check(o, _tp.Numeric) for o in other.vars] if isinstance(other, VarOp) else [
                    _tp.p_check(other, _tp.Numeric)
                ]
            ),
            append_to_reader=True
        )

        return self

    def __imul__(self, other: typing.Union["Numeric", VarOp, "DFVariable"]) -> "DFVariable":
        self.set(self.__mul__(other))

        return self

    def __ipow__(self, power: typing.Union["Numeric", VarOp, "DFVariable"], modulo=None) -> "DFVariable":
        self.set(self.__pow__(power))

        return self

    def __imod__(self, other: typing.Union["Numeric", VarOp, "DFVariable"]) -> "DFVariable":
        self.set(self.__mod__(other))

        return self

    def __itruediv__(self, other: typing.Union["Numeric", VarOp, "DFVariable"]) -> "DFVariable":
        self.set(self.__truediv__(other))

        return self
        # [Tag("Division Mode", option="Default", action=SetVarType.SET_TO_QUOTIENT, block=BlockType.SET_VAR)]

    def __ifloordiv__(self, other: typing.Union["Numeric", VarOp, "DFVariable"]) -> "DFVariable":
        self.set(self.__floordiv__(other))

        return self
        # [Tag("Division Mode", option="Round to Integer", action=SetVarType.SET_TO_QUOTIENT, block=BlockType.SET_VAR)]

    def __hash__(self):
        return hash((self.name, self.scope))


remove_u200b_from_doc(DFVariable, VarOp, DFGameValue, VarOperable)


