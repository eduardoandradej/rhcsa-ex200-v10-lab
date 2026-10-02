On `servera`, working as `student`, use:

`/home/student/rhcsa-lab/obj01-02`

Do not manually edit the result files. Produce them from the command line by using redirection and pipelines.

1. Run `bin/stream-demo` and save only standard output to `output/stdout.log`, and only standard error to `output/stderr.log`.
2. Run `bin/stream-demo` again and save both streams together in `output/combined.log`, redirecting stderr to the same destination as stdout.
3. Run `bin/append-demo` twice and append each result to `output/append.log` without overwriting the previous run.
4. By using a pipeline, sort `input/services.txt`, remove duplicate lines, and save the result to `output/services-unique.txt`.
5. By using a pipeline, count how many lines in `input/status.txt` contain the word `active`, and save only the number to `output/active-count.txt`.

When finished, return to the bastion and run `lab grade obj01-02`.
