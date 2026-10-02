# Hotfix 0.6.7 — obj01-02 locale-safe

O grader de `obj01-02` não fixa mais uma ordem de classificação baseada em
locale específico.

Antes, o resultado esperado era codificado manualmente e podia divergir do
`sort` real do RHEL quando `LC_COLLATE`/`LANG` alteravam a ordenação de
`NetworkManager`.

Agora o grader calcula a referência com o próprio `sort -u` no `servera`.
Assim, o laboratório continua avaliando o estado correto sem depender do
locale da instalação.
