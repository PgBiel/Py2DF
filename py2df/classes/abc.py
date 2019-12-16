"""
Generic base classes for the library.
"""
import abc

from .. import constants
from ..enums import BlockType, CodeblockActionType, ActionType, EventType, IfType, RepeatType, Target, IfEntityType
from ..utils import remove_u200b_from_doc, snake_to_capitalized_words
import typing

if typing.TYPE_CHECKING:
    from .collections import Arguments
    from .mc_types import Item

# region:JSONData


class JSONData(metaclass=abc.ABCMeta):
    """An ABC that describes a class implementing ``.as_json_data()``."""
    __slots__ = ()

    @abc.abstractmethod
    def as_json_data(self) -> typing.Union[str, int, float, dict, list, tuple, bool]:
        """Exports this class as parsed json data (not as string, but as a valid json data type).

        Returns
        -------
        Union[:class:`str`, :class:`int`, :class:`float`, :class:`dict`, :class:`list`, :class:`tuple`, :class:`bool`]
        """
        raise NotImplementedError

    @classmethod
    def __subclasshook__(cls, o_cls: type):
        """
        Checks if the given class is a subclass of JSONData (implements it.)
        :param o_cls: Class to check.
        :return: True if subclass; NotImplemented otherwise
        """
        if cls is JSONData:
            if any("as_json_data" in B.__dict__ for B in o_cls.__mro__):
                return True  # has to have "as_json_data"

        return NotImplemented


class BuildableJSONData(JSONData, metaclass=abc.ABCMeta):
    """An ABC that describes a JSON Data class that can also build itself from pre-existing JSON data."""
    __slots__ = ()

    @abc.abstractmethod
    def as_json_data(self) -> typing.Union[str, int, float, dict, list, tuple]:
        """Exports this class as parsed json data (not as string, but as a valid json data type).

        Returns
        -------
        Union[:class:`str`, :class:`int`, :class:`float`, :class:`dict`, :class:`list`, :class:`tuple`, :class:`bool`]
        """
        raise NotImplementedError

    @classmethod
    @abc.abstractmethod
    def from_json_data(cls: type, data: typing.Union[str, int, float, dict, list, tuple]) -> "BuildableJSONData":
        """Builds a class instance using pre-existing PARSED JSON data. (Str, int, float, dict, list, tuple).

        Parameters
        ----------
        data : Union[:class:`str`, :class:`int`, :class:`float`, :class:`dict`, :class:`list`, :class:`tuple`, \
:class:`bool`]
            The parsed JSON data.

        Returns
        -------
        :class:`BuildableJSONData`
            The new class instance.

        """
        raise NotImplementedError

    @classmethod
    def __subclasshook__(cls, o_cls: type):
        """
        Checks if the given class is a subclass of BuildableJSONData (implements it.)
        :param o_cls: Class to check.
        :return: `True` if subclass; `NotImplemented` otherwise
        """
        if cls is BuildableJSONData:
            if JSONData.__subclasshook__(o_cls) is NotImplemented:  # must be valid JSON data.
                return NotImplemented

            if any("from_json_data" in B.__dict__ for B in o_cls.__mro__):
                return True  # has to have "as_json_data"

        return NotImplemented


class Itemable(JSONData, metaclass=abc.ABCMeta):
    """An ABC that describes a class representing an item or DF type (i.e., can be converted to
    :class:`~py2df.classes.mc_types.Item`)."""
    __slots__ = ()

    @abc.abstractmethod
    def as_json_data(self):
        """Exports this class as parsed json data (not as string, but as a valid json data type).

        Returns
        -------
        Union[:class:`str`, :class:`int`, :class:`float`, :class:`dict`, :class:`list`, :class:`tuple`, :class:`bool`]
        """
        raise NotImplementedError

    @abc.abstractmethod
    def to_item(self) -> "Item":
        """Converts this class to an equivalent Item.

        Returns
        -------
        :class:`~py2df.classes.mc_types.Item`
        """
        raise NotImplementedError

    @classmethod
    def __subclasshook__(cls, o_cls: type):
        """
        Checks if the given class is a subclass of JSONData (implements it.)
        :param o_cls: Class to check.
        :return: True if subclass; NotImplemented otherwise
        """
        if cls is Itemable:
            if JSONData.__subclasshook__(o_cls) is NotImplemented:  # must be valid JSON data.
                return NotImplemented

            if any("to_item" in B.__dict__ for B in o_cls.__mro__):
                return True  # has to have "as_json_data"

        return NotImplemented

# endregion:JSONData

# region:Misc


class Settable(metaclass=abc.ABCMeta):
    """An ABC that describes a class that can be ``.set()`` ."""
    @abc.abstractmethod
    def set(self, *args, **kwargs) -> "Settable":
        """
        Set this class instance's attributes.

        Parameters
        ----------
        args : Any
            Attributes to set.

        kwargs : Any
            Attributes to set.

        Returns
        -------
        :class:`Settable`
            self to allow chaining.
        """
        raise NotImplementedError

    @classmethod
    def __subclasshook__(cls, o_cls: type):
        """
        Checks if the given class is a subclass of Settable (implements it.)
        :param o_cls: Class to check.
        :return: True if subclass; NotImplemented otherwise
        """
        if cls is Settable and any("set" in B.__dict__ for B in o_cls.__mro__):
            return True  # has to have "set" attr

        return NotImplemented


class FunctionHolder(metaclass=abc.ABCMeta):
    """
    An ABC that describes a class holding a function.

    Attributes
    ----------\u200b
        function : Callable
            The function that an instance holds.
    """
    __slots__ = ()
    function: typing.Callable

    @classmethod
    def __subclasshook__(cls, o_cls: type):
        """
        Checks if the given class is a subclass of Settable (implements it.)
        :param o_cls: Class to check.
        :return: True if subclass; NotImplemented otherwise
        """
        if cls is FunctionHolder and any("function" in B.__dict__ for B in o_cls.__mro__):
            return True  # has to have "function" attr

        return NotImplemented


class DFType(BuildableJSONData, Settable, metaclass=abc.ABCMeta):
    """Represents a DiamondFire variable type."""
    pass


# endregion:Misc

# region:Codeblock


class Block(JSONData, metaclass=abc.ABCMeta):
    """An ABC that describes any block in code -- either Codeblock or Bracket.

    Attributes
    ----------\u200b
    length : :class:`int`
        The length of this Block.
    """
    length: int


class Codeblock(Block, metaclass=abc.ABCMeta):
    """An ABC that describes any codeblock - event, action etc.

    Attributes\u200b
    -------------
        block : :class:`~py2df.enums.parameters.BlockType`
            Type of block. (Class var)

        args : Optional[:class:`~py2df.classes.collections.Arguments`]
            Arguments of this codeblock (Instance var). Some codeblocks (such as events) do not have arguments; for
            them, this attribute is ``None``.

        action : Optional[:class:`~py2df.enums.enum_util.CodeBlockActionType`]
            Specific action/description of it - e.g. event name (Class/instance var). Some do not have this.

        sub_action : Optional[:class:`~py2df.enums.enum_util.CodeBlockActionType`]
            Describes, in an even more specific way, the aforementioned action. Generally used in Repeat and
            SelectObj objects.

        length : :class:`int`
            The space, in Minecraft blocks, that this codeblock occupies. (Most are 2, but some, like IFs, are 1)
            (Class var)

        data : Optional[:class:`str`]
            An optional customized data field. Used for Function and Process names.

        target : Optional[:class:`~py2df.enums.targets.Target`]
            The target of this codeblock, if any.
    """
    block: BlockType
    args: typing.Optional["Arguments"]
    action: typing.Optional[CodeblockActionType]
    sub_action: typing.Optional[CodeblockActionType]
    length: int
    data: typing.Optional[str]
    target: typing.Optional[Target]
    __slots__ = ()

    @classmethod
    def __subclasshook__(cls, o_cls: type):
        """
        Checks if the given class is a subclass of Codeblock (implements it).
        :param o_cls: Class to check.
        :return: True if subclass; NotImplemented otherwise
        """

        if cls is Codeblock:
            attribs = ["block", "length"]  # must have those attributes to be a codeblock.
            if all(any(attr in B.__dict__ for B in o_cls.__mro__) for attr in attribs):
                return True
        return NotImplemented

    def __repr__(self):
        attrs = " ".join(
            f"{attr}={repr(getattr(self, attr))}" for attr in filter(lambda t: not str(t).startswith("_"), getattr(
                self.__class__, "__slots__", self.__class__.__dict__
            ))
        )
        if attrs:
            attrs = " " + attrs

        return f"<{self.__class__.__name__}" + attrs + ">"

    def as_json_data(self) -> dict:
        """Obtains this codeblock as a JSON-serializable dict.

        Returns
        -------
        :class:`dict`
        """
        from .collections import Arguments
        return dict(
            id=constants.BLOCK_ID,
            block=self.block.value,
            **(
                dict(
                    args=(self.args if self.args and isinstance(self.args, JSONData) else Arguments()).as_json_data()
                )
            ),
            **(
                dict(
                    action=str(self.action.value)
                ) if self.action and hasattr(self.action, "value") else dict()
            ),
            **(
                dict(
                    subAction=(
                        "E" if self.sub_action in (
                            IfEntityType.NAME_EQUALS, IfEntityType.IS_NEAR, IfEntityType.STANDING_ON
                        ) else ""  # ENameEquals; EIsNear; EStandingOn => separate from IfPlayer's.
                    ) + str(self.sub_action.value)
                ) if self.sub_action and hasattr(self.sub_action, "value") else dict()
            ),
            **(
                dict(
                    data=str(self.data)[:constants.MAX_FUNC_NAME_LEN]
                ) if self.data else dict()
            ),
            **(
                dict(
                    target=str(self.target.value if hasattr(self.target, "value") else self.target)
                ) if self.target else dict()
            )
        )


class ActionBlock(Codeblock, metaclass=abc.ABCMeta):
    """An ABC that describes any action - Player Action, Game Action, Entity Action or Control.
    Must implement :class:`Codeblock`.

    Includes all of :class:`Codeblock` 's attributes, plus:

    Attributes\u200b
    -----------
        block : Union[:attr:`~py2df.enums.parameters.BlockType.PLAYER_ACTION`, \
:attr:`~py2df.enums.action.BlockType.ENTITY_ACTION`, :attr:`~py2df.enums.action.BlockType.GAME_ACTION`, \
:attr:`~py2df.enums.action.CONTROL`]
            The block type - either `Player Action`, `Entity Action`. `Game Action` or `Control`.
    """
    block: BlockType
    args: "Arguments"
    action: ActionType
    sub_action: None
    length: int
    data: None
    target: typing.Optional[Target]
    __slots__ = ()

    @classmethod
    def __subclasshook__(cls, o_cls: type):
        """
        Checks if the given class is a subclass of Action (implements it).
        :param o_cls: Class to check.
        :return: True if subclass; NotImplemented otherwise
        """

        if cls is ActionBlock:
            if Codeblock.__subclasshook__(o_cls) is NotImplemented:  # must be a Codeblock
                return NotImplemented

            try:
                if BlockType(getattr(o_cls, "block")) in (
                        BlockType.PLAYER_ACTION, BlockType.GAME_ACTION, BlockType.CONTROL, BlockType.ENTITY_ACTION
                ):
                    return True  # must be one of BlockType.PLAYER_ACTION or BlockType.GAME_ACTION
            except ValueError:  # not a valid block type
                return NotImplemented  # not an Action

        return NotImplemented  # #


class EventBlock(Codeblock, metaclass=abc.ABCMeta):
    """
    An ABC that describes any event - Player Event or Entity Event. Must implement :class:`Codeblock`.

    Includes all of :class:`Codeblock` 's attributes, plus:

    Attributes\u200b
    -----------
        block : Union[:attr:`~py2df.enums.parameters.BlockType.PLAYER_EVENT`, \
:attr:`~py2df.enums.action.BlockType.ENTITY_EVENT`]
            The block type - either `Player Event` or `Entity Event`.
    """
    block: BlockType
    args: None
    action: EventType
    sub_action: None
    length: int
    data: None
    target: None
    __slots__ = ()

    @classmethod
    def __subclasshook__(cls, o_cls: type):
        """
        Checks if the given class is a subclass of Event (implements it).
        :param o_cls: Class to check.
        :return: True if subclass; NotImplemented otherwise
        """

        if cls is EventBlock:
            if Codeblock.__subclasshook__(o_cls) is NotImplemented:
                return NotImplemented

            try:
                if BlockType(getattr(o_cls, "block")) in (BlockType.PLAYER_EVENT, BlockType.ENTITY_EVENT):  # be event.
                    return True
            except ValueError:  # not a valid block type
                return NotImplemented  # not an Event

        return NotImplemented


class BracketedBlock(Codeblock, metaclass=abc.ABCMeta):
    """
    An ABC that describes any codeblock with brackets. Can be used on a `with` construct. Must implement
    :class:`Codeblock`. This is only used for If-related and Repeat classes.

    For all the iterable-related methods, please refer to :class:`~collections.deque` .

    Attributes\u200b
    ----------

    block : Union[:attr:`~py2df.enums.parameters.IF_PLAYER`, :attr:`~py2df.enums.parameters.IF_ENTITY`, \
:attr:`~py2df.enums.parameters.IF_GAME`, :attr:`~py2df.enums.parameters.IF_VAR`, :attr:`~py2df.enums.parameters.REPEAT`]
        The type of block this is.

    args : :class:`~py2df.classes.collections.Arguments`
        The Arguments of this block.

    action : Union[:class:`~py2df.enums.enum_util.IfType`, :class:`~py2df.enums.utilityblock.RepeatType`]
        The condition (If)/specific type (Repeat) of this bracketed block.

    sub_action : Optional[:class:`~py2df.enums.enum_util.IfType`]
        If this is a Repeat and action is :attr:`~py2df.enums.utilityblock.RepeatType.WHILE_COND`,
        the condition to check (it will repeat while that condition is true).

    length : :class:`int`
        The length of this codeblock, excluding brackets, in Minecraft blocks. Should always be equal to 1.

    total_length : :class:`int`
        The sum of all lengths of all codeblocks inside this Bracketed Block, including itself and brackets
        (so, 3 + inner length).

    data : ``None``
        (Bracketed blocks do not have extra data.)

    codeblocks : Deque[:class:`Block`]
        The blocks (brackets and inner codeblocks) contained within this If.

    target : Optional[:class:`~py2df.enums.targets.Target`]
        The target of this If (for If Player and If Entity), or None for the current selection.
    """
    block: BlockType
    args: "Arguments"
    action: typing.Union[IfType, RepeatType]
    sub_action: typing.Optional[IfType]
    length: int = 1
    data: None = None
    codeblocks: typing.Deque[Block]
    target: typing.Optional[Target]
    __slots__ = ()

    @classmethod
    def __subclasshook__(cls, o_cls: type):
        """
        Checks if the given class is a subclass of BracketedBlock (implements it).
        :param o_cls: Class to check.
        :return: True if subclass; NotImplemented otherwise
        """

        if cls is BracketedBlock:
            if Codeblock.__subclasshook__(o_cls) is NotImplemented:  # must be a Codeblock
                return NotImplemented

            attribs = ["__exit__", "__enter__"]  # must have those attributes to be a bracket block. (Used in a `with`)
            if all(any(attr in B.__dict__ for B in o_cls.__mro__) for attr in attribs):
                return True

        return NotImplemented

    @abc.abstractmethod
    def __enter__(self):
        """Places the OPEN bracket. Can have two types: :attr:`~py2df.enums.parameters.BracketType.NORM`
        and :attr:`~py2df.enums.parameters.BracketType.REPEAT`
        """
        raise NotImplementedError

    @abc.abstractmethod
    def __exit__(self, *args):
        """Places the CLOSE bracket. Can have two types: :attr:`~py2df.enums.parameters.BracketType.NORM`
        and :attr:`~py2df.enums.parameters.BracketType.REPEAT`
        """
        raise NotImplementedError

    @property
    def total_length(self) -> int:
        """The total length of this Bracketed Block, in blocks. This sums the lengths of all codeblocks inside,
        including the If itself (1) and the two brackets (1 + 1 = 2).

        Returns
        -------
        :class:`int`
            The length.
        """

        def get_length(block: Block):
            return getattr(block, "total_length", block.length)

        return self.length + sum(map(get_length, self.codeblocks))

    def __iter__(self):
        for codeblock in self.codeblocks:
            yield codeblock

    def __contains__(self, item):
        return item in self.codeblocks or any(item in it for it in filter(
            lambda o: isinstance(o, BracketedBlock), self.codeblocks
        ))

    def __getitem__(self, item):
        return self.codeblocks.__getitem__(item)

    def __setitem__(self, key, value):
        return self.codeblocks.__setitem__(key, value)

    def __delitem__(self, key):
        return self.codeblocks.__delitem__(key)

    def append(self, item: Block):
        return self.codeblocks.append(item)

    def appendleft(self, item: Block):
        return self.codeblocks.appendleft(item)

    def extend(self, sequence: typing.Iterable[Block]):
        return self.codeblocks.extend(sequence)

    def extendleft(self, sequence: typing.Iterable[Block]):
        return self.codeblocks.extendleft(sequence)

    def pop(self, index: int):
        return self.codeblocks.pop(index)

    def popleft(self):
        return self.codeblocks.popleft()

    def rotate(self, n):
        return self.codeblocks.rotate(n)


class CallableBlock(Codeblock, FunctionHolder, metaclass=abc.ABCMeta):
    """An ABC that describes any callable - Function or Process. Must implement :class:`Codeblock` and
    :class:`FunctionHolder`.

    Used to define a line of code that can be called with a Call Function (Function) or Start Process (Process)
    block. Decorator. Example usage::

            @Function(name="My Function")  # 'hidden' is False by default
            def my_function():
                # code

            @Process(name="Some Process", hidden=False)
            def some_process():
                # code

            @Function  # default name is the function's name as Capitalized Words.
            def cool_function():  # in this case, the name will be 'Cool Function'
                # code

    Parameters
    ----------\u200b
    name_or_func : Union[:class:`str`, Callable]
        Can be either the proper Python function containing the code to be run when this Function/Process is called,
        or the name of this Function/Process (its :attr:`data`).

    hidden : :class:`bool`, optional
        Whether or not this function/process is hidden in the Call Function/Start Process menu.
        Defaults to ``False``.

    item_icon : Optional[:class:`~py2df.classes.mc_types.Item`], optional
        An optional item that represents this Function/Process in the Call Function/Start Process menu.

    Warnings
    --------\u200b
    The function name cannot exceed 16 characters.

    Attributes
    ----------\u200b
    block : Union[:attr:`~py2df.enums.parameters.BlockType.FUNCTION`, \
:attr:`~py2df.enums.parameters.BlockType.PROCESS`]
        The type of the callable block - `Function` or `Process`.

    args : :attr:`~py2df.classes.collections.Arguments`
        The item arguments of the Callable codeblock (containing the Hidden tag, i.e., whether or not it is hidden in
        the Call Function (Function)/Start Process (Process) menu).

    action : ``None``
        (Callable codeblocks have no action.)

    sub_action : ``None``
        (Callable codeblocks have no sub-actions.)

    function : Callable
        The Python function containing this Function's code.

    item_icon : Optional[:class:`~py2df.classes.mc_types.Item`]
        An optional item that represents this Function/Process in the Call Function/Start Process menu.

    length : :class:`int`
        The length of a Function/Process codeblock, in blocks. This is always 2.

    name : :class:`str`
        The name of this function/process. Note that **this cannot exceed 16 characters**.

    data : :class:`str`
        The name of this function/process (same as :attr:`name`).

    hidden : :class:`bool`
        Whether or not this function/process is hidden in the Call Function/Start Process menu.
        Defaults to ``False``.

    target : ``None``
        (Callable codeblocks have no targets.)
    """
    __slots__ = ("data", "hidden", "function", "item_icon")
    block: BlockType
    args: "Arguments"
    action: None = None
    sub_action: None = None
    function: typing.Callable
    item_icon: typing.Optional["Item"]
    length: int = 2
    data: str  # Name
    hidden: bool
    target: None = None

    def __init__(
        self, name_or_func: typing.Union[str, typing.Callable],
        *, hidden: bool = False, item_icon: typing.Optional["Item"] = None
    ):
        """
        Parameters
        ----------
        name_or_func : Union[:class:`str`, Callable]
            Can be either the proper Python function containing the code,
            or the name of this Function/Process (its :attr:`data`).

        hidden : :class:`bool`, optional
            Whether or not this Function/Process is hidden in the Call Function (Function)/Start Process (Process)
            menu. Defaults to ``False``.
        """
        self.function: typing.Callable = typing.cast(typing.Callable, None)
        if callable(name_or_func):  # the class was used directly as a decorator
            self.data: str = str(snake_to_capitalized_words(name_or_func.__name__))
            self.__call__(name_or_func)
        else:  # generate decorator
            self.data: str = str(name_or_func)

        self.name = self.data  # run checks
        self.hidden: bool = bool(hidden)

        self.item_icon: Item = item_icon

    @property
    def name(self) -> str:
        """The name of this function/process."""
        return self.data

    @name.setter
    def name(self, new_name: str) -> None:
        string = str(new_name)
        if len(string) > constants.MAX_FUNC_NAME_LEN:
            raise ValueError(
                f"{self.__class__.__name__} name must not exceed {constants.MAX_FUNC_NAME_LEN} characters."
            )
        self.data = str(new_name)

    @property
    @abc.abstractmethod  # abstract to avoid cyclic import between abc and collections
    def args(self) -> "Arguments":
        raise NotImplementedError

    @abc.abstractmethod
    def __call__(self, func: typing.Callable) -> "CallableBlock":  # decorate
        """Decorator for storing this function/process and its line of code.

        Parameters
        ----------
        func : Callable
            The Python function containing the code that will be run when this function/process is invoked
            by a Call Function (Function)/Start Process (Process) block.

        Returns
        -------
        :class:`CallableBlock`
            self (The final Callable Block - either a :class:`~py2df.reading.callable_decorators.Function`
            or a :class:`~py2df.reading.callable_decorators.Process`)

        Warnings
        --------
        This appends the Callable Block to the :class:`~py2df.reading.reader.DFReader` singleton.
        """
        raise NotImplementedError

    @classmethod
    def __subclasshook__(cls, o_cls: type):
        """
        Checks if the given class is a subclass of CallableBlock (implements it).
        :param o_cls: Class to check.
        :return: True if subclass; NotImplemented otherwise
        """

        if cls is CallableBlock:
            if Codeblock.__subclasshook__(o_cls) is NotImplemented:
                return NotImplemented

            try:
                if BlockType(getattr(o_cls, "block")) in (BlockType.FUNCTION, BlockType.PROCESS):
                    return True
            except ValueError:  # not a valid block type
                return NotImplemented  # not a CallableBlock

        return NotImplemented


class CallerBlock(Codeblock, metaclass=abc.ABCMeta):
    """An ABC that describes any caller - Call Function or Start Process. Must implement :class:`Codeblock`.

    Attributes\u200b
    ------------
    block : Union[:attr:`~py2df.enums.parameters.BlockType.CALL_FUNC`, \
:attr:`~py2df.enums.parameters.BlockType.START_PROCESS`]
        The type of the callable block - `Call Function` or `Start Process`.

    args : ``None``
        (Caller codeblocks have no arguments.)

    action : ``None``
        (Caller codeblocks have no action.)

    sub_action : ``None``
        (Caller codeblocks have no sub-actions.)

    length : :class:`int`
        The length of a Caller codeblock, in blocks. This is always 2.

    name : :class:`str`
        The name of the function/process to call. Note that **this cannot exceed 16 characters.**

    data : :class:`str`
        The name of the function/process to call (same as :attr:`name`).

    target : ``None``
        (Caller codeblocks have no targets.)
    """
    block: BlockType
    args: None
    action: None
    sub_action: None
    length: int
    data: str  # Name
    target: None
    __slots__ = ()

    @property
    def name(self) -> str:
        """The name of the function/process to call."""
        return self.data

    @name.setter
    def name(self, new_name: str) -> None:
        string = str(new_name)
        if len(string) > constants.MAX_FUNC_NAME_LEN:
            raise ValueError(
                f"{self.__class__.__name__} name must not exceed {constants.MAX_FUNC_NAME_LEN} characters."
            )
        self.data = str(new_name)

    @classmethod
    def __subclasshook__(cls, o_cls: type):
        """
        Checks if the given class is a subclass of CallerBlock (implements it).
        :param o_cls: Class to check.
        :return: True if subclass; NotImplemented otherwise
        """

        if cls is CallableBlock:
            if Codeblock.__subclasshook__(o_cls) is NotImplemented:
                return NotImplemented

            try:
                if BlockType(getattr(o_cls, "block")) in (BlockType.CALL_FUNC, BlockType.START_PROCESS):
                    return True
            except ValueError:  # not a valid block type
                return NotImplemented  # not a CallerBlock

        return NotImplemented


class UtilityBlock(Codeblock, metaclass=abc.ABCMeta):
    """An ABC that describes any utility block - Set Var, Select Object or Repeat. Must implement :class:`Codeblock`.

    Includes all of :class:`Codeblock` 's attributes, plus:

    Attributes\u200b
    ------------
        block : Union[:attr:`~py2df.enums.parameters.BlockType.REPEAT`, \
:attr:`~py2df.enums.parameters.BlockType.SELECT_OBJ`, :attr:`~py2df.enums.parameters.BlockType.SET_VAR`]
            The type of the utility block - `Set Var`, `Select Object` or `Repeat`.
    """
    block: BlockType
    args: None
    action: None
    sub_action: typing.Optional[CodeblockActionType]
    length: int
    data: str  # Name
    target: None
    __slots__ = ()

    @classmethod
    def __subclasshook__(cls, o_cls: type):
        """
        Checks if the given class is a subclass of UtilityBlock (implements it).
        :param o_cls: Class to check.
        :return: True if subclass; NotImplemented otherwise
        """

        if cls is CallableBlock:
            if Codeblock.__subclasshook__(o_cls) is NotImplemented:
                return NotImplemented

            try:
                if BlockType(getattr(o_cls, "block")) in (BlockType.SET_VAR, BlockType.REPEAT, BlockType.SELECT_OBJ):
                    return True
            except ValueError:  # not a valid block type
                return NotImplemented  # not an UtilityBlock

        return NotImplemented


# endregion:Codeblock

_abc_classes = (
    Block, Codeblock, EventBlock, BracketedBlock, CallableBlock, ActionBlock, CallerBlock, UtilityBlock,
    JSONData, BuildableJSONData, Itemable, Settable, FunctionHolder, DFType
)
remove_u200b_from_doc(_abc_classes)
