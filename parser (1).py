"""Simple Arithmetic Interpreter.

Grammar (EBNF):
    expression = term, { ("+" | "-"), term } ;
    term       = factor, { "*", factor } ;
    factor     = integer | "(", expression, ")" ;
    integer    = digit, { digit } ;
    digit      = "0" | "1" | "2" | "3" | "4" | "5" | "6" | "7" | "8" | "9" ;
"""


class ASTNode:
    pass


class NumberNode(ASTNode):
    def __init__(self, value):
        self.value = value


class BinaryOpNode(ASTNode):
    def __init__(self, left, op, right):
        self.left = left
        self.op = op
        self.right = right


class Parser:
    def __init__(self, expression):
        self.expr = expression.replace(' ', '')
        self.pos = 0
        self.current_char = self.expr[0] if self.expr else None

    def advance(self):
        self.pos += 1
        self.current_char = self.expr[self.pos] if self.pos < len(self.expr) else None

    def parse_number(self):
        # Read all consecutive digits as a single positive integer.
        if self.current_char is None or not self.current_char.isascii() or not self.current_char.isdigit():
            raise ValueError(f"Expected a number at position {self.pos}")
        digits = []
        while self.current_char is not None and self.current_char.isascii() and self.current_char.isdigit():
            digits.append(self.current_char)
            self.advance()
        return NumberNode(int(''.join(digits)))

    def parse_factor(self):
        # A factor is an integer or an expression inside parentheses.
        if self.current_char == '(':
            self.advance()
            node = self.parse_expression()
            if self.current_char != ')':
                raise ValueError(f"Expected ')' at position {self.pos}")
            self.advance()
            return node
        return self.parse_number()

    def parse_term(self):
        # Multiplication binds more tightly than addition and subtraction.
        node = self.parse_factor()
        while self.current_char == '*':
            op = self.current_char
            self.advance()
            node = BinaryOpNode(node, op, self.parse_factor())
        return node

    def parse_expression(self):
        # Build left-associative addition and subtraction nodes.
        node = self.parse_term()
        while self.current_char in ('+', '-'):
            op = self.current_char
            self.advance()
            node = BinaryOpNode(node, op, self.parse_term())
        return node


def evaluate(node):
    # Evaluate the syntax tree recursively, starting with its children.
    if isinstance(node, NumberNode):
        return node.value
    if isinstance(node, BinaryOpNode):
        left = evaluate(node.left)
        right = evaluate(node.right)
        if node.op == '+':
            return left + right
        if node.op == '-':
            return left - right
        if node.op == '*':
            return left * right
    raise ValueError('Unknown AST node or operator')


def interpret(expression):
    parser = Parser(expression)
    ast = parser.parse_expression()
    # Reject unconsumed characters rather than silently ignoring bad input.
    if parser.current_char is not None:
        raise ValueError(f"Unexpected character '{parser.current_char}' at position {parser.pos}")
    return evaluate(ast)


# Test cases
if __name__ == "__main__":
    test_expressions = [
        "42",
        "2 + 3",
        "10 - 4",
        "3 * 7",
        "2 + 3 * 4",
        "(2 + 3) * 4",
        "1 + 2 + 3",
        "10 - 5 - 2",
        "((1 + 2) * 3) - 4"
    ]

    print("Justice Williamson")
    print("Arithmetic Interpreter Test")
    for expr in test_expressions:
        try:
            result = interpret(expr)
            print(f"{expr} = {result}")
        except Exception as e:
            print(f"Error interpreting '{expr}': {e}")
