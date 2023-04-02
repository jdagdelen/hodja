"""Tools for math."""

from hodja.tools.base import Tool

class MathTool(Tool):
    """Example tool that evaluates simple math expressions."""

    def __init__(self, name="Math", description="Evaluate a math expression. Note: only numbers and basic operators (e.g. +-*/) are allowed.", instructions="Enter a math expression."):
        super().__init__(name=name, description=description, instructions=instructions)

    def run(self, input):
        # check if input is a math expression (e.g. numbers and math operators only)
        # if not, raise an error
        allowed_characters = "0123456789+-*/.,"
        for character in input:
            if character not in allowed_characters:
                raise ValueError("Invalid input. Only numbers, decimals (.), commas (,), and math operators (+-*/) are allowed.")
        # evaluate the math expression
        return eval(input)


class FibonacciTool(Tool):
    """Example tool that returns the nth Fibonacci number."""

    def __init__(self, name="Fibonacci", description="Returns the nth Fibonacci number", instructions="Enter a number n."):
        super().__init__(name, description, instructions)

    def run(self, n):
        # check if input is a number
        # if not, raise an error
        try:
            n = int(n)
        except:
            raise ValueError("Invalid input. Only numbers are allowed.")
        
        def _fib(n):
            if n <= 1:
                return n
            else:
                return _fib(n-1) + _fib(n-2)
            
        return _fib(n+1)