from .base import PolymorphicMatcher, CaseAction
from . import error
from .error import *
from .registry import pattern_registry

__version__ = "0.2.0"

__all__ = ("PolymorphicMatcher","CaseAction", "pattern_registry")
__all__ += error.__all__
