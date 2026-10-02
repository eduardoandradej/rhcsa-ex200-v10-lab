```bash
cd /home/student/rhcsa-lab/obj05-06

tuned-adm recommend > output/recommended.txt
tuned-adm list > output/profiles.txt

sudo tuned-adm profile throughput-performance

tuned-adm active > output/active.txt

sudo tuned-adm verify > output/verify.txt 2>&1
echo "verify rc=$?"

cat output/active.txt
cat output/verify.txt
```

O estado obrigatório do exercício é o perfil
`throughput-performance` ativo. O retorno do `verify` deve ser analisado como
diagnóstico da VM/perfil, não usado isoladamente para decidir se a ativação
falhou.
