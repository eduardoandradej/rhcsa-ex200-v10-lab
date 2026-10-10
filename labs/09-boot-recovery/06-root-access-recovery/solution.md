Conceitos/comandos a dominar no ambiente de recuperação:

```bash
mount -o remount,rw /
passwd root
touch /.autorelabel
```

No RHEL 10 atual, pratique também o fluxo com mídia de rescue na RHLS. Como
alternativa sem mídia, o boot loader pode ser usado para iniciar um shell de
recuperação; depois de corrigir a senha e preparar o relabeling SELinux, o
sistema deve retornar ao processo normal de inicialização.
