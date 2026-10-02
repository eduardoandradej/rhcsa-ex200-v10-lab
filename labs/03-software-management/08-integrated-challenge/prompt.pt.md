## Desafio integrado — RPM/DNF/Repositórios

No `serverb`, trabalhe em `/home/student/rhcsa-lab/obj03-08`.

1. Crie `/etc/yum.repos.d/rhcsa-system.repo` contendo:
   - `[rhcsa-system-base]`
     - `baseurl=file:///var/lib/rhcsa-lab/obj03/repos/base`
     - habilitado
     - `gpgcheck=0`
   - `[rhcsa-system-errata]`
     - `baseurl=file:///var/lib/rhcsa-lab/obj03/repos/errata`
     - inicialmente desabilitado
     - `gpgcheck=0`
2. Instale `rhcsa-system` versão `1.0-1` a partir do repositório base.
3. Inspecione o RPM local `assets/rhcsa-local-1.0-1.noarch.rpm` com RPM e
   salve as informações em `output/local-rpm-info.txt`.
4. Instale esse RPM local usando DNF.
5. Habilite o repositório de errata e atualize `rhcsa-system` para `2.0-1`.
6. Ao final, desabilite persistentemente os dois repositórios customizados.
7. Identifique a transação DNF mais recente envolvendo `rhcsa-system` e grave
   os detalhes de `dnf history info <ID>` em `output/history.txt`.

Estado final esperado:

- `rhcsa-system-2.0-1` instalado;
- `rhcsa-local-1.0-1` instalado;
- ambos os repositórios customizados desabilitados.
