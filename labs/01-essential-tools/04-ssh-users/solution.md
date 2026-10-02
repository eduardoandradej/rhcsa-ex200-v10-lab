# Solução possível — obj01-04

No `servera`:

```bash
cd /home/student/rhcsa-lab/obj01-04

ssh student@serverb 'hostname -f' > remote-host.txt
ssh student@serverb 'whoami' > remote-user.txt

su - labuser
whoami > /home/labuser/switch-user.txt
exit
```

A senha de laboratório do `labuser` é `redhat`.
