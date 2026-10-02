No `servera`, trabalhe em `/home/student/rhcsa-lab/obj05-06`.

O serviço TuneD já foi preparado para o exercício.

Tarefas:

1. Grave `tuned-adm recommend` em `output/recommended.txt`.
2. Grave `tuned-adm list` em `output/profiles.txt`.
3. Ative o perfil:
   `throughput-performance`
4. Grave `tuned-adm active` em `output/active.txt`.
5. Execute `tuned-adm verify` e grave a saída em `output/verify.txt`.

Estado final: o perfil ativo deve ser `throughput-performance`.

**Observação:** `tuned-adm verify` é uma verificação diagnóstica. Dependendo
do hardware/VM e das características do perfil, ela pode retornar código
diferente de zero e ainda assim o perfil solicitado estar corretamente ativo.
Neste lab, preserve a saída da verificação e confirme separadamente o perfil
ativo.

O `lab finish` restaurará o perfil e o estado do serviço anteriores.
