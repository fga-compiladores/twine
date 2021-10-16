import pytest
from lark import Tree, Token, InlineTransformer
from pprint import pprint

SRC = "main = f ( returns integer ) 42"
TOKENS = "IDENTIFIER EQUAL F LPAR RETURNS IDENTIFIER RPAR INTEGER"
AST = """
program
  define
    main
    params
    integer
    42
""".lstrip()


def test_realizou_a_análise_léxica_do_exemplo(twine):
    from twine.lexer import lex

    tokens = list(lex(SRC))

    print(tokens)
    assert len(tokens) == 8
    assert [str(tk) for tk in tokens] == SRC.split()
    assert [tk.type for tk in tokens] == TOKENS.split()


def test_realizou_a_análise_sintática_do_exemplo(twine):
    from twine.parser import parse

    ast = parse(SRC)

    assert type(ast) is Tree, "A saída deve ser um objeto do tipo Tree"
    assert ast.pretty() == AST
    assert ast.children[0].children[0] == "main"
    assert (
        type(ast.children[0].children[1]) is Tree
    ), "A lista de argumentos é uma árvore!"
    assert ast.children[0].children[1] == Tree("params", [])
    assert ast.children[0].children[2] == "integer"
    assert ast.children[0].children[3] == "42"
    assert (
        type(ast.children[0].children[3]) is Token
    ), "Utilize tokens no lugar de strings ou números"
    assert ast.children[0].children[3].type in {"INTEGER", "INT"}


def test_cria_a_representação_interna_da_função_main(twine):
    from twine.ir import transform
    from twine.parser import parse

    ast = parse(SRC)
    ir = transform(ast)
    assert ir == {"main": ([], int, 42)}


def test_cria_a_representação_interna_da_função_add(twine):
    from twine.ir import transform
    from twine.parser import parse

    ast = parse("main = f ( returns integer ) 42")
    define = ast.children[0]
    define.children[0] = "add"
    define.children[1] = Tree(
        "params",
        [
            Tree("param", ["x", "integer"]),
            Tree("param", ["y", "integer"]),
        ],
    )
    define.children[3] = Tree("add", ["x", "y"])

    print(ast.pretty())
    ir = transform(ast)

    assert len(ir) == 1
    assert "add" in ir

    args = ir["add"][0]
    assert args == [("x", int), ("y", int)]

    returns = ir["add"][1]
    assert returns == int

    body = ir["add"][2]
    assert len(body) == 3
    assert body[0] == "+"
    assert body[1] == "x"
    assert body[2] == "y"
