# Twine

Esta série de trabalhos cria um interpretador para a linguagem de programação Twine e posteriormente propõe algumas extensões. Twine é uma linguagem de programação extremamente simples, criada justamente com o objetivo de servir como uma linguagem introdutória em um curso de compiladores. Twine não possui uma gramática tão minimalista quanto LISP ou Brainf*ck, mas evita a complexidade desnecessária em linguagens de uso comum como Python, C, etc.

No fim da atividade, criaremos um interpretador capaz de ler e executar o códigos válidos em arquivos .twn. 

Twine não possui strings e portanto não é capaz de implementar o clássico "Hello, World!". Para compensar esta ausência, mostro abaixo um programa que imprime a sequência de Fibonacci:

```twine
% Calcula números de fibonacci de forma elegante e ineficiente.
fib = f( n: integer returns integer ) 
    if (n < 2)
       1
    else
       fib(n - 1) + fib(n - 2)

% A função main() executa a fib(n) para todos numeros de 1 a n.
main = f( n: integer returns boolean ) 
    run_main(0, n - 1)

% Twine não possui laços e, por isso, implementamos repetições com
% recursão.
run_main = f( step: integer, n: integer returns boolean ) 
    print(fib(step))
    if (step = n)
       true
    else
       run_main(step + 1, n)
```

## Introdução ao Twine

Twine é uma linguagem muito simples que visa ser fácil de se implementar, mas ainda assim interessante o suficiente para executar vários algoritmos clássicos. A especificação mais detalhada pode ser encontrada no link http://www.cs.uni.edu/~wallingf/teaching/cs4550/compiler/specification.html, mas aqui faço uma brevíssima introdução.

Twine não possui várias funcionalidades que podem ser esperadas de uma linguagem de programação usual. Para começar, não existem strings, estruturas de dados ou outros tipos mais complexos. Por isso, não é sequer possível implementar o clássico "Hello, World!". Existem apenas dois tipos primitivos: inteiros de 32 bits e booleanos. E não é possível declarar novos tipos.

Um programa Twine consiste em uma sequência de declarações de funções, onde o interpretador executa a função chamada "main". Assim, um programa muito simples na linguagem pode ser visto abaixo:

```twine
main = f ( x: integer, returns integer ) x + 1
```

Este programa pergunta um número "x" para o usuário e imprime o valor de "x + 1".

De forma geral, a declaração de uma função segue o padrão

```twine
<nome-da-função> = f ( [ <args>, ] returns <tipo> ) <corpo>
```

Args é uma sequência de pares <nome>: <tipo> e o corpo da função consiste em uma única expressão opcionalmente precedida por uma sequência de comandos "print(value)". Como usual, a linguagem aceita chamada de funções, expressões aritméticas com as 4 operações, operações lógicas e comparações. A linguagem é tão minimalista que somente as comparações essencias são suportadas:

```twine
x < y  % testa se x maior que y
x = y  % testa se x e y são iguais
```

Outras comparações derivadas devem ser implementadas compondo as comparações primitivas com os operadores lógicos `x | y` (x ou y), `x ^ y` (x e y) e `~x` (negação de x). 

```twine
(x < y) | (x = y)  % x menor ou igual a y
~(y < x)           % x maior ou igual a y
y < x              % x maior que y
~(x = y)           % x diferente de y
```

Além dos operadores `+, -, *, /, ^, |, ~`, a linguagem aceita chamada de funções utilizando a notação usual. A única instrução que afeta o fluxo de execução é o comando "if". Twine não possui laços e implementa repetições a partir de recursão.

Outra característica notável é a ausência de declaração de variáveis. Novas variáveis podem ser definidas apenas na lista de argumentos na declaração de uma função. Não é possível criá-las no corpo da função. Não é possível criar variáveis globais e deste modo não é necessário discutir as regras de escopo de variáveis, que são um tópico potencialmente sutil na implementação de uma linguagem. 


## Estrutura do trabalho

O objetivo do trabalho é implementar o interpretador Twine e algumas funcionalidades adicionais na linguagem. Para isso, existem uma série de testes automatizados que guiam o processo de implementação e verificam diversas competências da matéria de compiladores. De modo geral, cada competência está associada a um arquivo de testes e a competência é considerada satisfeita se todos os testes unitários passarem. 

A pasta "competências" possui arquivos markdown descrevendo cada competências analisada e, para a maior parte das competências, existe um arquivo de teste correspondente na pasta "tests". O arquivo de competência descreve o enunciado de cada problema e o arquivo de testes implementa o teste automatizado correspondente. 

A pasta "exemplos" inclui alguns exemplos (quase todos válidos) de programas Twine. A maior parte dos exemplos que fazem algo interessante estão em exemplos/twine.

Finalmente, a pasta "twine" inclui o código fonte a ser desenvolvido nesta atividade. O trabalho consiste em modificar os arquivos nesta pasta até passar em todos os testes para todas as competências. Algumas competências possuem a distinção entre a versão "avançada" e "básica". É necessário comprovar todas as competências básicas para passar na matéria. As competências avançadas são necessárias para atingir menções superiores como MS e SS.


## Preparando o ambiente

A atividade requer as bibliotecas lark-parser, hypothesis e pytest. Instale todo mundo, se necessário, usando 

    $ pip install -r requirements.txt


## Rodando os testes e verificando competências

O comando básico para executar cada teste é 

    $ pytest tests/test_<nome_da_competência>.py

Se o comando pytest não estiver disponível, tente trocá-lo por `python3 -m pytest`. 

Recomendo estudar algumas opções de execução do Pytest. Existe várias opções bastante úteis:

* `--maxfail=1`: para a execução após a primeira falha
* `--lf`: executa somente os testes que falharam na última execução
* `-vv`: modo verboso, mostra informações bem detalhadas sobre os erros
* `--tb=no` | `--tb=short`: reduz a quantidade de informação mostrada em cada erro 


## Executando um arquivo Twine

De modo geral, podemos executar o interpretador assim:     

    $ python run-twine.py file.twn

Em algumas instalações, também é possível rodar o interpretador como módulo:

    $ python -m twine file.twn

Lembre-se que Twine é implementado em Python e tende a ser muito mais lento que um código correspondente escrito em qualquer linguagem comercial. O interpretador de Python é implementado em C e ainda assim Python tende a ser várias vezes mais lento que o C. Podemos esperar uma diferença entre Python e Twine da mesma ordem que a entre Python e C. Mas isto é um detalhe de implementação: com um pouco de esforço, Twine tem o potencial para ser tão rápido quanto C!


## Ferramentas opcionais

Considere instalar algumas ferramentas que auxiliam no desenvolvimento de qualquer projeto em Python. Recomendo o trio Black + Flake8 + Mypy.

Black é um formatador de código que mantêm o estilo do código consistente. Já o Flake8 e o Mypy conseguem encontrar possíveis erros de programação. Os três ajudam em manter a qualidade do código e facilitam a nossa vida a longo prazo. Executamos cada ferramenta como `black|flake8|mypy <nome-do-arquivo>`. Dependendo das configurações do Python, pode ser necessário usar o comando alternativo `python3 -m <nome-da-ferramenta> <nome-do-arquivo>`. 

O VSCode possui plugins que integram estas 3 ferramentas. Formate um arquivo Python com "ctrl + shift + i" e normalmente o VSCode perguntará se quer instalar o Black na primeira execução deste atalho. Os avisos do Mypy e Flake8 aparecem se estas ferramentas estiverem habilitadas. Digite "ctrl + ," para abrir as configurações e busque por Mypy ou Flake8 para habilitar as inspeções.

O plugin oficial de Python para VSCode utiliza o Pyright, que possui um escopo parecido com as ferramentas acima e é uma boa alternativa ao Mypy e ao Flake8, normalmente já estando integrado ao próprio VSCode. 


## Enviando resultados

O código fica no github classroom e para enviar novas versões, basta subir um commit na "branch" principal do seu repositório pessoal.


## Roteiro sugerido

É possível resolver as questões em várias ordens diferentes, mas existe uma sequência natural para se seguir. Em alguns casos, existem dependências entre as questões, mas às vezes é possível pular uma questão ou resolvê-la de forma incompleta antes de avançar para a próxima.

### Básicas

1. twine_info
2. compilador_org
3. re_basico
4. lex_re
5. cfg_parse
6. ast
7. ir
8. eval

### Teóricas

1. first_follow
2. ll1
3. thompson

### Avançadas

1. eval_fn
2. lexer
3. recur
