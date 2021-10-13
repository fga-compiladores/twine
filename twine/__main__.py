# O arquivo __main__.py é executado quando o módulo é executado a partir
# do comando `python -m twine` (onde twine é o nome do módulo do nosso 
# projeto)
from .cli import twine


twine()