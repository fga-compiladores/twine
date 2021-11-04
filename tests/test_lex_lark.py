from types import SimpleNamespace
from random import choice, random, randint
import pytest
import lark
import os
from pathlib import Path
from lark import Token

TOKEN_MAP = {
    "ID": "IDENTIFIER",
    "INT": "INTEGER",
    "EQ": "EQUAL",
    "DIV": "SLASH",
}


def kind(cls):
    return TOKEN_MAP.get(cls, cls)


def normalize(tk):
    if isinstance(tk, Token):
        return Token(kind(tk.type), str(tk))
    else:
        return [normalize(tk) for tk in tk]


def token(typ, data, **kwargs):
    return Token(kind(typ), data)


@pytest.mark.parametrize(
    "ex",
    "x y1 nome snake_case camelCase ALL_CAPS $ $$ r$ $1 $42 $_ $var $ugly$but_valid".split(),
)
def test_identificadores_validos(ex, lex):
    assert normalize(lex(ex)) == [Token("IDENTIFIER", ex)]


@pytest.mark.parametrize(
    "ex",
    "_ _foo _A".split(),
)
def test_identificadores_invalidos(ex, lex):
    with pytest.raises(Exception):
        print(f"Aceitou identificador inválido: {normalize(lex(ex))}")


def test_identifica_numeros_inteiros(lex):
    for _ in range(1000):
        src = str(randint(0, 100) * randint(1, 1000))
        assert lex(src) == [Token("INTEGER", src)]


def test_ignora_comentarios(lex):
    tokens = lex("x %comentário")
    assert tokens[-1] == "x", "Tokens de comentários devem ser removidos da saída"
    assert tokens == ["x"]
