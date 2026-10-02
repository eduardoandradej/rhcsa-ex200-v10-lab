No `servera`, trabalhando como `student`, use:

`/home/student/rhcsa-lab/obj01-02`

Não edite manualmente os arquivos de resultado. Produza-os pela linha de comando usando redirecionamentos e pipelines.

1. Execute `bin/stream-demo` e grave apenas a saída padrão em `output/stdout.log` e apenas a saída de erro em `output/stderr.log`.
2. Execute novamente `bin/stream-demo` e grave as duas saídas juntas em `output/combined.log`, redirecionando stderr para o mesmo destino de stdout.
3. Execute `bin/append-demo` duas vezes e acrescente cada resultado a `output/append.log`, sem sobrescrever a execução anterior.
4. Usando um pipeline, ordene `input/services.txt`, remova linhas duplicadas e grave o resultado em `output/services-unique.txt`.
5. Usando um pipeline, conte quantas linhas de `input/status.txt` contêm a palavra `active` e grave somente o número em `output/active-count.txt`.

Ao terminar, retorne ao bastion e execute `lab grade obj01-02`.
