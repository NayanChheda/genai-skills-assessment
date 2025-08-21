# src/basics/math_utils.py

from typing import List

__all__: list[str] = ["add", "factorial", "fibonacci"]


def add(a: int, b: int) -> int:
    """Return the sum of two integers."""
    return a + b


def factorial(n: int) -> int:
    """Return factorial of n."""
    raise NotImplementedError("Implement factorial function")


def fibonacci(n: int) -> List[int]:
    """Return a list of first n Fibonacci numbers."""
    raise NotImplementedError("Implement fibonacci function")
