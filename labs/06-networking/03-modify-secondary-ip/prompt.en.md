On `servera`, `ex200-mod` is active on `ex200a` with `10.66.3.10/24`.

Change it to:

```text
IPv4 primary:      10.66.3.20/24
IPv4 secondary:    10.66.3.120/24
never-default:     yes
autoconnect:       yes
gateway property:  empty
```

`never-default=yes` is required so this profile cannot create a default route
and interfere with the management interface.

Important: in NetworkManager, `ipv4.never-default=yes` conflicts with
`ipv4.gateway`. Therefore this exercise requires the gateway property to remain
empty.

Reactivate the profile and save:

```text
output/profile.txt
output/runtime.txt
output/ping.txt
```

Peer `10.66.3.254` must respond through the directly connected route.
