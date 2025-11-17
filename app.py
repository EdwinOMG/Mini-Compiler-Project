from flask import Flask, render_template, request
from lexer import tokenize
from parser import Parser, Number, String, Var, BinOp, Assign
from semantic_analyzer import SemanticAnalyzer
import os
from datetime import datetime
from graphviz import Digraph

app = Flask(__name__)

AST_FOLDER = os.path.join(app.static_folder, "ast")
os.makedirs(AST_FOLDER, exist_ok=True)

def draw_ast(node, graph=None, parent=None, count=[0]):
    if graph is None:
        graph = Digraph(format="svg")
        count[0] = 0

    node_id = str(count[0])
    count[0] += 1

    if isinstance(node, Assign):
        label = f"Assign\n{node.name}"
    elif isinstance(node, BinOp):
        label = f"BinOp\n{node.op}"
    elif isinstance(node, Number):
        label = f"Number\n{node.value}"
    elif isinstance(node, String):
        label = f"String\n\"{node.value}\""
    elif isinstance(node, Var):
        label = f"Var\n{node.name}"
    else:
        label = type(node).__name__

    graph.node(node_id, label)

    if parent is not None:
        graph.edge(parent, node_id)

    if isinstance(node, Assign):
        draw_ast(node.value, graph, node_id, count)
    elif isinstance(node, BinOp):
        draw_ast(node.left, graph, node_id, count)
        draw_ast(node.right, graph, node_id, count)

    return graph

@app.route("/", methods=["GET", "POST"])
def index():
    code = ""
    lines_output = []

    if request.method == "POST":
        code = request.form.get("code", "")
        analyzer = SemanticAnalyzer()

        for line in code.strip().splitlines():
            line_data = {"line": line.strip(), "tokens": [], "ast_image": None, "status": ""}

            if not line.strip():
                continue

            try:
                tokens = tokenize(line.strip())
                line_data["tokens"] = [t.value for t in tokens]

                parser = Parser(tokens)
                ast_nodes = parser.parse()

                for ast_node in ast_nodes:
                    analyzer.analyze(ast_node)

                    graph = draw_ast(ast_node)

                    ts = datetime.now().strftime("%Y%m%d%H%M%S%f")
                    filepath = os.path.join(AST_FOLDER, ts)

                    graph.render(filepath, cleanup=True)

                    line_data["ast_image"] = f"ast/{ts}.svg"

                line_data["status"] = "OK"

            except Exception as e:
                line_data["status"] = f"ERROR: {e}"

            lines_output.append(line_data)

    output = {"lines": lines_output}
    return render_template("index.html", code=code, output=output)

if __name__ == "__main__":
    from waitress import serve
    import os
    port = int(os.environ.get("PORT", 10000))
    serve(app, host="0.0.0.0", port=port)