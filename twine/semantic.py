from typing import List, MutableMapping, Any
from .ir import IR

# Tipo que descreve os erros de semântica detectados.
# Por enquanto, utilizaremos strings
SemanticError = str

# Alguns erros comuns
ERROR_NO_MAIN = "Programa não define a função 'main'."
ERROR_TYPES = "O verificador de tipos encontrou um erro."

# O ambiente de execução é um dicionário mapeando nomes em valores
# que descrevem propriedades de cada variável.
Env = MutableMapping[str, Any]


def semantic_analysis(ir: IR, env: Env) -> List[SemanticError]:
    """
    Retorna a lista de todos os erros de semântica
    """
    return []  # Não implementado...
