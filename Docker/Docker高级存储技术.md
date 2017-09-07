# Docker卷插件
---

## Convoy

Convoy是Docker的一种后端的卷插件, 一款简单的卷插件, 具有快照, 备份和恢复的功能, 使用go编写.

Docker的支持的后端存储:
1. Device Mapper
2. Virtual File Systrem(VFS)/Network File System(NFS)
3. Amazon Elastic Block Store(EBS)

### 安装
1. 安装最新版的Docker(>= 1.8+)
```
wget https://github.com/rancher/convoy/releases/download/v0.5.0/convoy.tar.gz
tar xf convoy.tar.gz
cp convoy/convoy/convoy-pdata_tools /usr/local/bin
mkdir -p /etc/docker/plugins/
sudo bash -C 'echo "unix:///var/run/convoy/convoy.sock" > /etc/docker/plugins/convoy.spec '
```

### 使用本地二进制文件块测试Device   Mapper driver上, 不稳定不能用于生产.
```
truncate -s 100G data.vol
truncate -s 1G metadata.vol
sudo losetup /dev/loop5 data.vol
sduo losetup /dev/loop6 metadata.vol

# 使用Convoy plugin daemon
convoy daemon --driver devicemapper --driver-opts dm.data=/dev/loop5 --driver-opts dm.metadatadev=/dev/loop6

# 创建一个基于convoy的容器, 测试我们创建/vol1/foo在 convoy volumes
sudo docker run -v vol1:/vol1 --volume-driver=convoy ubuntu touch /vol1/foo

# 做快照, 并把快照保存到本地(或者NFS或者S3)

sudo convoy snapshot create vol1 --name snap1vol1
sudo mkdir -p /opt/convoy
sudo convoy backup create snap1vol1 --dest vfs:///opt/convoy

# 可以在另一台主机上恢复
sudo convoy create res1 --backup <backup_url>

sudo docker run -v res1:/res1 --volume-driver=convoy ubuntu ls /res1/foo
```

## 基本操作
### 启动的convoy的daemon形式
- 1.Device Mapper方式
`convoy daemon -drivers devicemapper --driver-opts dm.datadev=/dev/convoy-vg/data --driver-opts dm.metadatadev=/dev/convoy-vg/metadata`
可以是用`---driver-opts dm.defaultvolumesize` 指定卷大小

- 2.NFS
  1. 先mount目录, <vfs_path>
    `sudo mkdir <vs_path>`
    `sudo mount -t nfs <nfs_server>:/path <vfs_path>`
  2. 启动daemon
    `sudo convoy daemon --driver vfs --driver-opts vfs.path=<vfs_path>`

- 3.EBS
  `convoy daemon --driver ebs`

### 卷命令
**新建卷**
`convoy crate volume_name`: 创建卷
  1. Device Mapper 默认的大小是100G, --size指定大小
  2. EBS 默认4G
  3. 创建也可以使用docker run: `docker run -it -v test_volume:/test  --volume-driver=convoy ubuntu`

**删除卷**
`convoy delete <volume_name>` or `docker rm -v <container_name>`
  1. `-r/ --reference` 操作只能删除当前主机的引用, 不能实际的删除.
  2. `docker rm -v` == `convoy delete -r`
  3. 使用--rm 删除所有在运行的且引用的容器的效果跟docker rm -v 的效果一样
  
**列出和查询**
```
sudo convoy list
sudo convoy inspect vol1
```

**做快照**
`convoy snapshot create vol1 --name snapvol1`

**删除快照**
`sudo convoy snapshot delete snapvol1`
Device Mapper:请确保您保留相同卷的最新备份快照以启用增量备份机制，因为Convoy需要它来计算快照之间的差异。

**备份快照**
在Device Mapper 和NFS我们可以备份快照到S3或者其他的NFS上
```
convoy backup  create snap1vol1 --dest s3://backup-buket@us-west-2/
# or
convoy backup create snap1vol1 --dest vfs:///opt/backup/
```
备份后会返回一个url
`s3://backup-bucket@us-west-2/?backup=f98f9ea1-dd6e-4490-8212-6d50df1982ea\u0026volume=e0d386c5-6a24-446c-8111-1077d10356b0`

**恢复**
`convoy create res1 --backup <url>``

**挂载一个恢复卷到容器中**
`docker run -it -v res1:/res1 --volume-driver convoy ubuntu`

**挂载一个NFS后端的卷到多个server上**
可以使用标准的docker run命令挂载到相同的NFS. 比如已经被挂载的vol1, 可以在其他容器里挂载
`docker run -it -v vol1:/vol1  --volume-driver=convoy ubuntu`

