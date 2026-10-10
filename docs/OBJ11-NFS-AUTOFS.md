# Objective 11 — NFS & AutoFS

OBJ11 builds the RHEL 10 network-attached storage client skills around a
dedicated NFS provider on `serverb`.

| Lab | Skill |
|---|---|
| obj11-01 | discover, manually mount, inspect, and unmount NFS |
| obj11-02 | persistent NFS mount in `/etc/fstab` |
| obj11-03 | direct AutoFS map |
| obj11-04 | indirect AutoFS wildcard map with `*` and `&` |
| obj11-05 | `x-systemd.automount` generated from `/etc/fstab` |
| obj11-06 | integrated manual verification + indirect AutoFS challenge |

## Infrastructure boundary

Ansible prepares `serverb` as the NFS provider. The learner works on
`servera` as the NFS client.

The provider uses only `/srv/rhcsa11` and
`/etc/exports.d/rhcsa11.exports`. The export definition keeps normal root
squashing; no `no_root_squash` training shortcut is used.

The NFS firewall services are enabled on the server-side active zone by the
prerequisite playbook. Student-facing firewall work remains in OBJ10.

## Cleanup

Client-facing labs clean their own mounts and AutoFS files. The two labs that
modify `/etc/fstab` back it up during setup and restore it during finish.
