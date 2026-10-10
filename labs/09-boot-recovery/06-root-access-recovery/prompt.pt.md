## Drill manual de recuperação de superusuário

Este item é **manual-only** e não usa `lab start`.

A referência RHEL 10 deve ser praticada preferencialmente no laboratório RHLS
com RHEL 10 e console apropriado. O objetivo é saber recuperar acesso
administrativo quando a senha root é desconhecida ou está bloqueada.

Pratique no ambiente apropriado:

1. Interromper o boot no GRUB.
2. Entrar em um ambiente de recuperação.
3. Garantir que o filesystem raiz esteja em leitura/escrita antes de alterar
   a senha.
4. Definir uma nova senha root.
5. Garantir o relabeling SELinux necessário quando arquivos de autenticação
   forem alterados fora do boot normal.
6. Retornar ao boot normal e validar o acesso.

### Limitação deliberada do KVM local

No RHEL 10, a trilha atual recomenda mídia de rescue e também documenta uma
alternativa sem mídia usando `init=/bin/bash`. Essa alternativa pode exigir
alterações nos parâmetros `console=`. O nosso acesso automatizado é serial via
`virsh console`; remover parâmetros de console pode justamente cortar esse
canal durante o boot.

Por isso o projeto **não automatiza nem força** esta recuperação a partir do
bastion. Faça o drill em um console gráfico do `virt-manager` se desejar
experimentá-lo localmente, e repita a prática no RHLS RHEL 10.
