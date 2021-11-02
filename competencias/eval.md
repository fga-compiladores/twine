"""
# `[eval]`: Avaliando código

A função `eval()` do Python recebe uma string de código, interpretando-a como código Python, e retorna o valor correspondente. Por exemplo `eval("x + 2", {"x": 40})` retorna 42. Vamos criar a nossa própria função eval para Twine que, ao invés de receber uma string, recebe uma S-Expression e retorna o resultado correspondente. Assim como na versão Python, nossa função de avaliação precisa de um ambiente de execução que, no nosso caso, pode ser somente um dicionário com o valor das variáveis locais.

Assim como discutido na atividade `[compiladores_org]`, a função `eval(sexpr, env)` está no módulo `twine/interpreter.py`. O processo de avaliação segue mais ou menos o roteiro abaixo:

- Verificamos o tipo da S-Expr
- eval() Retorna inteiros e booleanos imediatamente
- No caso de strings, consulta o dicionário env e retorna o valor correspondente.
- Para listas, avalia recursivamente todos os elementos e executa o primeiro resultado passando os valores seguintes como argumentos. 

Por exemplo, na S-Expr `["+", 40, 2]` extraímos a função associada ao `"+"` a partir do dicionário e os dois outros elementos seguem inalterados, pois são números inteiros. Isso resulta na lista `[lambda x, y: x + y, 40, 2]`. O resultado desta operação pode ser obtido por uma expressão como `lst[0](*lst[1:])`, onde assume-se que o primeiro elemento é uma função e os outros são seus argumentos (o Python utiliza a notação *args para expandir uma lista nos argumentos de uma função).

Observe que, para o interpretador funcionar, é necessário registrar as funções associadas aos operadores no ambiente padrão. A função `default_env()`, no mesmo módulo, declara este ambiente. Complete a definição incluindo todos os outros operadores suportados pelo Twine. 

Existem vários pequenos detalhes necessários para que um interpretador funcione corretamente. O módulo de testes verifica exaustivamente vários casos potencialmente problemáticos e se existe alguma omissão importante na implementação. Termine a implementação de eval() e default_env() até passar em todos os testes. 

