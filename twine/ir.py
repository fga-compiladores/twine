from typing import Dict, Union, Tuple, List
from lark import InlineTransformer, Tree

# Representa um módulo Twine
IR = Dict[str, "Declaration"]

# Representa o lado direito de uma declaração de função
Declaration = Tuple["ArgDefs", type, "SExpr"]

# A lista de argumentos é uma lista de duplas (nome, tipo) para cada argumento
ArgDefs = List[Tuple[str, type]]

# Representa uma expressão Twine como S-Expression
SExpr = Union[tuple, str, int, bool]


def transform(tree: Tree) -> IR:
    """
    Transforma uma árvore sintática que descreve um módulo Twine
    na representação interna do código como um dicionário de definições.
    """
    raise NotImplementedError
