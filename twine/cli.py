"""
Interface de linha de comando
"""
import click
import builtins
from pprint import pprint
from lark import Tree

# Importamos as funções principais do módulo twine.
from .parser import parse
from .lexer import lex
from .ir import transform
from .interpreter import run_module


def main(
    src, show_ast=False, show_ir=False, show_tokens=False, run=False, optimize_ir=False
):
    """
    Comando principal a ser executado pelo interpretador.
    """

    # A ação padrão é executar o código
    if not show_tokens and not show_ast and not show_ir:
        run = True

    # Realiza a análise léxica e imprime sequência de tokens
    if show_tokens:
        for tk in lex(src):
            print(f"{tk.kind:10}: {tk}")

    # Realiza a análise sintática e imprime a árvore sintática
    # como retornada pelo Lark.
    if show_ast:
        tree = parse(src)
        print(tree.pretty())

    # Imprime a representação do código como uma como S-Expression.
    if show_ir:
        tree = parse(src)
        ir = transform(tree)
        pprint(ir)

    # Executa código
    if run:
        tree = parse(src)
        ir = transform(tree)

        if optimize_ir:
            ir = optimize(ir)

        run_module(ir)


# Usamos a biblioteca click (https://click.palletsprojects.com/en/8.0.x/)
# para criar a interface de linha de comando. A biblioteca cria o programa
# de linha de comando a partir de uma função e algumas anotações que
# descrevem informações sobre os argumentos na forma de decoradores.
@click.command()
@click.argument("input", type=click.File())
@click.option(
    "--lex",
    "-l",
    is_flag=True,
    default=False,
    help="Realiza análise léxica e mostra um token por linha.",
)
@click.option(
    "--parse",
    "-p",
    is_flag=True,
    default=False,
    help="Imprime a árvore sintática do código.",
)
@click.option(
    "--ir",
    "-i",
    is_flag=True,
    default=False,
    help="Imprime a representação interna como uma S-Expression.",
)
@click.option(
    "--run",
    "-r",
    is_flag=True,
    default=False,
    help="Executa a função main() do programa.",
)
@click.option(
    "--optimize",
    "-O",
    is_flag=True,
    default=False,
    help="Habilita otimização.",
)
def twine(input, lex, parse, ir, run, optimize):
    src = input.read()
    return main(
        src, show_tokens=lex, show_ast=parse, show_ir=ir, run=run, optimize_ir=optimize
    )
