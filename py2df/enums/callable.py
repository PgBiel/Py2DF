from enum import auto, unique

from .enum_util import TagType, AutoSnakeToPascalCaseNameEnum, CodeblockActionType, AutoLowerNameEnum


@unique
class CallableAction(CodeblockActionType, AutoLowerNameEnum):
    """This is only used for the Function/Process 'Is Hidden' tag, and provides the type of action of it. (There is only
    one: :attr:`DYNAMIC`.)"""
    DYNAMIC = auto()


@unique
class CallableHiddenTag(TagType, AutoSnakeToPascalCaseNameEnum):
    TRUE = auto()
    FALSE = auto()
