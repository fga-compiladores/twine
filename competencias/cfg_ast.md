"""
# `[cfg_ast]`: Criação de árvores sintáticas 

Diferentemente da maioria das bibliotecas que auxiliam na criação de parsers, Lark produz automaticamente uma árvore sintática como saída do analisador sintático, sem a necessidade de nenhum código adicional. Esta árvore, no entanto, nem sempre possui um formato ideal e pode carregar algumas idiossincrasias de como a gramática foi definida que não carregam muito significado semântico.

Existem duas maneiras principais de contornar estes problemas e otimizar as árvores criadas para obter uma representação adequada. A primeira consiste em utilizar alguns operadores que controlam o formato da árvore na própria declaração da gramática e a segunda é utilizando a técnica dos "transformers", que será discutida em outra competência.

Vamos começar com a primeira. Existem duas operações principais, a de renomeação e a de junção representadas pelos operadores `->` e `?` respectivamente. Também é possível consultar outras operações mais avançadas na [folha de cola](https://lark-parser.readthedocs.io/en/latest/_static/lark_cheatsheet.pdf).

A operação de renomeação serve para diferenciar diferentes alternativas que possuem estruturas idênticas ou potencialmente ambíguas. Por exemplo, uma regra do tipo

```lark
simple : term "+" simple
       | term "-" simple
```

possui uma ambiguidade durante o uso. O Lark, por padrão, omite os terminais declarados de forma literal (como uma string), e portanto monta uma árvore idêntica do tipo `Tree("simple", [x, y])`, com os dois filhos do tipo "term" e "simple" respectivamente. Para distinguir entre as duas operações, podemos utilizar o operador de renomeação, como abaixo, 

```lark
simple : term "+" simple  -> add
       | term "-" simple  -> sub
```

Neste caso, a árvore criada será ou  `Tree("add", [x, y])` ou `Tree("sub", [x, y])`, dependendo do operador encontrado no código fonte. 

O operador de junção, `?` sinaliza ao Lark para evitar a criação de hierarquias desnecessárias como no exemplo abaixo:

```lark
term : factor
     | factor "*" term

factor : NUMBER
```

Uma expressão do tipo "21 * 2" se resolveria, portanto em `Tree("term", [x, y])` onde x seria um número e y uma sub-árvore com um único filho `Tree("term", [2])`. Essa hierarquia adicional é apenas um artefato de como criamos a gramática para obter uma determinada precedência e associatividade de operadores. Idealmente, gostaríamos de obter uma estrutura um pouco mais plana do tipo `Tree("term", [21, 2])` deixando os dois argumentos da multiplicação estão em pé de igualdade.

Podemos obter este efeito adicionando um símbolo de interrogação antes da declaração de term:

```lark
?term : factor
      | factor "*" term

factor : NUMBER
```

Isto comanda Lark a **não** criar um nó do tipo "term" caso possua apenas um filho (que nesse caso seria a a primeira produção "term: factor").

Use estas duas regras para moldar as árvores sintáticas produzidas pela gramática até obter o formato simplificado esperado pelos testes.

Nos testes eliminamos qualquer referência às regras correspondentes a EXPRESSSION, SIMPLE-EXPRESSION, TERM e FACTOR na [gramática do Twine](http://www.cs.uni.edu/~wallingf/teaching/cs4550/compiler/specification.html) e renomeamos as regras de operadores para utilizar os nomes correspondentes do Python como declarados no módulo operator. 

| Operação       | nome |
| -------------- | ---- |
| `x "=" y`      | eq   |
| `x "<" y`      | lt   |
| `x "&vert;" y` | or_  |
| `x "+" y`      | add  |
| `x "-" y`      | sub  |
| `x "^" y`      | and_ |
| `x "*" y`      | mul  |
| `x "/" y`      | div  |
| `"~" x`        | not_ |
| `"-" x`        | neg  |