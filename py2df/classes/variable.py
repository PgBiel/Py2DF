import collections
import typing
import json

from collections import deque
from ..constants import SMALL_CHEST_SIZE
from .abc import DFType
from .mc_types import DFText
from .collections import Arguments
from .dataclass import Tag
from ..utils import remove_u200b_from_doc, flatten, TrueLiteral, FalseLiteral
from ..enums import SetVarType, VariableScope, BlockType, IfVariableType
from ..constants import ITEM_ID_DYNAMIC_VAR, DEFAULT_VAL
from ..errors import LimitReachedError

if typing.TYPE_CHECKING:
    from .. import typings as _tp
    from ..codeblocks.ifs import IfVariable, IfVariable as _IfVariable
    from ..codeblocks.utilityblock import SetVar  # lazy import in Var init
    from ..typings import Param, Numeric, Locatable


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


class DFVariable(DFType):
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
        global _SetVar, _tp, _IfVariable
        from ..codeblocks.utilityblock import SetVar  # lazy import to avoid cyclic imports
        from .. import typings                        # ^
        from ..codeblocks.ifs import IfVariable       # ^

        self.name: str = str(name)

        if scope != DEFAULT_VAL:
            self.scope: VariableScope = VariableScope(scope)
        elif saved:
            self.scope: VariableScope = VariableScope.SAVED
        elif local:
            self.scope: VariableScope = VariableScope.LOCAL
        elif unsaved:
            self.scope: VariableScope = VariableScope.UNSAVED

        _SetVar = SetVar
        _tp = typings
        _IfVariable = IfVariable

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
        if not _tp.p_bool_check(other, _tp.Numeric):
            return NotImplemented

        return _IfVariable(
            action=IfVariableType.GREATER_THAN,
            args=Arguments([self, _tp.p_check(other, _tp.Numeric, "other")]),
            append_to_reader=False
        )

    def __ge__(self, other: "Numeric") -> "IfVariable":
        if not _tp.p_bool_check(other, _tp.Numeric):
            return NotImplemented

        return _IfVariable(
            action=IfVariableType.GREATER_THAN_OR_EQUAL_TO,
            args=Arguments([self, _tp.p_check(other, _tp.Param, "other")]),
            append_to_reader=False
        )

    def __lt__(self, other: "Numeric") -> "IfVariable":
        if not _tp.p_bool_check(other, _tp.Numeric):
            return NotImplemented

        return _IfVariable(
            action=IfVariableType.LESS_THAN,
            args=Arguments([self, _tp.p_check(other, _tp.Numeric, "other")]),
            append_to_reader=False
        )

    def __le__(self, other: "Numeric") -> "IfVariable":
        if not _tp.p_bool_check(other, _tp.Numeric):
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
            other, typing.Union[_tp.Numeric, _tp.Locatable]
        ):
            return NotImplemented

        return VarOp(SetVarType.SET_TO_ADDITION, self, other)

    def __radd__(self, other: typing.Union["Numeric", "Locatable", VarOp, "DFVariable"]):
        return self.__add__(other)

    def __sub__(self, other: typing.Union["Numeric", "Locatable", VarOp, "DFVariable"]):
        if not isinstance(other, (DFVariable, VarOp)) and not _tp.p_bool_check(
            other, typing.Union[_tp.Numeric, _tp.Locatable]
        ):
            return NotImplemented

        return VarOp(SetVarType.SET_TO_SUBTRACTION, self, other)

    def __rsub__(self, other: typing.Union["Numeric", "Locatable", VarOp, "DFVariable"]):
        if not isinstance(other, (DFVariable, VarOp)) and not _tp.p_bool_check(
                other, typing.Union[_tp.Numeric, _tp.Locatable]
        ):
            return NotImplemented

        res = VarOp(SetVarType.SET_TO_SUBTRACTION, self)
        res._add_var(
            other, SetVarType.SET_TO_SUBTRACTION, append_left=True, is_rsub=True, allow_other_iters=False,
            error_incompatible=True, modify_self=True
        )

    def __mul__(self, other: typing.Union["Numeric", VarOp, "DFVariable"]):
        if not isinstance(other, (DFVariable, VarOp)) and not _tp.p_bool_check(other, _tp.Numeric):
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

        if not isinstance(power, DFVariable) and not _tp.p_bool_check(power, _tp.Numeric):
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

        if not isinstance(other, DFVariable) and not _tp.p_bool_check(other, _tp.Numeric):
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

        if not isinstance(other, DFVariable) and not _tp.p_bool_check(other, _tp.Numeric):
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

        if not isinstance(other, DFVariable) and not _tp.p_bool_check(other, _tp.Numeric):
            return NotImplemented

        return VarOp(SetVarType.SET_TO_MOD, other, self)  # notice the change in order.

    def __truediv__(self, other: typing.Union["Numeric", VarOp, "DFVariable"]) -> VarOp:
        if not isinstance(other, (DFVariable, VarOp)) and not _tp.p_bool_check(other, _tp.Numeric):
            return NotImplemented

        return VarOp(
            SetVarType.SET_TO_QUOTIENT, self, other,
            tags=[Tag("Division Mode", option="Default", action=SetVarType.SET_TO_QUOTIENT, block=BlockType.SET_VAR)]
        )

    def __rtruediv__(self, other: typing.Union["Numeric", VarOp, "DFVariable"]) -> VarOp:
        if not isinstance(other, (DFVariable, VarOp)) and not _tp.p_bool_check(other, _tp.Numeric):
            return NotImplemented

        return VarOp(
            SetVarType.SET_TO_QUOTIENT, other, self,
            tags=[Tag("Division Mode", option="Default", action=SetVarType.SET_TO_QUOTIENT, block=BlockType.SET_VAR)]
        )

    def __floordiv__(self, other: typing.Union["Numeric", VarOp, "DFVariable"]) -> VarOp:
        if not isinstance(other, (DFVariable, VarOp)) and not _tp.p_bool_check(other, _tp.Numeric):
            return NotImplemented

        return VarOp(
            SetVarType.SET_TO_QUOTIENT, self, other,
            tags=[Tag(
                "Division Mode", option="Round to Integer", action=SetVarType.SET_TO_QUOTIENT, block=BlockType.SET_VAR
            )]
        )

    def __rfloordiv__(self, other: typing.Union["Numeric", VarOp, "DFVariable"]) -> VarOp:
        if not isinstance(other, (DFVariable, VarOp)) and not _tp.p_bool_check(other, _tp.Numeric):
            return NotImplemented

        return VarOp(
            SetVarType.SET_TO_QUOTIENT, other, self,
            tags=[Tag(
                "Division Mode", option="Round to Integer", action=SetVarType.SET_TO_QUOTIENT, block=BlockType.SET_VAR
            )]
        )

    def __iadd__(self, other: typing.Union["Numeric", VarOp, "DFVariable"]) -> "DFVariable":
        if not isinstance(other, (DFVariable, VarOp)) and not _tp.p_bool_check(other, _tp.Numeric):
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
        if not isinstance(other, (DFVariable, VarOp)) and not _tp.p_bool_check(other, _tp.Numeric):
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
        # [Tag("Divison Mode", option="Default", action=SetVarType.SET_TO_QUOTIENT, block=BlockType.SET_VAR)]

    def __ifloordiv__(self, other: typing.Union["Numeric", VarOp, "DFVariable"]) -> "DFVariable":
        self.set(self.__floordiv__(other))

        return self
        # [Tag("Divison Mode", option="Round to Integer", action=SetVarType.SET_TO_QUOTIENT, block=BlockType.SET_VAR)]

    def __hash__(self):
        return hash((self.name, self.scope))
    # endregion:var_ops


remove_u200b_from_doc(DFVariable, VarOp)
