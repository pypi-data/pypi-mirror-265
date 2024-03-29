# This file was auto-generated by Fern from our API Definition.

import enum
import typing

T_Result = typing.TypeVar("T_Result")


class MetadataFilterRuleCombinator(str, enum.Enum):
    """
    - `and` - AND
    - `or` - OR
    """

    AND = "and"
    OR = "or"

    def visit(self, and_: typing.Callable[[], T_Result], or_: typing.Callable[[], T_Result]) -> T_Result:
        if self is MetadataFilterRuleCombinator.AND:
            return and_()
        if self is MetadataFilterRuleCombinator.OR:
            return or_()
