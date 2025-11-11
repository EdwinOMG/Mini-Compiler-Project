from lexer import tokenize
from parser import Parser
from semantic_analyzer import SemanticAnalyzer
from interpreter import Interpreter

def run_demo(code: str):
    print("Mini Compiler Demo — Semantic Analysis in Action\n")

    analyzer = SemanticAnalyzer()
    interpreter = Interpreter()

    for i, line in enumerate(code.strip().splitlines(), start=1):
        if not line.strip():
            continue

        print(f"Line {i}: {line.strip()}")
        try:
            # Lexical Analysis
            tokens = tokenize(line.strip())
            print("  Tokens:", [t.value for t in tokens])

            # Parsing
            parser = Parser(tokens)
            ast = parser.parse()
            print("  AST:", ast)

            # Semantic Analysis
            for node in ast:
                result_type = analyzer.analyze(node)
            print("  Semantic Check: OK")

            # Interpretation
            for node in ast:
                result = interpreter.interpret(node)
            print("  Executed successfully\n")

        except Exception as e:
            print(f"  ERROR: {e}\n")

    print("Final Symbol Table (Runtime Environment):")
    for name, value in interpreter.env.items():
        print(f"  {name} = {value}")

if __name__ == "__main__":
    code = '''
    x = 5 + 2
    y = "hello"
    z = x + 3
    w = y + " world"
    bad = y + 3        # should trigger type error
    u = unknown + 1    # should trigger undeclared variable error
    '''
    run_demo(code)