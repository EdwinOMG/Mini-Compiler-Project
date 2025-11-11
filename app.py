from flask import Flask, render_template, request
from lexer import tokenize
from parser import Parser
from semantic_analyzer import SemanticAnalyzer
from interpreter import Interpreter

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    output = {}
    code = ""
    if request.method == "POST":
        code = request.form.get("code", "")
        analyzer = SemanticAnalyzer()
        interpreter = Interpreter()
        lines_output = []

        for i, line in enumerate(code.strip().splitlines(), start=1):
            if not line.strip():
                continue
            try:
                tokens = tokenize(line.strip())
                parser = Parser(tokens)
                ast = parser.parse()
                for node in ast:
                    analyzer.analyze(node)
                    interpreter.interpret(node)
                lines_output.append({
                    "line": line.strip(),
                    "tokens": [t.value for t in tokens],
                    "ast": ast,
                    "status": "OK"
                })
            except Exception as e:
                lines_output.append({
                    "line": line.strip(),
                    "tokens": [],
                    "ast": [],
                    "status": f"ERROR: {e}"
                })
        output["lines"] = lines_output
        output["symbol_table"] = interpreter.env

    return render_template("index.html", code=code, output=output)

if __name__ == "__main__":
    app.run(debug=True)