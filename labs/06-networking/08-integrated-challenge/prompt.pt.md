## Desafio integrado

No `serverb`, configure a interface isolada `ex200a` sem tocar na interface SSH.

Crie `exam-net`:

```text
IPv4 primary:    10.66.8.20/24
IPv4 secondary:  10.66.8.120/24
IPv6:            fd00:66:8::20/64
methods:         manual/manual
autoconnect:     yes
gateway:         nenhum
```

O peer usa `10.66.8.254/24` e `fd00:66:8::fe/64`.
Também configure persistentemente o hostname `serverb-net.lab.test` e adicione `10.66.8.254 peer-net.lab.test peer-net` ao `/etc/hosts`.

Salve `profile.txt`, `runtime.txt`, `ping4.txt`, `ping6.txt` e `getent.txt` em `/home/student/rhcsa-lab/obj06-08/output/`.
