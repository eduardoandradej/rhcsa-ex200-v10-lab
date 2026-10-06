# Objective 06 — NetworkManager, IP Networking & Name Resolution

O OBJ06 treina rede sem tocar na interface de gerenciamento. Os exercícios mutáveis usam um par `veth` isolado:

```text
ex200a <========== veth ==========> ex200b
aluno                              peer preparado
```

## Labs

| Lab | Competência |
|---|---|
| obj06-01 | devices, profiles e conexões ativas |
| obj06-02 | IPv4 estático com nmcli |
| obj06-03 | modificação, segundo IPv4, gateway e never-default |
| obj06-04 | dual-stack IPv4/IPv6 |
| obj06-05 | edição direta de `.nmconnection`, reload e reactivate |
| obj06-06 | hostname temporário/persistente e `/etc/hosts` |
| obj06-07 | DNS/search-domain no perfil e `nsswitch.conf` |
| obj06-08 | desafio integrado |

## Foco RHEL 10

O bloco usa NetworkManager e keyfiles em `/etc/NetworkManager/system-connections/`. Não usa o formato legado `ifcfg`/`network-scripts`.

## Segurança do lab

- nenhuma tarefa desconecta a interface SSH;
- perfis ativos de treino não instalam default route;
- DNS fictício fica em perfil inativo;
- mudanças em hostname e `/etc/hosts` são restauradas pelo `finish`;
- `ex200a/ex200b` e seus perfis são descartáveis.
