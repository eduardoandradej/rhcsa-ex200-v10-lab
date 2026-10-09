## Desafio integrado

Use **somente `/dev/vdc` e `/dev/vdd`**.

Crie em cada disco uma GPT e uma partição LVM:

- `/dev/vdc1`: aproximadamente 4 GiB;
- `/dev/vdd1`: aproximadamente 2.5 GiB.

Crie:

```text
VG:  rhcsa_vgfinal
LV:  rhcsa_data  2 GiB inicialmente
LV:  rhcsa_swap  512 MiB
```

Depois:

1. Formate `rhcsa_data` como XFS label `FINAL08`.
2. Monte persistentemente por UUID em `/lvfinal`.
3. Crie `/lvfinal/marker.txt` com `OBJ08-FINAL`.
4. Formate `rhcsa_swap` como swap label `FINALSWAP08`, ative e persista por UUID.
5. Estenda `rhcsa_data` para **3 GiB de tamanho total**.
6. Expanda o XFS online, preservando `marker.txt`.
7. Valide o fstab com `findmnt --verify`.
8. Salve em `output/`: `pvs.txt`, `vgs.txt`, `lvs.txt`, `findmnt.txt`,
   `swapon.txt`, `df.txt`.

Não use `/dev/vda` nem altere o swap original.
