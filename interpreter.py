from lexer import tokenize
from parser import Parser, Number, String, Var, BinOp, Assign

class Interpreter:
    def __init__(self):
        self.env = {}  

    def interpret(self, node):
        method_name = f'visit_{type(node).__name__}'
        method = getattr(self, method_name, self.generic_visit)
        return method(node)

    def generic_visit(self, node):
        raise Exception(f'No visit_{type(node).__name__} method')

    def visit_Number(self, node):
        return node.value

    def visit_String(self, node):
        return node.value

    def visit_Var(self, node):
        if node.name not in self.env:
            raise Exception(f"Runtime Error: Undefined variable '{node.name}'")
        return self.env[node.name]

    def visit_BinOp(self, node):
        left_val = self.interpret(node.left)
        right_val = self.interpret(node.right)

        if node.op == '+':
            return left_val + right_val
        elif node.op == '-':
            return left_val - right_val
        elif node.op == '*':
            return left_val * right_val
        elif node.op == '/':
            return left_val / right_val
        else:
            raise Exception(f"Runtime Error: Unknown operator '{node.op}'")

    def visit_Assign(self, node):
        value = self.interpret(node.value)
        self.env[node.name] = value
        return value


if __name__ == "__main__":
    code = '''
    x = 5 + 2
    y = "hello"
    z = x + 3
    w = y + " world"
    '''

    tokens = tokenize(code)
    parser = Parser(tokens)
    interpreter = Interpreter()

    for line in code.strip().splitlines():
        if not line.strip():
            continue
        tokens = tokenize(line.strip())
        parser = Parser(tokens)
        ast = parser.parse()

        for node in ast:
            result = interpreter.interpret(node)

    print("\nFinal Environment:")
    for name, value in interpreter.env.items():
        print(f"{name} = {value}")