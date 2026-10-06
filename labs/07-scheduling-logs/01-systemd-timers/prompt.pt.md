No `servera`, trabalhe com `sysstat-collect.timer`.

1. Examine o timer e o serviço correspondente.
2. Copie o timer do diretório do fornecedor para `/etc/systemd/system/`.
3. Altere `OnCalendar` para executar a cada **2 minutos**.
4. Execute `systemctl daemon-reload`.
5. Habilite e inicie `sysstat-collect.timer`.
6. Salve `systemctl cat sysstat-collect.timer` em `output/timer.txt` e `systemctl list-timers sysstat-collect.timer --all --no-pager` em `output/list-timers.txt`.

Não edite diretamente `/usr/lib/systemd/system`.
