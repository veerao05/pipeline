"""Math module with basic arithmetic operations."""


def add(a: float, b: float) -> float:
    """Simple function to add two numbers.

    Args:
        a: First number
        b: Second number

    Returns:
        Sum of a and b
    """
    return a + b


def subtract(a: float, b: float) -> float:
    """Simple function to subtract two numbers.

    Args:
        a: First number
        b: Second number

    Returns:
        Difference of a and b
    """
    return a - b


if __name__ == "__main__":
    print("Math module loaded")
    print(f"Add: {add(2, 3)}")
    print(f"Subtract: {subtract(5, 2)}")
    
    # Keep the container running
    import time
    time.sleep(3600)
