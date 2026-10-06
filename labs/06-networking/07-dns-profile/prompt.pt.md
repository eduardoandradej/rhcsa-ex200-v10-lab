O perfil `ex200-dns` existe em `ex200a` e deve permanecer **inativo**, para não interferir na resolução usada pela administração.

Configure persistentemente:

```text
IPv4 DNS:          192.0.2.53, 192.0.2.54
DNS search:        lab.example
ignore-auto-dns:   yes
never-default:     yes
autoconnect:       no
```

Salve esses campos em `output/dns-profile.txt` e a linha `hosts:` de `/etc/nsswitch.conf` em `output/nsswitch-hosts.txt`. Não ative o perfil.
