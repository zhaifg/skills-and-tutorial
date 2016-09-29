common {
    protocol C;
    handlers {
        # 当承载drbd的物理文件损坏时处理
        # echo b > /proc/sysrq-trigger
        # 立即重启机器，而且不会将缓冲区同步到硬盘，也不会卸载已挂载的硬盘
        pri-on-incon-degr "/usr/lib/drbd/notify-pri-on-incon-degr.sh; /usr/lib/drbd/
notify-emergency-reboot.sh; echo b > /proc/sysrq-trigger ; reboot -f";

        # 当同步过程中主设备失去联系处理
        # echo b > /proc/sysrq-trigger
        # 立即重启机器，而且不会将缓冲区同步到硬盘，也不会卸载已挂载的硬盘
        pri-lost-after-sb "/usr/lib/drbd/notify-pri-lost-after-sb.sh; /usr/lib/drbd/
notify-emergency-reboot.sh; echo b > /proc/sysrq-trigger ; reboot -f";

        # 当同步过程中发生io错误处理
        # echo o > /proc/sysrq-trigger
        # 关闭系统
        local-io-error "/usr/lib/drbd/notify-io-error.sh; /usr/lib/drbd/
notify-emergency-shutdown.sh; echo o > /proc/sysrq-trigger ; halt -f";

        # fence-peer "/usr/lib/drbd/crm-fence-peer.sh";
        # split-brain "/usr/lib/drbd/notify-split-brain.sh root";
        # out-of-sync "/usr/lib/drbd/notify-out-of-sync.sh root";
        # before-resync-target "/usr/lib/drbd/snapshot-resync-target-lvm.sh -p 15 
-- -c 16k";
        # after-resync-target /usr/lib/drbd/unsnapshot-resync-target-lvm.sh;
    }
    startup {
        #wfc-timeout 120;
        #degr-wfc-timeout 120;
    }
    disk {
        # 当磁盘io异常,将分离当前设备
        on-io-error detach;
        #fencing resource-only;
    }
    net {
        # 消息验证校验码
        cram-hmac-alg "sha1";
        shared-secret "9bb9f0ea87ca30cfbc094c7dad12d1ea";
        # openssl dgst sha1 install.log 对任意文件进行信息摘要取得交换码
    }
    syncer {
        # drbd设备同步速率
        rate 1000M;
    }
