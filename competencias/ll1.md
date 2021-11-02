# `[ll1]`: algoritmo LL(1) 

Responda a questão no arquivo manual/ll1.txt.

A gramática do Twine, como expressa na [documentação](http://www.cs.uni.edu/~wallingf/teaching/cs4550/compiler/specification.html), não é compatível com o algoritmo LL(1). No entanto, é possível transformá-la numa gramática compatível com pequenas modificações. Responda às perguntas abaixo para identificar o problema e criar uma gramática compatível.

1. Um problema comum para gramáticas se encaixarem na categoria LL(1) é a recursão à esquerda. Ela normalmente aparece na declaração de operadores com em `expr : expr "+" term | term`. A gramática do Twine possui algum exemplo de recursão deste tipo? Onde? 

2. Qual a diferença entre as regras de precedência e associatividade de operadores do Twine com relação à convenção à matemática e à maior parte das linguagens de programação? Sabendo que Twine foi concebido com a ênfase na simplicidade de implementação, justifique a escolha em função da resposta dada em (1).

3. Outro exemplo comum de conflito no LL(1) é a ocorrência de duas produções alternativas de um mesmo não-terminal que compartilham algum elemento de seu conjunto FIRST. Isto acontece com bastante frequência na gramática do Twine, mas em todos os casos o problema pode ser eliminado por uma transformação simples na gramática. Aponte uma situação em que este problema aparece e a sua respectiva solução.