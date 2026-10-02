On `servera`, repository `rhcsa-base` is already configured.

1. Install `rhcsa-toolkit` with DNF.
2. Install `rhcsa-temp` with DNF.
3. Verify both packages with RPM.
4. Remove `rhcsa-temp` with DNF.
5. At the end, `rhcsa-toolkit` must remain installed at version `1.0-1`
   and `rhcsa-temp` must be absent.
