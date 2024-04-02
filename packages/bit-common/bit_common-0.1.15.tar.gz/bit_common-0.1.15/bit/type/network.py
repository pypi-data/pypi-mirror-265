import ipaddress
from typing import Any, ClassVar, Self, Union

from pydantic_core import core_schema

from bit.type.integer import UnsignedInteger


class IPv4Address(UnsignedInteger):
    LENGTH = 32
    EXTRA: ClassVar[type] = ipaddress.IPv4Address

    @classmethod
    def transform(cls, value: Union[str, int, list[int]]) -> int:
        if isinstance(value, str):
            return int(cls.EXTRA(value))

        return super().transform(value)

    @classmethod
    def _validate(
        cls,
        value: Union[str, int, list[int], Self],
        info: dict[str, Any] | core_schema.ValidationInfo,
    ) -> int:

        if isinstance(value, str):
            return int(cls.EXTRA(value))

        return super()._validate(value, info)

    def __repr__(self):
        return str(self.EXTRA(self.value))


class IPv6Address(IPv4Address):
    LENGTH = 128
    EXTRA: ClassVar[type] = ipaddress.IPv6Address


class IPv4Mask(IPv4Address):
    pass


class IPv6Mask(IPv6Address):
    pass


class MACAddress(UnsignedInteger):
    LENGTH = 48

    def __repr__(self):
        hex_data = f"{self.value:012x}"
        return ":".join([hex_data[i : i + 2] for i in range(0, len(hex_data), 2)])
