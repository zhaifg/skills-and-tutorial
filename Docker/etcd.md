# etcd 手册
---
安装
cp etcd* /bin/
etcd --version

## 启动

mkdir /data/etcd
etcd --name etcserver --peer-addr 192.168.8.92
:7001 -addr 192.168.8.92:4001 -data-dir /data/etcd -peer-bind-addr 0.0.0.0:7001 -bind-addr 0.0.0.0:4001

sudo etcd -name etcdserver  --data-dir /data/etcd \
-listen-peer-urls http://192.168.8.88:2380 \
-listen-client-urls http://192.168.8.88:2379,http://127.0.0.1:2379 \
-advertise-client-urls http://192.168.8.88:2379,http://127.0.0.1:2379


curl -XPUT http://192.168.8.88:2379/v2/keys/app/servers/backstabbing_rosalind -d value="192.168.8.91:4501"

curl -XPUT http://192.168.8.88:2379/v2/keys/app/servers/cocky_morse -d value="192.168.8.91:4502"


v1.5.2
curl -LO https://storage.googleapis.com/kubernetes-release/release/v1.5.2/bin/linux/amd64/kubectl
