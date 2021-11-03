# `[lex_re]`: Análise léxica manual 

Na competência `[lex_lark]`, criamos um analisador léxico de forma declarativa utilizando o Lark. Agora, vamos criar um analisador léxico manualmente baseado em expressões regulares. A [documentação do módulo `re`](https://docs.python.org/3/library/re.html#writing-a-tokenizer) no próprio Python mostra um exemplo de como criar um tokenizador (analisador léxico).

Para a competência atual, implemente manualmente um analisador léxico semelhante ao mostrado na documentação do Python no arquivo `twine/lexer_manual.py`. Os testes desabilitam a implementação do lexer contida no Lark e a nossa implementação manual deve retornar os mesmos resultados.

Preste atenção a alguns pontos que devemos adaptar do exemplo da documentação e o formato esperado pelos testes.

1. O nome da função deve ser `lex()` ao invés de tokenize.
2. A função deve produzir tokens do Lark e não instâncias da classe baseada em NamedTuple utilizada no exemplo.
3. A classe Token aceita os argumentos `line` e `column` passados por nome (como em `Token("INTEGER", "42", line=1, column=10)`), mas a inclusão destes parâmetros é opcional.
