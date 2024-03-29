# This file was auto-generated by Fern from our API Definition.

import datetime as dt
import typing

from ..core.datetime_utils import serialize_datetime
from .entity_status import EntityStatus
from .environment_enum import EnvironmentEnum
from .vellum_variable import VellumVariable

try:
    import pydantic.v1 as pydantic  # type: ignore
except ImportError:
    import pydantic  # type: ignore


class SlimWorkflowDeployment(pydantic.BaseModel):
    id: str
    name: str = pydantic.Field(
        description="A name that uniquely identifies this workflow deployment within its workspace"
    )
    label: str = pydantic.Field(description="A human-readable label for the workflow deployment")
    status: typing.Optional[EntityStatus] = pydantic.Field(
        description=(
            "The current status of the workflow deployment\n" "\n" "- `ACTIVE` - Active\n" "- `ARCHIVED` - Archived\n"
        )
    )
    environment: typing.Optional[EnvironmentEnum] = pydantic.Field(
        description=(
            "The environment this workflow deployment is used in\n"
            "\n"
            "- `DEVELOPMENT` - Development\n"
            "- `STAGING` - Staging\n"
            "- `PRODUCTION` - Production\n"
        )
    )
    created: dt.datetime
    last_deployed_on: dt.datetime
    input_variables: typing.List[VellumVariable] = pydantic.Field(
        description="The input variables this Workflow Deployment expects to receive values for when it is executed."
    )
    output_variables: typing.List[VellumVariable] = pydantic.Field(
        description="The output variables this Workflow Deployment will produce when it is executed."
    )

    def json(self, **kwargs: typing.Any) -> str:
        kwargs_with_defaults: typing.Any = {"by_alias": True, "exclude_unset": True, **kwargs}
        return super().json(**kwargs_with_defaults)

    def dict(self, **kwargs: typing.Any) -> typing.Dict[str, typing.Any]:
        kwargs_with_defaults: typing.Any = {"by_alias": True, "exclude_unset": True, **kwargs}
        return super().dict(**kwargs_with_defaults)

    class Config:
        frozen = True
        smart_union = True
        json_encoders = {dt.datetime: serialize_datetime}
