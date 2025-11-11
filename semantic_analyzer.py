from lexer import tokenize
from parser import Parser, Number, String, Var, BinOp, Assign

class SemanticAnalyzer:
    def __init__(self):
        self.symbols = {}

    def visit_list(self, node_list):
        for node in node_list:
            self.analyze(node)

    def analyze(self, node):
        if isinstance(node, list):  # <--- handle list of nodes
            return self.visit_list(node)
        method_name = f'visit_{type(node).__name__}'
        method = getattr(self, method_name, self.generic_visit)
        return method(node)

    def generic_visit(self, node):
        raise Exception(f'No visit_{type(node).__name__} method')

    def visit_Number(self, node):
        return 'int'

    def visit_String(self, node):
        return 'string'

    def visit_Var(self, node):
        if node.name not in self.symbols:
            raise Exception(f"Semantic Error: Undeclared variable '{node.name}'")
        return self.symbols[node.name]

    def visit_BinOp(self, node):
        left_type = self.analyze(node.left)
        right_type = self.analyze(node.right)

        if left_type != right_type:
            raise Exception(
                f"Type Error: cannot apply '{node.op}' between {left_type} and {right_type}"
            )

        # numeric ops (+, -, *, /)
        if left_type == 'int' and right_type == 'int':
            return 'int'
        # string concatenation
        if node.op == '+' and left_type == 'string':
            return 'string'

        raise Exception(
            f"Invalid operation '{node.op}' for types {left_type} and {right_type}"
        )

    def visit_Assign(self, node):
        value_type = self.analyze(node.value)
        self.symbols[node.name] = value_type
        return value_type


if __name__ == "__main__":
    code = '''
    x = 5 + 2
    y = "hello"
    z = x + 3
    w = y + " world"
    bad = y + 3        # should throw type error
    u = unknown + 1    # should throw undeclared variable error
    '''

    tokens = tokenize(code)
    parser = Parser(tokens)
    analyzer = SemanticAnalyzer()

    for line in code.strip().splitlines():
        if not line.strip():
            continue
        try:
            tokens = tokenize(line.strip())
            parser = Parser(tokens)
            ast = parser.parse()
            print("AST:", ast)
            result_type = analyzer.analyze(ast)
            if isinstance(ast, list) and len(ast) == 1:
                result_type = analyzer.symbols.get(ast[0].name, result_type)
            print(f"✅ OK: type = {result_type}")
        except Exception as e:
            print(f"❌ {e}")