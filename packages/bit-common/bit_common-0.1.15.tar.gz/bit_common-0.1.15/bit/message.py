from typing import Any, ClassVar

from pydantic import ConfigDict, Field, PrivateAttr

from bit.model import BaseModel
from bit.protocol import BaseProtocol


class MessageContext(BaseModel):
    """Message context."""

    model_config = ConfigDict(arbitrary_types_allowed=True)

    data: dict[str, Any] = Field(
        default_factory=dict,
        description="Additional data.",
    )

    protocol: BaseProtocol


class BaseMessage(BaseModel):
    ctx_model: ClassVar[type[MessageContext]] = MessageContext
    _ctx: MessageContext | None = PrivateAttr(None)

    @property
    def ctx(self) -> MessageContext | None:
        return self.__pydantic_private__["_ctx"]  # noqa: unresolved-reference

    def set_context(self, context: MessageContext | dict[str, Any]) -> None:
        """Sets the context for the message."""

        self._ctx = self.ctx_model.parse_obj(context) if isinstance(context, dict) else context
