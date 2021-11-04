import pytest
from pathlib import Path
from lark import Lark

LEX_LARK_PATH = Path(__file__).parent / "test_lex_lark.py"
src = LEX_LARK_PATH.read_text()
exec(src)

def error(*args):
    raise NotImplementedError("não pode usar o método lex() da classe Lark.")


@pytest.fixture()
def lex(twine):
    try:
        from twine import lexer_manual as mod
    except ImportError:
        try:
            from twine import lex_manual as mod
        except ImportError:
            raise NotImplementedError("crie o arquivo twine/lexer_manual.py")

    fn = mod.lex
    Lark.lexer = prop = property(error) 
    yield lambda src: list(fn(src))
    if Lark.lexer is not prop:
        raise RuntimeError
    del Lark.lexer
    