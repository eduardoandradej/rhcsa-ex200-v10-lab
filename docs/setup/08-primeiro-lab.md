# 08 — Primeiro exercício

[Índice](README.md) · [Home](../../README.md) · [Anterior](07-baseline.md)

**Onde executar:** comandos `lab` no `bastion`; resolução manual no host indicado pelo enunciado.

Esta etapa encerra a instalação do ambiente e apresenta o fluxo normal de uso do laboratório.

O primeiro exercício utilizado neste roteiro é:

```text
obj01-01 — Operações com arquivos
```

Na versão atual do projeto, esse exercício possui:

| Campo | Valor |
|---|---|
| Objetivo | Objective 01 — Essential Tools |
| Alvo | `servera` |
| Dificuldade | 1/5 |
| Tempo estimado | 10 minutos |
| Compatibilidade local | RHEL 9.8 |
| Referência | RHEL 10 |
| Nível de compatibilidade | `exact` |
| Política de reset | `ansible` |
| Status | `ready` |

O objetivo desta página não é ensinar a resposta do exercício.

O estudante deve utilizar o enunciado, a documentação do sistema e seus próprios conhecimentos para chegar ao estado final solicitado.

---

## 8.1 Fluxo normal de um laboratório

A sequência recomendada é:

```text
lab status
    ↓
lab list
    ↓
lab show ID
    ↓
lab start ID
    ↓
resolver manualmente no alvo
    ↓
lab grade ID
    ↓
corrigir, se necessário
    ↓
lab grade ID
    ↓
lab finish ID
    ↓
lab status
```

O CLI separa três responsabilidades:

```text
start   → prepara o cenário
grade   → avalia o estado final
finish  → limpa o cenário
```

Essas três operações não devem ser confundidas.

---

## 8.2 Confirmar que o ambiente está pronto

No `bastion`:

```bash
cd ~/rhcsa-ex200-v10-lab
```

Execute:

```bash
lab status
```

Antes de iniciar o primeiro exercício, confirme:

```text
Control Plane
  bastion      ...   ONLINE

Managed Nodes
  servera      ...   ONLINE
  serverb      ...   ONLINE
```

As ferramentas devem aparecer como disponíveis:

```text
ansible    OK
ssh        OK
git        OK
python3    OK
```

O estado do laboratório deve indicar:

```text
Active      none
```

E o resultado final:

```text
Environment: READY
```

Se o ambiente estiver `DEGRADED`, não inicie um novo exercício antes de corrigir o problema.

---

## 8.3 Consultar o catálogo

Execute:

```bash
lab list
```

O comando organiza os exercícios por objetivo e exibe:

```text
ID
LAB
LEVEL
TIME
STATUS
```

Somente exercícios com status:

```text
ready
```

podem ser iniciados.

Um item com outro status pode existir no catálogo sem estar disponível para execução.

### Filtrar por objetivo

Para listar apenas os laboratórios do Objective 01:

```bash
lab list --objective obj01
```

Também é possível filtrar por parte do nome do objetivo:

```bash
lab list --objective essential
```

---

## 8.4 Conhecer o exercício antes de iniciá-lo

Execute:

```bash
lab show obj01-01
```

O CLI apresenta:

```text
ID
Objective
Title
Target
Difficulty
Time
Compatibility
Reset policy
Status
Description
```

Para `obj01-01`, confirme especialmente:

```text
Target       servera
Status       ready
```

Leia o enunciado completo antes de executar `lab start`.

### Enunciado em inglês

Os laboratórios que possuem tradução também podem ser consultados com:

```bash
lab show obj01-01 --lang en
```

O idioma do enunciado não altera o cenário nem os critérios de avaliação.

---

## 8.5 O que o primeiro exercício pratica

O exercício `obj01-01` trabalha operações fundamentais com arquivos e diretórios.

O cenário é preparado em:

```text
/home/student/rhcsa-lab/obj01-01
```

no host:

```text
servera
```

O diretório inicial contém arquivos fornecidos pelo próprio laboratório.

O estudante deverá organizar esse conteúdo conforme o enunciado.

As competências envolvidas incluem operações como:

```text
criação de diretórios
cópia de arquivos
movimentação de arquivos
renomeação
criação de arquivos vazios
remoção seletiva
preservação do conteúdo fornecido
```

Esta página não fornece os comandos de solução.

---

## 8.6 Iniciar o exercício

No `bastion`:

```bash
lab start obj01-01
```

O CLI executa o `setup.yml` correspondente ao exercício.

Se a preparação terminar corretamente, a saída inclui:

```text
LAB READY
```

e apresenta novamente:

```text
Objective
Exercise
Target
Time
Tarefa
```

O comando também informa o host ao qual o estudante deve se conectar.

Para este exercício:

```text
servera
```

---

## 8.7 O que acontece durante `lab start`

Para `obj01-01`, a preparação automatizada ocorre em `servera`.

O projeto:

1. remove dados antigos desse exercício, se existirem;
2. cria:

```text
/home/student/rhcsa-lab/obj01-01/input
```

3. adiciona arquivos de prática;
4. registra `obj01-01` como o laboratório ativo.

O estado ativo é mantido no `bastion`.

Enquanto houver um laboratório ativo, o CLI impede que outro seja iniciado.

Essa proteção evita que dois cenários automatizados disputem o mesmo ambiente.

---

## 8.8 Confirmar o laboratório ativo

Depois de iniciar:

```bash
lab status
```

A seção:

```text
Lab State
```

deve apresentar:

```text
Active      obj01-01
```

Se já houver uma pontuação registrada, também poderá aparecer:

```text
Last score  NN%
```

---

## 8.9 Conectar ao alvo

No `bastion`:

```bash
ssh servera
```

Confirme:

```bash
hostname -f
```

Resultado esperado:

```text
servera.lab.test
```

Confira o usuário:

```bash
id -un
```

Resultado esperado:

```text
student
```

---

## 8.10 Ir para o diretório do exercício

No `servera`:

```bash
cd /home/student/rhcsa-lab/obj01-01
```

Confira:

```bash
pwd
```

Resultado esperado:

```text
/home/student/rhcsa-lab/obj01-01
```

Inspecione o cenário antes de alterá-lo:

```bash
find . -maxdepth 2 -type f -o -type d
```

Ou:

```bash
ls -la
```

e:

```bash
ls -la input
```

Essa inspeção inicial é uma prática importante.

Antes de modificar um sistema em uma prova prática ou ambiente real, entenda o estado de partida.

---

## 8.11 Ler o enunciado novamente, se necessário

O enunciado pode ser consultado no `bastion` com:

```bash
lab show obj01-01
```

Se você estiver trabalhando em outra sessão SSH, mantenha o enunciado aberto no terminal do `bastion`.

O exercício solicita um **estado final**.

O grader não exige que o estudante utilize um comando específico para chegar a esse estado.

Isso é intencional e aproxima a prática de uma avaliação baseada em resultado.

---

## 8.12 Resolver manualmente

A partir deste ponto, resolva o exercício manualmente em `servera`.

Não execute playbooks de solução e não consulte `solution.md` durante a tentativa normal.

Use, quando necessário:

```text
man
info
--help
documentação instalada no sistema
```

Exemplos de consulta:

```bash
man cp
```

```bash
man mv
```

```bash
man mkdir
```

```bash
man touch
```

```bash
man rm
```

O objetivo é desenvolver velocidade e segurança com as ferramentas de administração Linux.

---

## 8.13 Não alterar o cenário fora do solicitado

Durante o exercício:

- trabalhe somente nos arquivos e diretórios relacionados ao cenário;
- não modifique o `setup.yml`;
- não modifique o `grade.py`;
- não modifique o `finish.yml`;
- não altere o inventário Ansible para fazer o grader passar;
- não execute a solução de referência como substituto da prática.

O grader avalia o sistema, não o texto do seu comando.

---

## 8.14 Sair de servera antes da avaliação

Quando considerar a tarefa concluída:

```bash
exit
```

Você deve retornar ao shell de:

```text
student@bastion
```

Confirme, se desejar:

```bash
hostname -f
```

Resultado esperado:

```text
bastion.lab.test
```

---

## 8.15 Avaliar o exercício

No `bastion`:

```bash
lab grade obj01-01
```

Como `obj01-01` já está ativo, também é possível utilizar:

```bash
lab grade
```

Para documentação e troubleshooting, utilizar o ID explicitamente costuma deixar a operação mais clara.

---

## 8.16 Como interpretar a avaliação

O grader apresenta cada critério com:

```text
[PASS]
```

ou:

```text
[FAIL]
```

Ao final:

```text
Score: NN%
```

Quando todos os critérios são atendidos:

```text
Score: 100%
Resultado: PASS
```

Quando ainda existem pendências:

```text
Resultado: INCOMPLETE
```

Um resultado incompleto não encerra o exercício.

---

## 8.17 O que o grader verifica em `obj01-01`

Sem revelar uma sequência de comandos de solução, o grader verifica o estado final correspondente ao enunciado, incluindo:

- existência da estrutura de diretórios solicitada;
- arquivos que deveriam ser copiados presentes na origem e no destino;
- arquivos que deveriam ser movidos ausentes da origem e presentes no destino;
- arquivo de notas movido e renomeado corretamente;
- arquivos vazios solicitados realmente vazios;
- arquivos temporários removidos;
- conteúdo dos arquivos fornecidos preservado.

Portanto, “parece certo” não é suficiente.

O estado final precisa corresponder aos critérios do exercício.

---

## 8.18 Corrigir uma tentativa incompleta

Se o resultado não for 100%, leia as linhas `[FAIL]`.

O grader pode apresentar uma dica curta para o critério pendente.

Volte ao alvo:

```bash
ssh servera
```

Entre novamente:

```bash
cd /home/student/rhcsa-lab/obj01-01
```

Corrija apenas o que estiver incorreto.

Depois:

```bash
exit
```

Avalie novamente:

```bash
lab grade obj01-01
```

Esse ciclo pode ser repetido:

```text
resolver
   ↓
grade
   ↓
corrigir
   ↓
grade
```

até atingir o estado desejado.

---

## 8.19 Não usar `lab start` novamente para corrigir uma tentativa

Depois que o exercício está ativo, não execute novamente:

```bash
lab start obj01-01
```

O CLI já possui um laboratório ativo e impedirá o início de outro cenário.

Além disso, a função do `start` é preparar o estado inicial, não corrigir uma resposta.

Para corrigir:

```text
volte ao host
ajuste manualmente
execute grade novamente
```

---

## 8.20 Registrar mentalmente o motivo de cada erro

A pontuação é útil, mas o objetivo do laboratório não é apenas chegar a 100%.

Ao encontrar um `[FAIL]`, identifique:

```text
o que eu interpretei errado?
qual comando ou conceito faltou?
eu validei o resultado antes de chamar o grader?
```

Esse processo aumenta a retenção e reduz erros repetidos em exercícios posteriores.

---

## 8.21 Finalizar o exercício

Depois de concluir a prática e quando não precisar mais preservar o cenário:

```bash
lab finish obj01-01
```

Como o exercício está ativo, também é possível:

```bash
lab finish
```

O CLI executa:

```text
finish.yml
```

do exercício.

Em `obj01-01`, a limpeza remove:

```text
/home/student/rhcsa-lab/obj01-01
```

de `servera`.

Quando a limpeza termina corretamente:

```text
LAB FINISHED
```

O estado ativo é então removido.

---

## 8.22 Não executar `finish` antes de terminar a prática

`lab finish` é uma operação de limpeza.

Se você deseja continuar investigando ou corrigindo o exercício, não finalize o cenário.

Use:

```bash
lab grade
```

quantas vezes forem necessárias durante a tentativa.

Execute:

```bash
lab finish
```

somente quando quiser encerrar e limpar aquele exercício.

---

## 8.23 Confirmar a limpeza

Depois:

```bash
lab status
```

A seção:

```text
Lab State
```

deve voltar para:

```text
Active      none
```

Confira também a saúde do ambiente:

```text
Environment: READY
```

Opcionalmente, valide no `servera`:

```bash
ssh servera \
  'test ! -e /home/student/rhcsa-lab/obj01-01 && echo "obj01-01 limpo"'
```

Resultado esperado:

```text
obj01-01 limpo
```

---

## 8.24 O que acontece se `lab finish` falhar

Se o playbook `finish.yml` falhar, o CLI:

- informa a falha;
- não remove silenciosamente o estado ativo.

Isso permite diagnosticar a limpeza antes de prosseguir.

Consulte:

```bash
lab status
```

Se o exercício continuar ativo, investigue a causa.

Não apague `.state/active.json` apenas para esconder uma falha de cleanup.

Se a VM tiver sido profundamente alterada e a limpeza não puder ser concluída, utilize o procedimento de recuperação por snapshot documentado em:

[07 — Baseline e snapshots](07-baseline.md)

---

## 8.25 Um exercício por vez

O projeto trabalha com um único laboratório ativo por vez.

Se tentar iniciar outro enquanto `obj01-01` estiver ativo, o CLI recusará a operação.

O fluxo correto é:

```text
lab start obj01-01
...
lab finish obj01-01
lab start obj01-02
```

Essa regra reduz interferência entre cenários.

---

## 8.26 Status `ready` e outros estados do catálogo

O comando:

```bash
lab list
```

é a referência para a disponibilidade atual.

Um exercício com:

```text
ready
```

possui o conjunto necessário para execução automatizada, incluindo:

```text
setup.yml
finish.yml
grade.py
prompt.pt.md
```

Além dos demais metadados e arquivos utilizados pelo projeto.

Se um item não estiver em `ready`, não tente forçar sua execução alterando os metadados.

---

## 8.27 Como estudar com cada laboratório

Uma rotina eficiente é:

```text
1. Leia o título.
2. Defina mentalmente quais comandos/conceitos serão necessários.
3. Inicie o cenário.
4. Leia o enunciado completo.
5. Inspecione o estado inicial.
6. Resolva sem consultar a solução.
7. Valide manualmente seu próprio resultado.
8. Execute o grader.
9. Corrija o que faltar.
10. Só então finalize o cenário.
```

A etapa 7 é especialmente importante.

No exame real, você não terá um grader indicando cada erro durante a execução.

Aprender a validar o próprio trabalho faz parte da preparação.

---

## 8.28 Use documentação local antes de procurar respostas prontas

Durante a primeira tentativa, priorize:

```bash
man COMANDO
```

```bash
COMANDO --help
```

```bash
apropos PALAVRA
```

```bash
info COMANDO
```

Quando aplicável:

```bash
rpm -qd PACOTE
```

e documentação instalada em:

```text
/usr/share/doc
```

Isso treina uma habilidade valiosa para administração Linux e para avaliações práticas.

---

## 8.29 Soluções de referência

Os diretórios dos laboratórios podem conter:

```text
solution.md
```

Esse arquivo existe para manutenção, estudo posterior e validação do projeto.

Para uma tentativa realista:

```text
não consulte solution.md antes de resolver
```

Uma forma produtiva de utilizá-lo é:

```text
tentativa própria
    ↓
grade
    ↓
correção própria
    ↓
100%
    ↓
comparar com a solução de referência
```

Assim, a solução serve para comparar abordagens em vez de substituir o raciocínio.

---

## 8.30 Compatibilidade RHEL 9.8 e RHEL 10

O `lab show obj01-01` informa:

```text
Local       RHEL 9.8
Target      RHEL 10
Level       exact
```

Para esse exercício, o projeto classifica a prática local como compatível de forma direta com o objetivo correspondente usado como referência.

Outros laboratórios podem possuir classificações diferentes.

Sempre consulte:

```bash
lab show ID
```

antes de iniciar uma prática nova.

---

## 8.31 O projeto não simula uma prova oficial

Este laboratório é um projeto independente de treinamento.

Ele não reproduz:

- questões reais do EX200;
- ambiente oficial de exame;
- conteúdo proprietário da Red Hat;
- laboratórios da Red Hat Learning Subscription.

Os cenários são autorais e utilizam competências de administração Linux/RHEL como referência de estudo.

O objetivo é desenvolver capacidade prática, repetição e troubleshooting.

---

## 8.32 Primeira sessão de estudo recomendada

Para uma primeira sessão, utilize esta sequência:

```bash
cd ~/rhcsa-ex200-v10-lab
```

```bash
lab status
```

```bash
lab list --objective obj01
```

```bash
lab show obj01-01
```

```bash
lab start obj01-01
```

Depois resolva manualmente em `servera`.

Ao terminar:

```bash
lab grade obj01-01
```

Se necessário, corrija e repita o grade.

Quando concluir:

```bash
lab finish obj01-01
```

Por fim:

```bash
lab status
```

---

## 8.33 Antes de iniciar o segundo exercício

Confirme:

```text
[ ] primeiro exercício foi iniciado corretamente
[ ] resolução foi feita manualmente no host indicado
[ ] grader foi utilizado somente após a tentativa
[ ] critérios pendentes foram corrigidos conscientemente
[ ] exercício foi finalizado
[ ] Lab State voltou para Active none
[ ] Environment voltou para READY
```

Depois consulte:

```bash
lab list --objective obj01
```

e avance para o próximo item `ready` do Objective 01.

---

## 8.34 Critério para concluir a instalação do laboratório

A instalação completa pode ser considerada funcional quando você consegue executar, de ponta a ponta:

```text
lab status
    ↓
lab list
    ↓
lab show obj01-01
    ↓
lab start obj01-01
    ↓
acesso ao servera
    ↓
resolução manual
    ↓
lab grade obj01-01
    ↓
lab finish obj01-01
    ↓
lab status
```

O estado final esperado é:

```text
Active      none
Environment READY
```

A partir deste ponto, a infraestrutura deixa de ser o foco principal.

O foco passa a ser:

```text
prática
repetição
velocidade
validação
troubleshooting
```

Esse é o ciclo de estudo para o qual o projeto foi construído.

[Índice](README.md) · [Home](../../README.md) · [Anterior](07-baseline.md)
