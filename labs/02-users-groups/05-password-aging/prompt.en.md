On `servera`:

1. Set a valid password for `aginguser1` and `aginguser2`.
2. For `aginguser1`, configure:
   - minimum: 2 days;
   - maximum: 45 days;
   - warning: 7 days;
   - inactivity after expiration: 5 days.
3. Force `aginguser1` to change its password at the next login.
4. For `aginguser2`, configure a 90-day maximum password age.
5. Make the `aginguser2` account expire exactly 90 days from today.

Use `passwd`, `chage`, and `date` as needed.
