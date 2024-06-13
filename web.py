import subprocess
import os

# Create CLT in Proxmox 8 with Debian 11 standard
proxmox_cmd = f"qm create 100 --name Web --net0 vmbr1,ip=192.168.10.122/24,gw=192.168.10.1 --cpu cputype=host,cores=2 --memory 4096 --disk 16 --cdrom /var/lib/vz/template/iso/debian-11.0.0-amd64-netinst.iso --boot c --vnc 0"
subprocess.run(proxmox_cmd, shell=True)

# Enable NFS and CIFS features
proxmox_cmd = "qm feature 100 nfs,cifs"
subprocess.run(proxmox_cmd, shell=True)

# Start Web CLT
proxmox_cmd = "qm start 100"
subprocess.run(proxmox_cmd, shell=True)

# Run commands inside the CLT
ssh_cmd = f"ssh root@192.168.10.122 "
commands = [
    "apt update && apt upgrade -y",
    "apt install exfat-fuse -f -y",
    "mkdir /mnt/otg",
    "echo '//192.168.1.150/otg8t /mnt/otg cifs username=redi,password=871975,iocharset=utf8,noperm 0 0' >> /etc/fstab",
    "apt update",
    "wget https://sourceforge.net/projects/xampp/files/XAMPP%20Linux/8.2.12/xampp-linux-x64-8.2.12-0-installer.run",
    "chmod 755 xampp-linux-x64-8.1.4-1-installer.run",
    "./xampp-linux-x64-8.1.4-1-installer.run",
    "sed -i '/AllowOverride AuthConfig Limit/AllowOverride AuthConfig/g' /opt/lampp/etc/extra/httpd-xampp.conf",
    "/opt/lampp/lampp restart",
    "echo '[Unit]\nDescription=XAMPP\nAfter=network.target\n[Service]\nType=forking\nExecStart=/opt/lampp/lampp start\nExecStop=/opt/lampp/lampp stop\nRestart=always\n[Install]\nWantedBy=multi-user.target' > /etc/systemd/system/xampp.service",
    "systemctl daemon-reload",
    "systemctl enable xampp.service",
    "systemctl start xampp.service"
]

for command in commands:
    subprocess.run(ssh_cmd + command, shell=True)
