import pytest
import sys
import os

# Add parent directory to path to import our custom math module
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import from our custom my_math module (not the built-in math module)
import my_math as our_math


class TestMath:
    """Test class for math operations"""

    def test_add(self):
        """Test addition"""
        assert our_math.add(2, 3) == 5
        assert our_math.add(-1, 1) == 0
        assert our_math.add(0, 0) == 0

    def test_subtract(self):
        """Test subtraction"""
        assert our_math.subtract(5, 3) == 2
        assert our_math.subtract(0, 5) == -5
        assert our_math.subtract(-1, -1) == 0

    def test_add_floats(self):
        """Test addition with floats"""
        assert our_math.add(2.5, 3.5) == 6.0
        assert our_math.add(0.1, 0.2) > 0.2  # Floating point check

    def test_subtract_floats(self):
        """Test subtraction with floats"""
        assert our_math.subtract(5.5, 2.5) == 3.0


def test_add_simple():
    """Simple standalone test"""
    assert our_math.add(1, 1) == 2


def test_subtract_simple():
    """Simple standalone test"""
    assert our_math.subtract(10, 5) == 5
