# Simulado final integrado

Você recebeu uma demanda sem roteiro de comandos. Entregue o seguinte estado:

- grupo `opsfinal12`;
- usuário `operator12`, shell `/bin/bash`, membro suplementar de
  `opsfinal12`;
- diretório `/srv/final12`, `root:opsfinal12`, modo `2770`;
- AutoFS indireto com base `/remote12-final`;
- mapa mestre `/etc/auto.master.d/final12.autofs`;
- mapa `/etc/auto.final12`;
- wildcard que monte `serverb:/srv/rhcsa11/integrated/&` como NFS
  `rw,sync`;
- `autofs` habilitado e ativo;
- script executável `/usr/local/bin/final-report12`:
  - recebe uma chave (`red` ou `hat`) como primeiro argumento;
  - lê `/remote12-final/CHAVE/info.txt`;
  - grava o conteúdo em `/srv/final12/report-CHAVE.txt`;
- execute o script como `operator12` para `red` e `hat`;
- `/etc/cron.d/final12` deve executar
  `/usr/local/bin/final-report12 red` como `operator12` a cada 15 minutos.

Grave em `output/`:

- `id.txt`;
- `mounts.txt`, contendo evidência das chaves `red` e `hat`;
- `reports.txt`, contendo os dois relatórios;
- `cron.txt`.

Este é o fechamento do laboratório. Priorize estado final correto, persistente
e verificável.
