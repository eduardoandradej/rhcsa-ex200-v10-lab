O perfil ativo `ex200-keyfile` em `ex200a` possui `10.66.5.10/24`.
Edite diretamente `/etc/NetworkManager/system-connections/ex200-keyfile.nmconnection` e adicione `10.66.5.110/24` como segundo endereço persistente. **Não use `nmcli con mod` para adicionar esse endereço.** Depois execute `nmcli con reload`, reative o perfil e salve `ip -4 -br addr show ex200a` em `output/runtime.txt`.
