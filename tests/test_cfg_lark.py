from lark import Tree, LarkError
import pytest
from pathlib import Path

EXAMPLES = Path(__file__).parent.parent.absolute() / "exemplos"
FAIL_EXAMPLES = [*(EXAMPLES / "fail-hard").iterdir()]
GOOD_EXAMPLES = [
    *(EXAMPLES / f"{p}.twn" for p in ("simple", "fib-simple", "fib")),
    *(EXAMPLES / "twine").iterdir(),
]

@pytest.mark.parametrize("ex", map(str, GOOD_EXAMPLES))
def test_good_examples(ex, parse):
    with open(ex) as fd:
        src = fd.read()
    tree = parse(src)
    assert isinstance(tree, Tree)


@pytest.mark.parametrize("ex", FAIL_EXAMPLES)
def test_fail_examples(ex, parse):
    with open(ex) as fd:
        src = fd.read()
    
    with pytest.raises(LarkError):
        tree = parse(src)
        print('Aceitou entrada inválida:')
        print(ex)
        print('-' * 40)
        print(tree.pretty())
