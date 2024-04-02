from typing import Self


class Calculator:
    """
    Calculator class, keeping track of current result and supporting addition, subtraction, multiplication, division and
    taking nth root.
    """

    def __init__(self: Self) -> None:
        """ Initialize an instance with current result 0. """
        self.__result = 0
        self.__expression = f"{self.__result}"
        self.__previous_operator_precedence = 2

    def __str__(self: Self) -> str:
        """ Return current equation as a string. """
        return f"{self.__expression} = {self.__result}"

    def add(self: Self, addend: float) -> Self:
        """ Add the argument passed to current result and return self. """
        self.__result += addend
        self.__expression = f"{self.__expression} + {addend}"
        self.__previous_operator_precedence = 0
        return self

    def subtract(self: Self, subtrahend: float) -> Self:
        """ Subtract the argument passed to current result and return self. """
        self.__result -= subtrahend
        self.__expression = f"{self.__expression} - {subtrahend}"
        self.__previous_operator_precedence = 0
        return self

    def multiply_by(self: Self, factor: float) -> Self:
        """ Multiply current result by the argument passed and return self. """
        self.__result *= factor
        self.__expression = (
            f"({self.__expression}) × {factor}" if self.__previous_operator_precedence < 1
            else f"{self.__expression} × {factor}"
        )
        self.__previous_operator_precedence = 1
        return self

    def divide_by(self: Self, divisor: float) -> Self:
        """ Divide current result by the argument passed (cannot be 0) and return self. """
        if divisor == 0:
            raise ValueError("Division by 0 is undefined")
        self.__result /= divisor
        self.__expression = (
            f"({self.__expression}) / {divisor}" if self.__previous_operator_precedence < 1
            else f"{self.__expression} / {divisor}"
        )
        self.__previous_operator_precedence = 1
        return self

    def take_nth_root(self: Self, index: float) -> Self:
        """ Take nth root (index is the argument passed) of the current result and return self. """
        if index == 0:
            raise ValueError("0th root is undefined")
        exponent = 1.0 / index
        self.__result = (-1 if self.__result < 0 else 1) * pow(abs(self.__result), exponent)
        self.__expression = (
            f"({self.__expression}) ^ {exponent}" if self.__previous_operator_precedence < 2
            else f"{self.__expression} ^ {exponent}"
        )
        self.__previous_operator_precedence = 2
        return self

    def reset_memory(self: Self) -> Self:
        """ Reset current result back to 0 and return self. """
        self.__init__()
        return self

    @property
    def result(self: Self) -> float:
        """ Return current result. """
        return self.__result
