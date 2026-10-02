On `servera`:

1. Lock `departed1`'s password and immediately expire the account using expiration value `1`.
2. Set `serviceacct` to use `/sbin/nologin`.
3. Set `tempcontract` to expire 30 days from today.
4. `recoveruser` starts locked and expired. Unlock its password and clear the account expiration date.

Do not remove any of the four accounts.
