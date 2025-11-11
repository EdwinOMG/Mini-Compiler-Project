from flask import Flask, render_template, request
from lexer import tokenize
from parser import Parser, Number, String, Var, BinOp, Assign
from semantic_analyzer import SemanticAnalyzer
import os
from datetime import datetime
from graphviz import Digraph
import os 

app = Flask(__name__)

# Make sure static AST folder exists
AST_FOLDER = os.path.join("static", "ast")
os.makedirs(AST_FOLDER, exist_ok=True)

def draw_ast(node, graph=None, parent=None, count=[0]):
    """Recursively create a Graphviz AST"""
    if graph is None:
        graph = Digraph()
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

    # Recursively handle children
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
                # Tokenize
                tokens = tokenize(line.strip())
                line_data["tokens"] = [t.value for t in tokens]

                # Parse
                parser = Parser(tokens)
                ast_list = parser.parse()

                # Analyze & generate AST image
                for ast_node in ast_list:
                    analyzer.analyze(ast_node)
                    graph = draw_ast(ast_node)
                    timestamp = datetime.now().strftime("%Y%m%d%H%M%S%f")
                    graph_path = os.path.join(AST_FOLDER, timestamp)  # don't add .svg here
                    graph.render(graph_path, format='svg', cleanup=True)

                    # Store the filename for the template
                    line_data["ast_image"] = f"ast/{timestamp}.svg"  # relative to /static   # <-- include .svg here

                line_data["status"] = "OK"

            except Exception as e:
                line_data["status"] = f"ERROR: {e}"

            lines_output.append(line_data)

    output = {"lines": lines_output}
    return render_template("index.html", code=code, output=output)