# This file was auto-generated by Fern from our API Definition.

import enum
import typing

T_Result = typing.TypeVar("T_Result")


class BlockTypeEnum(str, enum.Enum):
    """
    - `CHAT_MESSAGE` - CHAT_MESSAGE
    - `CHAT_HISTORY` - CHAT_HISTORY
    - `JINJA` - JINJA
    - `FUNCTION_DEFINITION` - FUNCTION_DEFINITION
    """

    CHAT_MESSAGE = "CHAT_MESSAGE"
    CHAT_HISTORY = "CHAT_HISTORY"
    JINJA = "JINJA"
    FUNCTION_DEFINITION = "FUNCTION_DEFINITION"

    def visit(
        self,
        chat_message: typing.Callable[[], T_Result],
        chat_history: typing.Callable[[], T_Result],
        jinja: typing.Callable[[], T_Result],
        function_definition: typing.Callable[[], T_Result],
    ) -> T_Result:
        if self is BlockTypeEnum.CHAT_MESSAGE:
            return chat_message()
        if self is BlockTypeEnum.CHAT_HISTORY:
            return chat_history()
        if self is BlockTypeEnum.JINJA:
            return jinja()
        if self is BlockTypeEnum.FUNCTION_DEFINITION:
            return function_definition()
