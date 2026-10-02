# Setup atual

## Pré-requisitos no bastion

```bash
git --version
ansible --version
python3 --version
```

## Repositórios locais

```bash
sudo dnf repolist
```

## SSH

```bash
ssh servera hostname -f
ssh serverb hostname -f
```

## Ansible

```bash
cd ~/rhcsa-ex200-v10-lab/ansible
ansible-inventory --graph
ansible managed -m ansible.builtin.ping
ansible-playbook playbooks/validate.yml
```
