# `[recur]`: Descida recursiva

Implemente a gramática do Twine utilizando o algoritmo de descida recursiva. Testaremos os mesmos casos passados para o teste da competência `[ast]`, desabilitando o método .parse() das gramáticas do Lark. A implementação deve ficar no arquivo `twine/recur.py` e possuir aproximadamente a estrutura abaixo:

```python
from lark import Token
from collections import deque
from typing import Tuple
from .lexer import lex
from .ir import IR, SExpr, Declaration

EOF = Token("EOF", "$")  # representa o fim do arquivo
STOP = deque([EOF])
kinds = {"integer": int, "boolean": bool}

# Esta função é o ponto de entrada.
# Recebe uma string de código e retorna a representação interna diretamente.
# Você pode modificar as outras funções deste módulo, mas deve manter o 
# nome e assinatura de parse_to_ir() constantes. 
def parse_to_ir(src: str) -> IR:
    tokens = deque(lex(src))
    tokens.append(EOF)
    
    ir = program(tokens)
    if tokens != STOP:
        raise SyntaxError(f"esperava fim do arquivo: {tokens}")
    return ir

# Funções auxiliares genéricas
def peek(tokens):
    "Mostra o primeiro token da lista o None"
    return tokens[0]

def next(tokens):
    "Lê o próximo token"
    return tokens.popleft()

def read(kind, tokens):
    "Lê um token do tipo dado"
    if peek(tokens).type == kind:
        return next(tokens)
    raise SyntaxError(f"esperava {kind}, obteve {peek(tokens).type}")

def expect(lit, tokens):
    "Espera um literal"
    if peek(tokens) == lit:
        return next(tokens)
    raise SyntaxError(f"esperava {lit!r}, obteve {peek(tokens)}")

def push(token, tokens):
    "Insere token de volta no início da lista de tokens."
    tokens.appendleft(token)

# Continue sua implementação aqui
def program(tokens) -> IR:
    ir = {}
    while tokens != STOP:
        name, fn = define(tokens)
        ir[name] = fn
    return ir

def define(tokens) -> Tuple[str, Declaration]:
    """IDENTIFIER "=" "f" "(" params "returns" TYPE ")" body"""
    name = str(read("IDENTIFIER", tokens))
    expect("=", tokens)
    expect("f", tokens)
    expect("(", tokens)
    argdefs = params(tokens)
    expect("returns", tokens)
    restype = kinds[read("IDENTIFIER", tokens))]
    expect(")", tokens)
    sexpr = body(tokens)

    # Cria declaração e retorna
    decl = Declaration(argdefs, restype, sexpr)
    return (name, decl)

def body(tokens) -> SExpr:
    return ...

... 
```

Note que neste módulo, omitimos a criação de uma árvore sintática intermediária, já que é mais fácil produzir a representação interna diretamente.