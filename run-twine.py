import sys
import os
from pathlib import Path

CWD = Path.cwd()
sys.path.append(str(CWD))

# Muda o local de import padrão do twine. Útil para o professor
# trocar facilmente a versão do código que será utilizada a partir
# de variáveis de ambiente
if (version := os.environ.get("USE", "")):
    sys.path.pop()
    sys.path.insert(0, str(CWD / ('_' + version)))

from twine.cli import twine

twine()