"""
# `[eval_fn]`: Criando funções (10pts)

Um programa Twine é uma sequência de declarações de funções. No entanto, a implementação de eval() na competência `[eval]` executa apenas expressões Twine dentro de um ambiente. Como criamos uma declaração de função?

Python é uma linguagem flexível o suficiente para que seja possível (e razoavelmente simples) criar funções dinamicamente que interpretem uma IR de Twine. Vamos fazer isto nessa competência. O esqueleto para isto está na função `compile_function()` no arquivo `twine/interpreter.py`

```python
def compile_function(argdefs: ArgDefs, restype: type, body: SExpr, env: Env):
    
    def fn(*args):
        return ...

    return fn
```

Uma função que cria uma nova função a partir dos parâmetros de entrada é conhecida como um fechamento (closure). A implementação de um fechamento é algo relativamente complexo já que a função de saída pode capturar algumas das variáveis locais da função mãe. Felizmente, Python resolve tudo isto automaticamente sem maiores problemas e na maioria das vezes, basta declarar uma função dentro da outra sem nenhuma precaução adicional.

No exemplo abaixo, mostramos como criar uma função de saída numa função de 2 argumentos. Você pode generalizar para n argumentos facilmente e usar a implementação como guia. 

```python
argdefs = [("x", int), ("y", int)]  # argdefs, como utilizado na IR
restype = int
body = ["+", "x", "y"]
env = default_env()

def fn(*args) -> restype:
    # Inicializa argumentos
    local_vars = {"x": args[0], "y": args[1]}

    # Adiciona ao ambiente
    local_env = env.copy()
    local_env.update(local_vars)

    # Executa no novo ambiente
    return eval(body, local_env) 
```

A estratégia básica é inicializar o ambiente de execução com as variáveis locais e executar eval() na declaração do corpo da função. 

Note que foi necessário copiar o ambiente na variável local_env para que as funções não compartilhem as mesmas variáveis locais. Caso contrário, um módulo Twine como o abaixo poderia falhar

```
f1 = f ( x: integer, y: integer, returns integer) x + y
f2 = f ( x: integer, y: integer, returns integer) f1(y, x) + x
```

Isto porque se o dicionário fosse compartilhado, existiria apenas uma única variável x e uma única variável y compartilhada por todas funções do program. Assim, se fizéssemos `f2(1, 2)` o resultado seria 4 e não 3. A execução de `f1(y, x)` no corpo de f2 inverteria a atribuição de x e y, fazendo com que x passasse a valer 2 após a execução da função. Experimente trocar o env.copy() por simplesmente `local_env = env` para observar a diferença.

É lógico que a realização de uma cópia de dicionário a cada execução de função é bastante ineficiente, especialmente se o ambiente padrão contiver muitas funções. Para melhorar a performance nesses casos, podemos utilizar a class ChainMap() do módulo collections.

Um ChainMap é muito similar a um dicionário (e muitas vezes podemos simplesmente trocar um dicionário por um ChainMap sem realizar nenhuma alteração), mas armazena os dados como uma cadeia de dicionários. Seja, por exemplo, `d1` e `d2` dois dicionários ou estruturas similares. Um `ChainMap(d1, d2)` funciona da seguinte maneira:

* Em acesso para leitura, `cm[key]` busca a chave primeiro e d1 e, caso não exista, posteriomente em d2.
* Em acesso de escrita, `cm[key] = value`, salva o resultado apenas em d1 e nunca sobrescreve os valores de d2.

Usando o ChainMap(), podemos trocar a linha `local_env = env.copy()` por `local_env = ChainMap(local_vars, env)`. Isto evita a cópia potencialmente cara do ambiente padrão, mas mantêm o comportamento praticamente inalterado. Lembre-se de importar a classe do módulo `collections`. 

Pronto! Agora já temos o conhecimento necessário para implementar `compile_function()` de forma genérica e razoavelmente eficiente. Termine a implementação para passar em todos os testes.