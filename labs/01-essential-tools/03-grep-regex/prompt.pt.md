No `servera`, trabalhando como `student`, use:

`/home/student/rhcsa-lab/obj01-03`

Use `grep` e expressões regulares para produzir os arquivos abaixo. Não edite manualmente os resultados.

1. Em `input/systems.txt`, selecione somente linhas cujo primeiro campo seja `SRV-` seguido de exatamente três dígitos. Grave em `output/servers.txt`.
2. Selecione todas as linhas cujo hostname comece por `web`. Grave em `output/web-hosts.txt`.
3. Selecione somente sistemas que sejam simultaneamente do ambiente `prod` e estejam `active`. Grave em `output/prod-active.txt`.
4. Em `input/events.log`, selecione linhas contendo `WARN` ou `ERROR` usando expressão regular estendida. Grave em `output/alerts.log`.
5. Em `input/systems.txt`, selecione linhas cujo endereço IP termine em `.21`. Grave em `output/ip-ending-21.txt`.

Preserve a ordem original das linhas.

Ao terminar, retorne ao bastion e execute `lab grade obj01-03`.
