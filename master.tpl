#!/bin/bash
set -x
exec > >(tee /var/log/user-data.log|logger -t user-data ) 2>&1
echo BEGIN
date '+%Y-%m-%d %H:%M:%S'
cat <<EOF > /etc/sysconfig/docker-storage-setup
DEVS=/dev/xvdg
VG=docker-vg
EOF
