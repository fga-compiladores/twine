"""
# `[ir]`: Representação interna 

Ainda que seja natural representar código fonte utilizando árvores genéricas, muitas vezes é mais conveniente (ou eficiente) utilizar estruturas de dados específicas que possuem uma semântica mais próxima da linguagem que o objeto `Tree` fornecido pelo Lark. Estas estruturas de dados utilizadas internamente pelo compilador para representar o código e realizar as etapas posteriores de análise semântica, otimização e emissão do código final são conhecidas como "representação interna".

Em alguns casos, a representação interna pode corresponder diretamente à árvore sintática ou, ao menos, possuir uma relação 1 para 1 com a sintaxe da linguagem. Em outras, é possível que a representação interna seja substancialmente diferente, se preocupando apenas em armazenar uma estrutura que preserve o significado do código original.

Utilizaremos, no nosso compilador, apenas estruturas de dados nativas do Python, optando pela simplicidade. A abordagem já foi descrita na competência `[compiladores-org]` e consiste em representar um programa como um dicionário de nomes de funções mapeando em suas implementações. As expressões da linguagem são armazenadas na forma de S-Expressions.

Para fazer um código que realize a transformação para S-Expression no Lark, utilizaremos a classe de Transformers, que são estruturas responsáveis por transformar objetos do tipo `Tree` e criar outras árvores ou outras representações. 

Modifique o módulo `twine/ir.py` para incluir a classe IrTransformer como abaixo:

```python
from lark import Transformer, v_args

class IrTransformer(Transfomer):
    def program(self, def_list):
       return {...}
    
    @v_args(inline=True)
    def define(self, name, params, type, body):
       return (...)
    
    ...
```

Cada nó do tipo `Tree(<tipo>, <filhos>)` é processado executando o método com o mesmo nome do tipo e passando a lista de filhos como argumento. Os métodos que possuem o decorador `@v_args(inline=True)` recebem cada filho como um argumento separado, como no caso do define mostrado acima. O Lark transforma os filhos antes de passá-los para os pais.

Você deve criar métodos para lidar com todas as regras da gramática com o intuito de retornar a representação interna. Na maior parte dos casos, o processo é simples,

```python
    ...

    # Converte os terminais de inteiros.
    def INTEGER(self, tk):
       return int

    # Cria S-Expression para o operador de soma
    @v_args(inline=True)
    def add(self, x, y):
       return ['+', x, y]

    ...
```

Lembre-se que Python possui funções de primeira categoria e, assim, consegue automatizar o processo de criação de várias funções iguais para reduzir a duplicação de código

```python
# Cria métodos que lidam com operadores
def operator_factory(op, name):
   @v_args(inline=True)
   def operator(self, x, y)
       return [op, x, y]
   
   operator.__name__ = name
   return operator


IrTransformer.add = operator_factory('+', 'add')
```

Não é necessário utilizar esta técnica, mas elas pode facilitar enormemente a implementação de alguns trechos da gramática.

Para concluir a competência, é necessário implementar todas as regras do transformer para realizar a conversão completa das árvores Lark para a representação interna descrita em `[compilador-org]`.