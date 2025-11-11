from graphviz import Digraph
from parser import Assign, BinOp, Number, String, Var  # import your AST node classes

def draw_ast(node, graph=None, parent_id=None):
    """
    Recursively draws AST nodes using Graphviz.
    """
    if graph is None:
        graph = Digraph(format='png')

    node_id = str(id(node))
    label = ""

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
        label = str(type(node).__name__)

    graph.node(node_id, label)

    if parent_id:
        graph.edge(parent_id, node_id)

    if isinstance(node, Assign):
        draw_ast(node.value, graph, node_id)
    elif isinstance(node, BinOp):
        draw_ast(node.left, graph, node_id)
        draw_ast(node.right, graph, node_id)

    return graph

if __name__ == "__main__":
    from parser import Parser
    from lexer import tokenize

    # Sample code
    code = 'x = 5 + 2'
    tokens = tokenize(code)
    parser = Parser(tokens)
    ast = parser.parse()

    graph = draw_ast(ast[0])
    graph.render('ast', view=True)  