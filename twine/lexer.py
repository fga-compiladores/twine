from typing import Iterable
from lark import Token


def lex(src: str) -> Iterable[Token]:
    """
    Analiza o código fonte e retorna uma sequência de tokens.
    """
    yield Token("INVALID", "me implemente aqui!")
