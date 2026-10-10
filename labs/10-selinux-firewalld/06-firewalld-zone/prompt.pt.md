Na zona de treinamento `rhcsa10`:

1. Associe permanentemente a origem `198.51.100.0/24`.
2. Libere permanentemente o serviço predefinido `http`.
3. Libere permanentemente `45100/tcp`.
4. Recarregue o firewalld para que runtime e permanente coincidam.
5. Grave `firewall-cmd --zone=rhcsa10 --list-all` em `output/runtime.txt`.
6. Grave `firewall-cmd --permanent --zone=rhcsa10 --list-all` em
   `output/permanent.txt`.

Não altere a zona da interface usada pelo SSH.
