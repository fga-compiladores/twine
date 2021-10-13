import pytest
from lark import Tree, Token, InlineTransformer

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


def test_cria_a_representação_interna_da_função_main(twine):
    from twine.ir import transform
    from twine.parser import parse

    ast = parse(SRC)
    ir = transform(ast)
    assert ir == {"main": ([], int, 42)}


def test_cria_a_representação_interna_da_função_add(twine):
    from twine.ir import transform
    from twine.parser import parse

    ast = parse("add = f ( x: integer, y: integer returns integer) x + y")
    ir = transform(ast)
    assert ir == {"add": ([("x", int), ("y", int)], int, ["+", "x", "y"])}
