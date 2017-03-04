#!/bin/bash
set -x
exec > >(tee /var/log/user-data.log|logger -t user-data ) 2>&1
echo BEGIN
date '+%Y-%m-%d %H:%M:%S'
apt-get update
apt-get -y install squid3
cat <<EOF > /etc/squid/squid.conf
  acl all src all
  acl SSL_ports port 443
  acl CONNECT method CONNECT
  http_access allow all
  http_port 3128
  hierarchy_stoplist cgi-bin ?
  coredump_dir /var/spool/squid3
EOF
/etc/init.d/squid restart
