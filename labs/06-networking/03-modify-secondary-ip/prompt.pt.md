No `servera`, `ex200-mod` está ativo em `ex200a` com `10.66.3.10/24`.

Altere para:

```text
IPv4 primary:      10.66.3.20/24
IPv4 secondary:    10.66.3.120/24
never-default:     yes
autoconnect:       yes
gateway property:  vazio
```

`never-default=yes` é obrigatório para impedir que este perfil crie uma rota
default e interfira na interface de gerenciamento.

Importante: no NetworkManager, `ipv4.never-default=yes` é incompatível com
`ipv4.gateway`. Portanto, este exercício exige que a propriedade gateway fique
vazia.

Reative o perfil e salve:

```text
output/profile.txt
output/runtime.txt
output/ping.txt
```

O peer `10.66.3.254` deve responder ao ping pela rota diretamente conectada.
