```bash
cd /home/student/rhcsa-lab/obj06-06
sudo hostname temporary-net
hostname > output/temporary-hostname.txt
cat /etc/hostname > output/static-before.txt
sudo hostnamectl set-hostname nodea.lab.test
echo '10.66.6.254 peer06.lab.test peer06' | sudo tee -a /etc/hosts >/dev/null
getent hosts peer06 > output/getent.txt
ping -c 2 peer06 > output/ping.txt
```