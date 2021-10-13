from typing import MutableMapping, Optional

from .ir import IR

# O ambiente de execução é um dicionário mapeando nomes em valores
# que descrevem propriedades de cada variável.
Env = MutableMapping[str, object]


def optimize(ir: IR, env: Env = None) -> IR:
    """
    Aplica todas as técnicas de otimização conhecidas para este compilador e
    retorna a nova IR otimizada.
    """
    raise NotImplementedError("otimização não foi implementada")


def default_env() -> Env:
    """
    Retorna o ambiente de execução padrão.
    """
    return {}
