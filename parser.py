from dataclasses import dataclass
from lexer import Token

@dataclass
class Number:
    value: int

@dataclass
class String:
    value: str

@dataclass
class Var:
    name: str

@dataclass
class BinOp:
    left: any
    op: str
    right: any

@dataclass
class Assign:
    name: str
    value: any


class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0

    def peek(self):
        if self.pos < len(self.tokens):
            return self.tokens[self.pos]
        return None

    def consume(self, expected_type=None):
        token = self.peek()
        if not token:
            return None
        if expected_type and token.type != expected_type:
            raise SyntaxError(f"Expected {expected_type}, got {token.type}")
        self.pos += 1
        return token

    def parse(self):
        nodes = []
        while self.peek():
            nodes.append(self.statement())
        return nodes

    def statement(self):
        token = self.peek()
        if token.type == "ID":
            name = self.consume("ID").value
            self.consume("ASSIGN")
            expr = self.expression()
            self.consume("END")
            return Assign(name, expr)
        else:
            raise SyntaxError(f"Unexpected token {token.type}")

    def expression(self):
        node = self.term()
        while self.peek() and self.peek().type == "OP" and self.peek().value in ("+", "-"):
            op = self.consume("OP").value
            right = self.term()
            node = BinOp(node, op, right)
        return node

    def term(self):
        node = self.factor()
        while self.peek() and self.peek().type == "OP" and self.peek().value in ("*", "/"):
            op = self.consume("OP").value
            right = self.factor()
            node = BinOp(node, op, right)
        return node

    def factor(self):
        token = self.peek()
        if token.type == "NUMBER":
            return Number(self.consume("NUMBER").value)
        elif token.type == "STRING":
            return String(self.consume("STRING").value)
        elif token.type == "ID":
            return Var(self.consume("ID").value)
        elif token.value == "(":
            self.consume()  # consume '('
            expr = self.expression()
            self.consume()  # consume ')'
            return expr
        else:
            raise SyntaxError(f"Unexpected token {token.type}")