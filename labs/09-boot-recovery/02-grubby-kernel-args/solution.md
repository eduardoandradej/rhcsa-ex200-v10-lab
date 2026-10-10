```bash
cd /home/student/rhcsa-lab/obj09-02
sudo grubby --update-kernel=ALL --args="systemd.show_status=1"
sudo grubby --info=ALL | tee output/grubby.txt
```
