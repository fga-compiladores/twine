"""
# `[lark-lex]`: Análise léxica utilizando o Lark 

Vamos agora reimplementar `lex()` utilizando uma biblioteca de apoio que auxilia na criação de compiladores e analisadores léxicos e sintáticos. Existem algumas opções diferentes disponíveis para Python (e várias outras para outras linguagens de programação), mas aqui utilizaremos o [Lark](https://github.com/lark-parser/lark). 

No Lark, declaramos uma gramática completa (tantos as regras léxicas quanto as regras sintáticas) utilizando notação especial inspirada nas notação de Backus-Naur Extendida (EBNF). Começamos, então, criando um arquivo `twine/twine.lark` com uma declaração quase vazia:

```lark
// Símbolos não-terminais (regras sintáticas)
program: (BOOLEAN | COMMENT | IDENTIFIER | INTEGER | WHITESPACE)+ 

// Símbolos terminais (regras léxicas)
WHITESPACE: /\s+/
BOOLEAN: /.../
COMMENT: /.../
IDENTIFIER: /.../
INTEGER: /.../
// ...
```

O conteúdo das declarações de símbolos terminais é semelhante ao das entradas em `REGEX_MAP` no módulo `twine/lexer.py`. Note a presença explícita de uma regra para capturar espaços em branco. Anteriormente utilizávamos o truque simples, mas frágil, de aplicar o método .split() das strings.

Por enquanto, estamos apenas especificando que um programa é uma sequência de tokens, já que o interesse dessa atividade é apenas na análise léxica.Adapte as expressões regulares para os diferentes tokens utilizados na atividade anterior para usar a gramática do lark. Note que as regras triviais que capturam símbolos literalmente, como operadores, parênteses, vírgulas, etc, não precisam de declaração no Lark.

Precisamos carregar este arquivo de gramática no Python. Crie o módulo `twine/grammar.py` com o conteúdo igual ou similar ao que segue abaixo:

```python

from lark import Lark
from pathlib import Path

TWINE_PATH = Path(__file__).parent
GRAMMAR_PATH = TWINE_PATH / "twine.lark"
GRAMMAR_SRC = GRAMMAR_PATH.read_text()
GRAMMAR = Lark(GRAMMAR_SRC, start="program")
```

Finalmente, modificamos o `lex()` em `twine/lexer.py` para utilizar o lexer do Lark e não a versão que tínhamos implementado antes.  

```python
from .grammar import GRAMMAR

def lex(src: str) -> Iterable[Token]:
    return GRAMMAR.lex(src)
```

Muito mais simples, né? Podemos também limpar código auxiliar como a função classify_token() e o dicionário REGEX_MAP. Com estas mudanças, o nosso código já está quase pronto para passar nos testes da atividade. Provavelmente, apenas o teste sobre comentários e sequências de tokens falha.

Consulte a [documentação do Lark](https://lark-parser.readthedocs.io/en/latest/grammar.html) ou a [folha de cola](https://github.com/lark-parser/lark/blob/master/docs/_static/lark_cheatsheet.pdf) para ver como ignorar determinados tipos de tokens e modifique o código para passar nestes testes.


## Notas

Estamos agora numa situação onde o analisador léxico é mais robusto para alguns programas, mas falha em outros que funcionavam anteriormente, como em

    $ python run-twine.py exemplos/fib-simple.twn -l

O analisador léxico do Lark depende das regras sintáticas presentes na gramática: sempre que introduzimos regras com símbolos explícitos ou palavras chave, o Lark cria automaticamente as declarações para as regras léxicas correspondentes. 