"""Utility enums module.

This module contains auxiliary enums enriched with quality of life functions.
"""

import enum

__all__ = ['IntEnumMember']


class IntEnumMember(enum.IntEnum):
    """Integer enum base class with member value method."""

    @classmethod
    def has_value(cls, value: int) -> bool:
        """Check if enum contains member.

        Args:
            value (int): Value to find in enum

        Returns:
            :obj`bool`: True if value is member of enum, False otherwise
        """
        return value in cls._value2member_map_
