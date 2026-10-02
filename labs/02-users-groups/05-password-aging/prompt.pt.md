No `servera`:

1. Defina uma senha válida para `aginguser1` e `aginguser2`.
2. Em `aginguser1`, configure:
   - mínimo: 2 dias;
   - máximo: 45 dias;
   - aviso: 7 dias;
   - inatividade após expiração: 5 dias.
3. Force `aginguser1` a trocar a senha no próximo login.
4. Em `aginguser2`, configure máximo de 90 dias.
5. Faça a conta `aginguser2` expirar exatamente 90 dias a partir da data atual.

Use `passwd`, `chage` e `date` conforme necessário.
