def eq(x, y):
    """
    Implementa o operador de igualdade
    """
    return x == y


def lt(x, y):
    """
    Implementa o operador de "menor que"
    """
    return x < y


def add(x, y):
    """
    Implementa o operador de soma
    """
    return x + y


def sub(x, y):
    """
    Implementa o operador de subtração
    """
    return x - y


def mul(x, y):
    """
    Implementa o operador de multiplicação
    """
    return x * y


def div(x, y):
    """
    Implementa o operador de divisão.

    Obs.: Twine utiliza a divisão inteira, já que não possui floats.
    """
    return x // y


def negate(x):
    """
    Implementa a negação lógica
    """
    return not x


# Dicionário mapeando funções globais às implementações correspondentes.
GLOBALS = {
    "print": print,
    "=": eq,
    "<": lt,
    "+": add,
    "-": sub,
    "*": mul,
    "/": div,
    "~": negate,
}