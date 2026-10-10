Identifique a interface da rota padrão e a zona do firewalld associada a ela.

Nessa zona:

1. Libere `45102/tcp` de forma persistente.
2. Recarregue o firewalld.
3. Grave o nome da zona em `output/zone.txt`.
4. Grave o resultado de `--query-port=45102/tcp` em runtime em
   `output/runtime.txt`.
5. Grave a mesma consulta com `--permanent` em `output/permanent.txt`.

Não mova a interface para outra zona e não remova os serviços existentes.
