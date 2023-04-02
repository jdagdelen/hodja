"""Tools for math."""

from hodja.tools.base import Tool

class MathTool(Tool):
    """Example tool that evaluates simple math expressions."""

    def __init__(self, name="Math", description="Evaluate a math expression. Note: only numbers and basic operators (e.g. +-*/) are allowed.", instructions="Enter a math expression."):
        super().__init__(name, description, instructions)

    def run(self, input):
        # check if input is a math expression (e.g. numbers and math operators only)
        # if not, raise an error
        print("Running Math: " + input)
        allowed_characters = "0123456789+-*/"
        for character in input:
            if character not in allowed_characters:
                raise ValueError("Invalid input. Only numbers and math operators (+-*/) are allowed.")
        # evaluate the math expression
        return eval(input)


class FibonacciTool(Tool):
    """Example tool that calculates the Fibonacci numbers up to f_n and returns them as a list."""

    def __init__(self, name="Fibonacci", description="Get the Fibonacci numbers up to f_n.", instructions="Enter a number n."):
        super().__init__(name, description, instructions)

    def run(self, n):
        # check if input is a number
        # if not, raise an error
        try:
            n = int(n)
        except:
            raise ValueError("Invalid input. Only numbers are allowed.")
        
        # calculate the Fibonacci numbers
        fibonacci_numbers = [0, 1]
        for i in range(2, n):
            fibonacci_numbers.append(fibonacci_numbers[i-1] + fibonacci_numbers[i-2])
        return fibonacci_numbers
