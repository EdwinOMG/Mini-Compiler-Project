import re
from dataclasses import dataclass

@dataclass
class Token:
    type: str
    value: str

TOKEN_SPEC = [
    ('NUMBER',   r'\d+'),
    ('STRING',   r'"[^"]*"'),
    ('ID',       r'[A-Za-z_]\w*'),
    ('ASSIGN',   r'='),
    ('OP',       r'[+\-*/]'),
    ('LPAREN',   r'\('),
    ('RPAREN',   r'\)'),
    ('END',      r';'),
    ('SKIP',     r'[ \t]+'),
    ('COMMENT',  r'#.*'),  
    ('MISMATCH', r'.'),    
]

token_regex = "|".join(f"(?P<{name}>{pattern})" for name, pattern in TOKEN_SPEC)

def tokenize(code: str):
    tokens = []
    for match in re.finditer(token_regex, code):
        kind = match.lastgroup
        value = match.group()

        if kind == "NUMBER":
            tokens.append(Token("NUMBER", int(value)))
        elif kind == "STRING":
            tokens.append(Token("STRING", value.strip('"')))
        elif kind == "ID":
            tokens.append(Token("ID", value))
        elif kind == "ASSIGN":
            tokens.append(Token("ASSIGN", value))
        elif kind == "OP":
            tokens.append(Token("OP", value))
        elif kind == "LPAREN":
            tokens.append(Token("LPAREN", value))
        elif kind == "RPAREN":
            tokens.append(Token("RPAREN", value))
        elif kind == "END":
            tokens.append(Token("END", value))
        elif kind in ("SKIP", "COMMENT"):
            continue
        elif kind == "MISMATCH":
            raise SyntaxError(f"Unexpected character {value}")

    return tokens

if __name__ == "__main__":
    code = '''
    x = 5 + 2;
    # this is a comment
    y = x * 3;
    msg = "hello";
    '''
    for token in tokenize(code):
        print(token)