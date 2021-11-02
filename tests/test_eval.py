import contextlib
import io
import pytest
import operator as op

OPS = {
    "+": op.add,
    "-": op.sub,
    "*": op.mul,
    "/": op.floordiv,
    "=": op.eq,
    "<": op.lt,
}


@pytest.mark.parametrize("sexpr", [True, False, 0, 42])
def test_avalia_elementos_atomicos(eval, sexpr):
    assert eval(sexpr, {}) == sexpr


@pytest.mark.parametrize("op", OPS)
def test_avalia_operadores(eval, op):
    fn = OPS[op]
    assert eval([op, 1, 2], {op: fn}) == fn(1, 2)


@pytest.mark.parametrize("op", OPS)
def test_avalia_ambiente_padrão(eval, op, env):
    fn = OPS[op]
    assert op in env, f"operador {op} não está presente no ambiente padrão"
    assert eval([op, 1, 2], env) == fn(1, 2)


def test_eval_if(eval):
    assert eval(["if", True, 1, 2], {}) == 1
    assert eval(["if", False, 1, 2], {}) == 2


def test_eval_print(eval, env):
    with contextlib.redirect_stdout(io.StringIO()) as fd:
        assert eval(["print", 42, 1], env) == 1
    assert fd.getvalue() == "42\n"


def test_eval_if_é_lazy(eval, env):
    with contextlib.redirect_stdout(io.StringIO()) as fd:
        assert eval(["if", True, ["print", 1, 2], ["print", 3, 4]], env) == 2
        assert fd.getvalue() == "1\n", "lembre-se de avaliar apenas um ramo do print"

    with contextlib.redirect_stdout(io.StringIO()) as fd:
        assert eval(["if", False, ["print", 1, 2], ["print", 3, 4]], env) == 4
        assert fd.getvalue() == "3\n", "lembre-se de avaliar apenas um ramo do print"


def test_operadores_lógicos(eval, env):
    with contextlib.redirect_stdout(io.StringIO()) as fd:
        assert eval(["|", True, ["print", 1, True]], env) is True
        assert fd.getvalue() == "", "lembre-se de avaliar apenas um ramo do print"
        
        assert eval(["|", False, ["print", 1, True]], env) is True
        assert fd.getvalue() == "1\n"

    with contextlib.redirect_stdout(io.StringIO()) as fd:
        assert eval(["^", False, ["print", 1, True]], env) is False
        assert fd.getvalue() == "", "lembre-se de avaliar apenas um ramo do print"
        
        assert eval(["^", True, ["print", 1, False]], env) is False
        assert fd.getvalue() == "1\n"

