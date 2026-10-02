# Instalação do laboratório — comece por aqui

[Home](../../README.md)

Siga a sequência quando estiver montando o ambiente do zero. Se as VMs já estão prontas, confira a etapa 4 e avance para a preparação do bastion.

1. [Requisitos e arquitetura](01-requisitos.md)
2. [Preparação do host KVM/libvirt](02-host-kvm.md)
3. [Criação das máquinas virtuais](03-criacao-vms.md)
4. [Configuração inicial das VMs](04-configuracao-vms.md)
5. [Preparação do bastion e clonagem](05-bastion-git.md)
6. [Configuração e validação do Ansible](06-validacao-ansible.md)
7. [Baseline e snapshots](07-baseline.md)
8. [Primeiro exercício](08-primeiro-lab.md)

Cada guia informa o local de execução, os comandos e o critério para avançar. O host KVM cria as VMs; o bastion usa Git, Ansible e o comando `lab`.
