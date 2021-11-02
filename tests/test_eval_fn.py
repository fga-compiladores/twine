import contextlib
import io
import pytest
import operator as op
import copy


def test_cria_funcao_de_n_variáveis(twine, env):
    compile_function = twine.interpreter.compile_function

    args = []
    argdefs = []
    body = 1

    for n in range(1, 10):
        fn = compile_function(argdefs.copy(), int, copy.deepcopy(body), env)
        assert fn(*args) == n

        var = f"x{n}"
        args.append(1)
        argdefs.append((var, int))
        body = ["+", var, body]

