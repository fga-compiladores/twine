from lark import Tree, LarkError
import pytest
from pathlib import Path


def test_example(parse, examples: Path):
    src = (examples / "full-op.twn").read_text()
    expect = (examples / "full-op.tree").read_text()
    tree = parse(src)
    pretty = tree.pretty()
    assert pretty == expect
