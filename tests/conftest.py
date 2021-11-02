from types import SimpleNamespace
import pytest
import sys
import pathlib
import os

TEST_PATH = pathlib.Path(__file__).parent
PROJECT_PATH = TEST_PATH.parent
SRC_PATH = PROJECT_PATH / "twine"

sys.path.append(".")
sys.path.append(str(PROJECT_PATH))


@pytest.fixture(scope="session")
def twine():
    if version := os.environ.get("USE", ""):
        root = str(PROJECT_PATH / ("_" + version))
        if sys.path[0] != root:
            sys.path.insert(0, root)

    import twine

    return twine


@pytest.fixture(scope="session")
def lex(twine):
    from twine.lexer import lex

    return lambda src: list(lex(src))


@pytest.fixture(scope="session")
def parse(twine):
    from twine.parser import parse

    return parse


@pytest.fixture(scope="session")
def spec():
    return SimpleNamespace(
        keywords={
            "integer",
            "boolean",
            "true",
            "false",
            "if",
            "else",
            "f",
            "returns",
            "print",
        },
        operators=[*"+-*/<=^|~"],
        punctuation=[*"():,"],
        special_characters=[*"():,+-*/<=^|~%$_"],
    )


@pytest.fixture(scope="session")
def examples():
    return PROJECT_PATH / "examples"
