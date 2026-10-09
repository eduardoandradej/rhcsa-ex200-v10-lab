No `servera`, use **somente `/dev/vdb`**.

1. Crie uma tabela GPT.
2. Crie a primeira partição com nome GPT `data08`, indicação de tipo `xfs`,
   iniciando em `1MiB` e terminando em `1025MiB`.
3. Aguarde o udev registrar o device.
4. Salve `parted -s /dev/vdb unit MiB print` em `output/parted.txt`.
5. Salve `lsblk -o NAME,SIZE,TYPE,FSTYPE,PARTLABEL /dev/vdb` em `output/lsblk.txt`.

Não crie filesystem ainda.
