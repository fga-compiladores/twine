# `[thomspon]`: Construção de Thompson

A regra de criação de um identificador no Twine pode ser abstraída como `L(L|D)*`, onde L representa o conjunto de todas as letras e o cifrão e D representa o conjunto dos dígitos e underscore. 

1. Crie um autômato utilizando a construção de Thompson que identifique a linguagem dada pela expressão regular dada anteriormente.

2. Elimine todas as transições epsilon do autômato anterior.

3. Converta o NFA resultante para um DFA.