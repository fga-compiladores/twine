"""
# `[cfg_parse]`: Análise sintática em gramáticas livres de contexto (5pts)

A etapa seguinte da organização de um compilador consiste em implementar a análise sintática através da função `parse()`. Utilizaremos o [Lark](https://github.com/lark-parser/lark) novamente, mas como se trata de uma tarefa relativamente complexa e extensa, vamos criar um analisador básico e dedicar outras competências a aperfeiçoar o resultado da análise sintática.

Para habilitar o analisador sintático do lark, basta modificar a função `parse()` em `twine/parser.py` para chamar o método `.parse()` de uma gramática do Lark.

```python
from .grammar import GRAMMAR

def parse(src: str) -> Tree:
      return GRAMMAR.parse(src)
```

A gramática do Twine está declarada na forma Backus-Naur em http://www.cs.uni.edu/~wallingf/teaching/cs4550/compiler/specification.html. Podemos adaptar estas regras para o formato esperado pelo Lark em  `twine/twine.lark`, mas algumas regras precisam de ajustes. 

Para começar, o Lark declara os não-terminais em minúsculas e os terminais em maiúsculas e não aceita hífens nos nomes das regras gramaticais. Adapte os nomes para um formato aceito pelo Lark com o cuidado de diferenciar corretamente as regras terminais das não terminais.

Outra diferença está no modo como Lark lida com as regras epsilon. Ainda que seja possível declarar uma regra como:

```lark
regra : alt1
      |
```

onde a última alternativa vazia representa um epsilon, é mais comum utilizar os operadores estendidos para declarar explicitamente que uma produção é opcional.

```lark
regra : [ alt1 ]
```

As produções epsilon também aparecem na declaração de listas. Também é possível utilizar operadores estendidos para reescrever os epsilon como operações de repetição

```lark
// Usando os epsilons
items : item tail

tail  : sep items
      |

// Sem epsilons
items : item (sep item)*
```

Note que é necessário fazer pequenos ajustes no caso de listas potencialmente vazias ou se o separador não for utilizado. Identifique todas as ocorrências de epsilons na gramática e realize as adaptações necessárias. Note que alguns testes esperam nomes específicos para as regras gramaticais que podem ser ligeiramente diferente das declarações na documentação do Twine.

Alguns testes em compiladores_org provavelmente irão falhar após a reescrita da gramática, pois as árvores sintáticas resultantes podem ser ligeiramente diferentes. Lidaremos com estes problemas na próxima competência `[cfg_ast]`.
