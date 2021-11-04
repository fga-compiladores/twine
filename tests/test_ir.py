from pathlib import Path
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
    src = path.read_text()
    try:
        print(path)
        data = eval(serialized.read_text(), {"Declaration": Declaration})
    except FileNotFoundError:
        data = ir(src)
        serialized.write_text(
            repr(data).replace("<class 'int'>", "int").replace("<class 'bool'>", "bool")
        )

    assert ir(src) == data


def error(*args):
    raise NotImplementedError("não pode usar o método parse() da classe Lark.")
