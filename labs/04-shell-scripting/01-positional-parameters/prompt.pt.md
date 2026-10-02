No `servera`, trabalhe em `/home/student/rhcsa-lab/obj04-01`.

Crie o script executável `greet.sh`.

Requisitos:

1. O script deve exigir **exatamente dois argumentos**:
   - argumento 1: usuário;
   - argumento 2: função.
2. Com dois argumentos, deve imprimir exatamente:
   `USER=<arg1> ROLE=<arg2>`
3. Se a quantidade de argumentos for diferente de dois:
   - escreva em stderr:
     `Usage: greet.sh USER ROLE`
   - encerre com código `2`.
4. Com entrada válida, encerre com código `0`.

O script deve funcionar com valores diferentes dos exemplos usados durante o estudo.
