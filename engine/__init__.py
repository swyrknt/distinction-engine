"""
Core distinction engine package.

This package contains the fundamental distinction.py module which defines
the core Distinction and DistinctionEngine classes that all other packages
observe and build upon.
"""

from .distinction import Distinction, DistinctionEngine

__all__ = ['Distinction', 'DistinctionEngine']
