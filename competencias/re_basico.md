"""
# `[re-basico]`: Aplicações simples de expressões regulares 

Agora começa a nossa jornada de implementar todas as tarefas esboçadas em `[compilador_org]`. Como vimos antes, o primeiro passo de compilação consiste na análise léxica. A competência atual verifica se você consegue montar um analisador léxico simples baseado em expressões regulares. Para isso, modificaremos a função `lex(src)` em twine/lexer.py.

As regras da análise léxica estão descritas de maneira informal na [documentação do Twine](http://www.cs.uni.edu/~wallingf/teaching/cs4550/compiler/specification.html#lexical-features). 

O primeiro passo consiste em reestruturar a função lex para realmente realizar algum tipo de análise e não simplesmente retornar a resposta correta. Nós não implementaremos um analisador léxico robusto, ainda. O objetivo aqui é apenas verificar se é possível identificar os lexemas pelas expressões regulares correspondentes. Para isso, podemos reestruturar a função lex() da seguinte maneira:

```python
def lex(src: str) -> Iterable[Token]:
    # Este é o primeiro atalho: separar a string nos espaços.
    # Isto funciona para códigos formatados de forma bem deliberada,
    # mas falha em expressões válidas que omitem os espaços, ex., fn(x+y)
    words = src.split()
    for word in words:
        kind = classify_token(word)
        yield Token(kind, word)
        # se você não reconhece/entende o comando yield, sugiro um 
        # link: http://pythonclub.com.br/python-generators.html

def classify_token(word: str) -> str:
    """
    Identifica o tipo de cada token.
    """
    return "..."
```

Como mostrado acima, vamos criar cada objeto token a partir de cada palavra, classificando-as com a função `classify_token(word)`. Neste ponto que entram as expressões regulares. Podemos classificar cada token percorrendo uma lista de pares com (nome da categoria, expressão regular). 

```python
def classify_token(word: str) -> str:
    for (nome, regex) in REGEX_MAP:
        if re.fullmatch(regex, word):
            return nome
    raise SyntaxError(f'elemento não reconhecido: {word!r}')
```

Não se esqueça de importar o módulo `re` no início do arquivo. Caso precise de ajuda sobre o funcionamento da função fullmatch, consulte a [documentação](https://docs.python.org/3/library/re.html#re.fullmatch).

Nossa tarefa é criar a lista de pares com o nome da regra e a regra correspondente:

```python
REGEX_MAP = [
    ("BOOLEAN", r"..."),
    ("COMMA", r"..."),
    ("COMMENT", r"..."),
    ("EQUAL", r"..."),
    ("F", r"..."),
    ("HAT", r"..."),
    ("IDENTIFIER", r"..."),
    ("INTEGER", r"..."),
    ("LPAR", r"..."),
    ("LESS", r"..."),
    ("MINUS", r"..."),
    ("MUL", r"..."),
    ("PIPE", r"..."),
    ("PLUS", r"..."),
    ("RETURNS", r"..."),
    ("RPAR", r"..."),
    ("SEMICOLON", r"..."),
    ("DIV", r"..."),
    ("TILDE", r"..."),
]
```

Ainda que a escolha dos nomes de cada regra seja arbitrária (por exemplo, poderíamos ter chamado a regra de inteiros de "INT"), o código de teste espera um padrão bem determinado. Provavelmente será necessário executar algumas vezes o teste para encontrar o valor esperado para todos os nomes.

A maior parte das regras é bastante trivial. Por, exemplo, a regra "EQUALS" busca o símbolo de "=" e ser escrita simplesmente como `r"="`. Algumas regras simples precisam de um pouco mais de atenção se procurarem símbolos que correspondem a operadores de expressões regulares como *, + , (), etc. 

Utilizamos uma lista de pares no lugar de um dicionário porque a ordem de verificação importa. Por exemplo, as palavras reservadas conflitam com identificadores, assim é necessário testá-las antes dos próprios identificadores. 

Finalmente, os tokens de comentários devem ser **excluídos** do resultado final. Para tanto, simplesmente inclua uma verificação `if kind != "COMMENT": ...` antes do comando yield.


## Finalizando

Agora que terminamos a primeira parte do analisador léxico, podemos testá-lo em um código real. Execute o comando abaixo para ativar a linha de comando do twine no modo "lexer":

    $ python run-twine.py exemplos/fib-simple.twn -l

Ele mostrará o resultado da análise léxica completa deste programa. Teste no fib.twn para ver o código falhar! Nosso analisador ainda é muito primitivo para lidar com alguns casos mais problemáticos. Você consegue descobrir a fonte do erro?

As próximas tarefas atacarão este bug e outros.
