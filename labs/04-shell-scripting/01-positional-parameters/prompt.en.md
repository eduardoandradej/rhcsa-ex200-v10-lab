On `servera`, work in `/home/student/rhcsa-lab/obj04-01`.

Create executable script `greet.sh`.

Requirements:

1. The script must require **exactly two arguments**:
   - argument 1: user;
   - argument 2: role.
2. With two arguments, print exactly:
   `USER=<arg1> ROLE=<arg2>`
3. If the argument count is not two:
   - write to stderr:
     `Usage: greet.sh USER ROLE`
   - exit with code `2`.
4. With valid input, exit with code `0`.

The script must work with values other than the examples used during study.
