import pytest
import sys
import os

# Add parent directory to path to import math module
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from math import add, subtract


class TestMath:
    """Test class for math operations"""

    def test_add(self):
        """Test addition"""
        assert add(2, 3) == 5
        assert add(-1, 1) == 0
        assert add(0, 0) == 0

    def test_subtract(self):
        """Test subtraction"""
        assert subtract(5, 3) == 2
        assert subtract(0, 5) == -5
        assert subtract(-1, -1) == 0

    def test_add_floats(self):
        """Test addition with floats"""
        assert add(2.5, 3.5) == 6.0
        assert add(0.1, 0.2) > 0.2  # Floating point check

    def test_subtract_floats(self):
        """Test subtraction with floats"""
        assert subtract(5.5, 2.5) == 3.0


def test_add_simple():
    """Simple standalone test"""
    assert add(1, 1) == 2


def test_subtract_simple():
    """Simple standalone test"""
    assert subtract(10, 5) == 5