from typing import TYPE_CHECKING, Any

from pydantic import ConfigDict, Field, PrivateAttr

from bit.model import BaseModel

if TYPE_CHECKING:
    from bit.protocol import BaseProtocol


class MessageContext(BaseModel):
    """Message context."""

    model_config = ConfigDict(arbitrary_types_allowed=True)

    data: dict[str, Any] = Field(
        default_factory=dict,
        description="Additional data.",
    )

    protocol: "BaseProtocol"


class BaseMessage(BaseModel):
    _ctx: MessageContext | None = PrivateAttr(None)

    @property
    def ctx(self) -> MessageContext | None:
        return self.__pydantic_private__["_ctx"]  # noqa: unresolved-reference

    def set_context(self, context: MessageContext | dict[str, Any]) -> None:
        """Sets the context for the message."""

        self._ctx = context
