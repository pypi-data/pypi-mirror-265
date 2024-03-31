from public import public as _public

from ._enum import Enum, EnumValue, IntEnum


__version__ = '6.1.0'


_public(
    Enum=Enum,
    EnumValue=EnumValue,
    IntEnum=IntEnum,
    __version__=__version__,
)


del _public
