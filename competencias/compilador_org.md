# `[compilador_org]`: Organização de compiladores

Neste teste, vamos estudar a organização de um compilador/interpretador e como é o processo de partir de uma string de código fonte na linguagem de programação desejada, até a execução bem sucedida de um programa. 

Para ilustrar o processo, considere um dos exemplos mais triviais de código Twine:

```twine
main = f ( returns integer ) 42
```

Este código instrui o interpretador a simplesmente avaliar a função main e imprimir o resultado (42) na tela. Vamos implementar todas as etapas necessárias para sair desta string de código para uma execução bem sucedida do programa. 

Na competência `compilador_org`, Vamos usar uma estratégia de "enganação": ao invés de implementar um interpretador legítimo capaz de executar qualquer código (inclusive o mostrado acima), vamos implementar o mínimo necessário para executar **somente** este código. Isso vai servir de base como caso de teste. Posteriormente, na medida em implementamos novas funcionalidades no interpretador, os testes devem continuar passando, mas com funções mais universais. 

A estratégia de enganação segue uma lógica parecida com a própria organização de um compilador. Cada etapa abaixo representa uma função que devemos implementar para enganar a suite de testes. Você pode executar os testes desta atividade com o comando

    $ pytest tests/test_compilador_org.py


## Passo 1: análise léxica

A primeira etapa da compilação consiste na análise léxica, que decompõe o código em tokens/lexemas. A função responsável por fazer isto se chama `lex(src)` e está no módulo twine/lexer.py.

Pela assinatura da função, vemos que `lex(src)` deve emitir uma sequência de objetos do tipo `Token` importados do Lark. `Token` é uma subclasse de string que inclui algumas informações adicionais como o tipo do token e opcionalmente a posição da mesma no código, linha, coluna, entre outros. O primeiro token do código de exemplo é um identificador (IDENTIFIER) com o conteúdo "main". Podemos inicializá-lo como:

```python
main_tk = Token("IDENTIFIER", "main")
```

Agora crie os outros tokens e retorne a sequência correta para o código de exemplo. Você pode retornar uma lista ou um gerador usando o comando yield. Existe uma convenção esperada para os tipos dos tokens que você poderá descobrir executando os próprios testes unitários ;)

Dica: experimente com o comando abaixo na hora de rodar os testes
    
    $ pytest tests/test_compilador_org.py --maxfail=1 -vv


## Passo 2: análise sintática

Uma vez que sabemos decompor o código em uma lista de tokens, partimos para a análise sintática. O objetivo é montar a árvore sintática abstrata que descreve código fonte. Representamos as árvores sintáticas com instâncias da classe Tree do Lark, onde cada objeto é criado como 

```python
    tree = Tree("nome_do_nó", lista_de_filhos)
```

Os filhos podem ser tokens ou outros nós do tipo Tree. 

A função responsável por realizar a análise sintática se chama `parse(src)` e está no módulo twine/parser.py. Faça ela retornar uma árvore que descreve o código acima seguindo a mesma estrutura de árvore do exemplo abaixo:

    program
      define
        main
        params
        integer
        42

(esta é a saída do comando `print(tree.pretty())`)

A estrutura acima descreve uma árvore com um nó principal chamado program. Cada programa Twine consiste em uma lista de definições. No nosso caso, só existe uma, que corresponde ao único filho do tipo "define". Cada nó define, por sua vez, possui 4 filhos: um token com o nome da função (main), uma sub-árvore "params" com a declaração dos parâmetros de entrada, um token descrevendo o tipo de saída (integer) e finalmente um último filho declarando o corpo da função. 

No nosso caso, a lista de filhos da sub-árvore "params" é vazia, pois a função não recebe nenhum argumento. Já o último elemento elemento da lista pode ser formado por um único token, como no nosso caso, ou por sub-árvores que representam expressões mais complexas.

Por exemplo, o resultado abaixo mostra a árvore resultante caso 42 fosse escrito como 4 * 10 + 2

    program
      define
        main
        params
        integer
        add
          mul
            4
            10
          2

Observe que a função `parse(src)` recebe uma string de código e retorna um objeto do tipo Tree que representa a árvore sintática abstrata. Você pode utilizar `lex(src)` internamente para criar a lista de tokens para popular esta árvore, mas isto é opcional.


## Passo 3: representação interna

Ainda que as árvores sintáticas produzidas pelo Lark sejam bastante flexíveis e fáceis de trabalhar, nem sempre consistem numa representação ideal de código análise futura. É muito comum que compiladores reescrevam as árvores sintáticas para um formato mais especializado que facilita a análise e execução posterior.

Este é o papel da "representação interna" (ou IR, do inglês "internal representation"). Um compilador profissional pode ter várias etapas com várias representações internas diferentes otimizadas para diferentes objetivos de análise. Nos casos mais simples, no entanto, a própria árvore sintática pode funcionar como representação interna. 

No nosso projeto, vamos fazer algo intermediário: queremos converter as árvores sintáticas que representam programas Twine em objetos Python que carregam a mesma informação de modo um pouco mais prático. Aplicações mais sofisticadas talvez pediriam uma hierarquia de classes especializadas, mas para nossos propósitos podemos pensar em um módulo Twine como um simples dicionário que mapeia nomes de funções em declarações, onde cada declaração é uma trinca do tipo (argumentos, tipo de retorno, corpo da função):

```python
programa = {
    "main": (
        [],    # Argumentos, lista de tuplas (nome, tipo)
        int,   # Tipo de retorno (int ou bool) 
        42,    # Corpo da função
    )
}
```

Para deixar as coisas um pouquinho mais interessantes, vamos trocar a tupla de três elementos por uma NamedTuple que permite acesso tanto por posição quanto por nome. Criamos a NamedTuple com o código abaixo:

```python
from typing import NamedTuple, List, Tuple

class Declaration(NamedTuple):
    args: List[Tuple[str, type]]
    returns: str
    body: SExpr
```

Substitua este código no local apropriado no arquivo twine/ir.py.

SExpr, de S-Expressions, é o formato que utilizaremos para representar expressões no corpo de uma função Twine. Este é um formato simples que codifica uma chamada de função do tipo `f(arg1, arg2, ...)` como uma lista (algo como `[f, arg1, arg2, ....]`). O mesmo formato pode ser utilizado para representar operadores (ex.: `x + y` vira `[+, x, y]`) e formas especiais da linguagem (ex.: `if (cond) then else other` vira algo como `[if, cond, then, other]`). 

Uma SExpr que representa um elemento atômico como um inteiro ou booleano vira simplesmente o valor correspondente a este elemento em Python. Aproveitando que Twine não possui strings, utilizaremos strings para representar variáveis em S-Expressions e assim evitar a necessidade de criar um tipo especializado para isto.

Para completar esta atividade, vá no módulo twine/ir.py e modifique a função transform(tree) para retornar a representação interna adequada para o exemplo acima.

Para testar se você entendeu bem o conceito, o código de teste também verifica se você consegue criar uma representação interna consistente para o exemplo abaixo:

```twine
add = f ( x: integer, y: integer returns integer) x + y
```

Para decidir qual dos dois valores retornar, comece a implementação com um if:

```python
def transform(tree: Tree) -> IR:
    # (é roubo, mas vale!)
    if tree.children[0].children[0] == "main":
        return ... # IR da função main
    else:
        return ... # IR da função add
```


## Passo 4: análise semântica

Considere o programa abaixo:

```twine
main = f ( a : boolean returns integer ) 
    a + true
```

O programa é sintaticamente bem formado, mas possui um bug escondido que poderia aparecer durante a execução: `a + true` tenta somar dois Booleanos. (Python aceita operações matemáticas com Booleanos, mas vamos assumir que este comportamento é proibido em Twine).  

O papel da análise semântica é detectar problemas que podem ocorrer antes da execução do programa, seja porque resultam em bugs ou porque impedem a tradução do programa para instruções na linguagem de destino utilizada. Uma das etapas mais importantes da análise semântica é a verificação de consistência dos tipos. Dependendo do compilador, também é necessário realizar a propagação de tipos para sub-expressões. Por exemplo, se x e y forem inteiros, sabemos que uma expressão do tipo x + y também será. 

Para a atividade atual, vamos simplesmente detectar se o programa define a função "main" ou não. Esta é uma verificação muito simples e deixa a parte mais importante (e difícil!) de verificação de tipos para outra competência. 

Em termos de código, precisamos reimplementar a função `semantic_analysis(ir, env)` no módulo twine/semantic.py para retornar uma lista vazia ou uma lista com um único elemento ERROR_NO_MAIN, caso a função "main" não exista na IR.


## Passo 5: otimização

Finalmente, um compilador e mesmo um interpretador pode ser capaz de realizar várias transformações na representação interna com o intuito de simplificar o código resultante e deixá-lo mais eficiente. Considere o exemplo:

```twine
main = f ( returns integer ) 
    if (true)
        42
    else
        0
```

Sabemos que o if sempre executará o mesmo ramo com o valor 42. Desta forma, poderíamos reescrever o código como 

```twine
main = f ( returns integer )
    42
```

eliminando o teste e possivelmente melhorando o desempenho durante a execução do programa. Os dois exemplos são funcionalmente idênticos, mas o segundo é mais eficiente. Muitos compiladores fazem transformações semelhantes no código com o intuito de simplificar e ganhar performance. 

O exemplo do condicional com o valor da condição conhecida parece relativamente simples de se executar. Compiladores de qualidade industrial como o GCC ou o GHC do Haskell conseguem realizar transformações altamente sofisticadas. Por exemplo, tente compilar o exemplo abaixo em C habilitando todas as flags de compilação:

```C
#include <stdio.h>

void main() {
    int sum = 0;
    for (int n=1; n <= 1000; n++) {
        sum += n;
    }
    printf("sum: %d\n", sum);
}
```

Um compilador maduro como o gcc consegue deduzir o resultado completo do laço e aplicar uma fórmula matemática para concluir que `sum = 499500`. O programa resultante se reduz a um simples printf, cortando o tempo de execução do laço a zero!

```C
#include <stdio.h>

void main() {
    int sum = 499500;
    printf("sum: %d\n", sum);
}
```

É importante ressaltar que o compilador **não** produz uma string de código com a forma otimiza. Isto seria muito pouco prático! Na realidade, o otimizador normalmente trabalha em cima da representação interna do código e transforma a IR da versão ineficiente para a IR da versão eficiente.

Não tentaremos nada tão ambicioso como reescrever um laço aqui. Na realidade, por enquanto não faremos absolutamente nenhuma etapa de otimização! Para que isso aconteça, modifique a função optimize(ir, env) em twine/optimizer.py para retornar a representação interna inalterada. Voltaremos nessa função em outras atividades para implementar algumas das técnicas mais simples.


## Passo 6: execução

O passo final da criação do interpretador está na implementação da etapa de interpretação propriamente dita. Nesta etapa, nós utilizaremos a IR como a representação final que armazena as instruções a serem executadas. 

A parte crucial da interpretação consiste em executar a expressão declara do corpo de cada função. No nosso caso, uma expressão do tipo `x + 1` seria representada como a S-Expression `['+', 'x', 1]`. A função responsável por avaliar esta expressão está no módulo twine/interpreter.py e se chama `eval(sexpr, env)`. A função eval recebe uma S-Expression e um dicionário de ambiente e retorna o valor resultante de avaliar esta expressão.

O processo de avaliação segue mais ou menos o roteiro abaixo:

- Verificamos o tipo da S-Expr
- eval() Retorna inteiros e booleanos imediatamente
- No caso de strings, consulta o dicionário env e retorna o valor correspondente.
- Para listas, avalia recursivamente todos os elementos e executa o primeiro resultado passando os valores seguintes como argumentos.

Para a atividade atual, precisamos apenas lidar com o primeiro caso, onde os argumentos são inteiros ou booleanos. Implemente esta verificação em `eval(...)` e suba um erro do tipo NotImplementedError para os outros tipos de argumentos.

A função `eval(...)` não é o suficiente para realizar uma interpretação completa de um programa. S-Expressions aparecem no corpo de funções, mas um interpretador deve ser capaz de criar funções a partir de da IR e executar funções definidas em Twine se elas forem invocadas em outras partes do código.

Para lidar com funções, precisamos implementar `compile_function(...)`, também em twine/interpreter.py. Esta função possui uma assinatura curiosa, já que retorna uma função Python como saída. Ou seja, `compile_function` converte uma função Twine para a função correspondente Python. Como podem existir dependências entre funções, precisamos passar o ambiente de execução onde as funções foram definidas.

O exemplo abaixo mostra duas funções, ping, pong mutualmente dependentes. Ping não pode ser criada sem acessar o ambiente que define pong nem vice-versa.

```twine
ping = f ( n : integer returns integer )
    if (n = 0)
        1 
    else
        n * pong(n - 1)
        
pong = f (n : integer returns integer )
    if (n = 0)
        1 
    else
        n * ping(n - 1)
```

Por enquanto, não precisamos nos preocupar sobre como implementar `compile_function(...)` corretamente, mas ela deve funcionar ao menos para o caso especial que estamos estudando, ou seja,

```twine
main = f ( returns integer ) 42
```

Deste modo, faça a função `compile_function(...)` retornar uma função Python que não recebe nenhum argumento e retorna 42, já que é isto que aparece no nosso exemplo.


## Finalizando

Isto termina esta competência. Continuaremos no futuro reescrevendo cada etapa com as implementações apropriadas, criando código genérico que funciona para além do exemplo trivial da função main que retorna 42. 