"""
Compatibility module for supporting older Python versions.

This module provides fallbacks for features introduced in newer Python versions:
- StrEnum (Python 3.11+)
- tomllib (Python 3.11+)
- Self type hint (Python 3.11+)
"""

import sys
from enum import Enum

# Python version check
PY_VERSION = sys.version_info[:2]

# =============================================================================
# StrEnum compatibility (Python 3.11+)
# =============================================================================
if PY_VERSION >= (3, 11):
    from enum import StrEnum
else:
    class StrEnum(str, Enum):
        """
        Backport of StrEnum for Python < 3.11.
        
        StrEnum is a string enum that ensures all members are strings,
        and string comparison works as expected.
        """
        def __new__(cls, value):
            if not isinstance(value, str):
                raise TypeError(f"StrEnum values must be strings, got {type(value).__name__}")
            member = str.__new__(cls, value)
            member._value_ = value
            return member

        def __str__(self):
            return str(self._value_)

        @staticmethod
        def _generate_next_value_(name, start, count, last_values):
            """
            Return the name as the value for auto().
            """
            return name.lower()


# =============================================================================
# tomllib compatibility (Python 3.11+)
# =============================================================================
if PY_VERSION >= (3, 11):
    import tomllib
else:
    try:
        import tomli as tomllib
    except ImportError:
        raise ImportError(
            "tomllib is not available. For Python < 3.11, install the 'tomli' package: "
            "pip install tomli"
        )


# =============================================================================
# Self type hint compatibility (Python 3.11+)
# =============================================================================
if PY_VERSION >= (3, 11):
    from typing import Self
else:
    try:
        from typing_extensions import Self
    except ImportError:
        raise ImportError(
            "Self is not available. For Python < 3.11, install the 'typing-extensions' package: "
            "pip install typing-extensions"
        )


__all__ = ["StrEnum", "tomllib", "Self", "PY_VERSION"]
