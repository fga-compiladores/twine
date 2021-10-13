from collections import ChainMap
from typing import Union, Tuple, Dict, List, Iterator, Callable, MutableMapping, cast

from .ir import IR, SExpr, Declaration, ArgDefs
from .stdlib import GLOBALS

# Tipo que para um valor Twine qualquer
#
# Incluimos funções junto aos booleanos e inteiros, já que um
# módulo declara várias funções e as mesmas podem aparecer
# no dicionário de ambiente.
Value = Union[bool, int, Callable]

# O ambiente de execução é qualquer coisa que lembre um dicionário
# Por isso, usamos MutableMapping, no lugar de Dict.
Env = MutableMapping[str, Value]


def eval(sexpr: SExpr, env: Env) -> Value:
    """
    Executa uma S-Expression dentro do ambiente dado.
    """
    return 42  # ... implemente a versão correta aqui!


def compile_function(
    argdefs: ArgDefs, restype: type, body: SExpr, env: Env
) -> Callable:
    """
    Compila a função a partir da listas de argumentos, tipo de retorno, corpo
    da função e dicionário de ambiente.

    O resultado é uma função Python que realiza a mesma operação
    codificada na SExpr dentro do contexto de execução fornecido.
    """

    # Coloque a implementação correta aqui!
    def fn():
        return ...

    return fn


def compile_module(ir: IR, env: Env) -> Dict[str, Callable]:
    """
    Compila um módulo a partir da IR e retorna um dicionário
    que relaciona o nome de cada função à sua implementação correspondente.

    Todas estas funções são espelhadas no dicionário de ambiente.
    """

    module = {}

    # Popula ambiente com definições de funções.
    # Cada declaração adiciona uma entrada (nome, função)
    # no dicionário de ambiente.
    for (name, define) in ir.items():
        args, restype, body = cast(tuple, define)
        func = compile_function(args, restype, body, env)
        module[name] = env[name] = func

    return module


def default_env():
    """
    Retorna o ambiente de execução padrão da linguagem.

    Twine é extremamente minimalista e define poucas funções nativas.
    A única função óbvia é a função print, que recebe um argumento e imprime
    o resultado sem retornar nada.

    Outras funções menos óbvias são os operadores: +, -, *, etc. Operadores são
    apenas nomes mais amigáveis para as funções binárias. O dicionário com a biblioteca
    global fica gravado no ambiente de execução associando por exemplo, "+": lambda x, y: x + y.
    """
    return {
        "+": lambda x, y: x + y,
        "-": lambda x, y: x - y,
        "...": ...,
    }


# -----------------------------------------------------------------------------
# Funções auxiliares
#
# (implementações fornecidas, já que não tem nada de muito interessante para
# a matéria de compiladores)
# -----------------------------------------------------------------------------


def run_module(ir: IR) -> Value:
    """
    Executa o módulo representado pela IR e retorna o valor calculado pela função main.
    """

    env = default_env()
    module = compile_module(ir, env)

    # Lê argumentos da linha de comando e executa a função main
    # do ambiente
    argdefs = ir["main"][0]
    argvalues = read_args(argdefs)

    main_fn = cast(Callable, module["main"])
    result = main_fn(*argvalues)

    # Imprimimos true|false e não True|False, como acontece por padrão no Python
    if isinstance(result, bool):
        print("true" if result else "false")
    else:
        print(result)

    return result


def read_args(argdefs: ArgDefs) -> Iterator[Value]:
    """
    Lê argumentos do terminal a partir do padrão declarado em argdefs.
    """
    for k, typ in argdefs:
        while True:
            value = input(f"{k} ({typ.__name__}): ")

            if typ == int:
                try:
                    yield int(value)
                    break
                except ValueError:
                    print("ERRO: inteiro inválido!")

            elif typ == bool:
                if value == "true":
                    yield True
                    break
                elif value == "false":
                    yield False
                    break
                else:
                    print("ERRO: booleano inválido!")
