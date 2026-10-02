# Objective 04 — Simple Shell Scripts

## Exam mapping

This objective is intentionally limited to the RHCSA EX200 shell-scripting
scope:

1. conditional execution (`if`, `test`, `[ ]`, or equivalent);
2. loops to process command-line input and files;
3. positional script inputs (`$1`, `$2`, `$#`, `$@`);
4. processing shell-command output inside a script.

The objective does **not** attempt to turn RHCSA preparation into a Bash
programming course. Functions, arrays, advanced parameter expansion, traps,
regular-expression operators, associative arrays, or complex parsing are not
required by these labs.

## Labs

| Lab | Primary skill |
|---|---|
| obj04-01 | positional parameters and input validation |
| obj04-02 | file tests and conditional branches |
| obj04-03 | conditional execution based on command result |
| obj04-04 | process command output |
| obj04-05 | `for` over command-line arguments |
| obj04-06 | `for` over file input |
| obj04-07 | arguments + loop + conditional + command output |
| obj04-08 | integrated EX200-style scripting scenario |

## Grading philosophy

Graders prefer observable behavior rather than one exact source-code solution.

For example, a grader may execute the student's script with:

- different arguments;
- missing arguments;
- an intentionally missing user or file;
- a second input file created at grade time.

This approach rejects hard-coded answers while allowing valid alternative
shell implementations.

## Suggested study sequence

Run each lab manually:

```bash
lab start obj04-01
lab grade obj04-01
lab finish obj04-01
```

Use `man bash`, `help if`, `help test`, `help for`, `help read`, and
system command man pages when needed.

Do not read `solution.md` until after a genuine attempt.
