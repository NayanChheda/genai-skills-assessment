from src.basics.math_utils import add, factorial, fibonacci


def test_add() -> None:
    assert add(2, 3) == 5


def test_factorial() -> None:
    assert factorial(0) == 1
    assert factorial(5) == 120


def test_fibonacci() -> None:
    assert fibonacci(1) == [0]
    assert fibonacci(5) == [0, 1, 1, 2, 3]
