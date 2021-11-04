import pytest
from pathlib import Path
from lark import Lark
from typing import NamedTuple
from pprint import pprint

class Declaration(NamedTuple):
    args: object
    returns: object
    body: object


BLACKLIST = {"operators.twn"}


def test_examples(ir, examples: Path):
    for path in examples.iterdir():
        check_path(ir, path)

def check_path(ir, path):
    if not str(path).endswith(".twn") or path.name in BLACKLIST:
        return
    
    serialized = path.with_suffix(".txt")
    expect = serialized.read_text()
    data = eval(expect, {"Declaration": Declaration})
    src = path.read_text()
    assert ir(src) == data


def error(*args):
    raise NotImplementedError("não pode usar o método parse() da classe Lark.")


@pytest.fixture()
def ir(twine):
    try:
        from twine import recur as mod
    except ImportError:
        raise NotImplementedError("crie o arquivo twine/recur.py")

    parse = Lark.parse
    Lark.parse = prop = property(error)

    yield mod.parse_to_ir

    if Lark.parse is not prop:
        raise RuntimeError
    Lark.parse = parse
