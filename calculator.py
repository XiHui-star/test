"""Simple command-line calculator supporting addition, subtraction,
multiplication, and division.

Usage:
    python calculator.py <number1> <operator> <number2>

Operators:
    +   addition
    -   subtraction
    *   multiplication
    /   division

If run without command-line arguments the program will prompt the user to
enter the values interactively.
"""
from __future__ import annotations

import operator
import sys
from typing import Callable, Dict

Operation = Callable[[float, float], float]


class CalculatorError(Exception):
    """Custom exception for calculator errors."""


def get_operations() -> Dict[str, Operation]:
    """Return a mapping of operator symbols to their corresponding functions."""

    return {
        "+": operator.add,
        "-": operator.sub,
        "*": operator.mul,
        "/": operator.truediv,
    }


def calculate(lhs: float, op: str, rhs: float) -> float:
    """Perform the requested calculation.

    Args:
        lhs: Left-hand side value.
        op: Operator symbol as a string.
        rhs: Right-hand side value.

    Returns:
        Result of applying the operator to the operands.

    Raises:
        CalculatorError: If an invalid operator is provided or division by zero occurs.
    """

    operations = get_operations()
    if op not in operations:
        raise CalculatorError(f"Unsupported operator: {op}")

    if op == "/" and rhs == 0:
        raise CalculatorError("Division by zero is not allowed")

    return operations[op](lhs, rhs)


def parse_args(args: list[str]) -> tuple[float, str, float]:
    """Parse command-line arguments and return operands and operator."""

    if len(args) != 3:
        raise CalculatorError("Expected usage: <number1> <operator> <number2>")

    lhs_str, op, rhs_str = args
    try:
        lhs = float(lhs_str)
        rhs = float(rhs_str)
    except ValueError as exc:  # pragma: no cover - defensive
        raise CalculatorError("Operands must be numeric values") from exc

    return lhs, op, rhs


def main(argv: list[str] | None = None) -> int:
    """Entry point for the calculator CLI."""

    if argv is None:
        argv = sys.argv[1:]

    try:
        if argv:
            lhs, op, rhs = parse_args(argv)
        else:
            lhs = float(input("Enter the first number: "))
            op = input("Enter the operator (+, -, *, /): ")
            rhs = float(input("Enter the second number: "))

        result = calculate(lhs, op, rhs)
    except CalculatorError as err:
        print(f"Error: {err}", file=sys.stderr)
        return 1
    except ValueError as err:
        print(f"Invalid numeric input: {err}", file=sys.stderr)
        return 1

    print(f"Result: {result}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
