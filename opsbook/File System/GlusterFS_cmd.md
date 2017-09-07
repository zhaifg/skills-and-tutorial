# gluster 命令
```
volume info [all|<VOLNAME>] - list information of all volumes

volume create <NEW-VOLNAME> [stripe <COUNT>] [replica <COUNT> [arbiter <COUNT>]] [disperse [<COUNT>]] [disperse-data <COUNT>] [redundancy <COUNT>] [transport <tcp|rdma|tcp,rdma>] <NEW-BRICK>?<vg_name>... [force] - create a new volume of specified type with mentioned bricks

volume delete <VOLNAME> - delete volume specified by <VOLNAME>
volume start <VOLNAME> [force] - start volume specified by <VOLNAME>
volume stop <VOLNAME> [force] - stop volume specified by <VOLNAME>
volume tier <VOLNAME> status
volume tier <VOLNAME> start [force]
volume tier <VOLNAME> attach [<replica COUNT>] <NEW-BRICK>...
volume tier <VOLNAME> detach <start|stop|status|commit|[force]>

 - Tier translator specific operations.
volume attach-tier <VOLNAME> [<replica COUNT>] <NEW-BRICK>... - NOTE: this is old syntax, will be depreciated in next release. Please use gluster volume tier <vol> attach [<replica COUNT>] <NEW-BRICK>...
volume detach-tier <VOLNAME>  <start|stop|status|commit|force> - NOTE: this is old syntax, will be depreciated in next release. Please use gluster volume tier <vol> detach {start|stop|commit} [force]
volume add-brick <VOLNAME> [<stripe|replica> <COUNT> [arbiter <COUNT>]] <NEW-BRICK> ... [force] - add brick to volume <VOLNAME>
volume remove-brick <VOLNAME> [replica <COUNT>] <BRICK> ... <start|stop|status|commit|force> - remove brick from volume <VOLNAME>
volume rebalance <VOLNAME> {{fix-layout start} | {start [force]|stop|status}} - rebalance operations
volume replace-brick <VOLNAME> <SOURCE-BRICK> <NEW-BRICK> {commit force} - replace-brick operations
volume set <VOLNAME> <KEY> <VALUE> - set options for volume <VOLNAME>
volume help - display help for the volume command
volume log <VOLNAME> rotate [BRICK] - rotate the log file for corresponding volume/brick
volume log rotate <VOLNAME> [BRICK] - rotate the log file for corresponding volume/brick NOTE: This is an old syntax, will be deprecated from next release.
volume sync <HOSTNAME> [all|<VOLNAME>] - sync the volume information from a peer
volume reset <VOLNAME> [option] [force] - reset all the reconfigured options
volume profile <VOLNAME> {start|info [peek|incremental [peek]|cumulative|clear]|stop} [nfs] - volume profile operations
volume quota <VOLNAME> {enable|disable|list [<path> ...]| list-objects [<path> ...] | remove <path>| remove-objects <path> | default-soft-limit <percent>} |
volume quota <VOLNAME> {limit-usage <path> <size> [<percent>]} |
volume quota <VOLNAME> {limit-objects <path> <number> [<percent>]} |
volume quota <VOLNAME> {alert-time|soft-timeout|hard-timeout} {<time>} - quota translator specific operations
volume inode-quota <VOLNAME> enable - quota translator specific operations
volume top <VOLNAME> {open|read|write|opendir|readdir|clear} [nfs|brick <brick>] [list-cnt <value>] |
volume top <VOLNAME> {read-perf|write-perf} [bs <size> count <count>] [brick <brick>] [list-cnt <value>] - volume top operations
volume status [all | <VOLNAME> [nfs|shd|<BRICK>|quotad]] [detail|clients|mem|inode|fd|callpool|tasks] - display status of all or specified volume(s)/brick
volume heal <VOLNAME> [enable | disable | full |statistics [heal-count [replica <HOSTNAME:BRICKNAME>]] |info [healed | heal-failed | split-brain] |split-brain {bigger-file <FILE> | latest-mtime <FILE> |source-brick <HOSTNAME:BRICKNAME> [<FILE>]}] - self-heal commands on volume specified by <VOLNAME>
volume statedump <VOLNAME> [nfs|quotad] [all|mem|iobuf|callpool|priv|fd|inode|history]... - perform statedump on bricks
volume list - list all volumes in cluster
volume clear-locks <VOLNAME> <path> kind {blocked|granted|all}{inode [range]|entry [basename]|posix [range]} - Clear locks held on path
volume barrier <VOLNAME> {enable|disable} - Barrier/unbarrier file operations on a volume
volume get <VOLNAME> <key|all> - Get the value of the all options or given option for volume <VOLNAME>
volume bitrot <VOLNAME> {enable|disable} |
volume bitrot <volname> scrub-throttle {lazy|normal|aggressive} |
volume bitrot <volname> scrub-frequency {hourly|daily|weekly|biweekly|monthly} |
volume bitrot <volname> scrub {pause|resume|status} - Bitrot translator specific operation. For more information about bitrot command type  'man gluster'
peer probe { <HOSTNAME> | <IP-address> } - probe peer specified by <HOSTNAME>
peer detach { <HOSTNAME> | <IP-address> } [force] - detach peer specified by <HOSTNAME>
peer status - list status of peers
peer help - Help command for peer 
pool list - list all the nodes in the pool (including localhost)
quit - quit
help - display command options
exit - exit
snapshot help - display help for snapshot commands
snapshot create <snapname> <volname> [no-timestamp] [description <description>] [force] - Snapshot Create.
snapshot clone <clonename> <snapname> - Snapshot Clone.
snapshot restore <snapname> - Snapshot Restore.
snapshot status [(snapname | volume <volname>)] - Snapshot Status.
snapshot info [(snapname | volume <volname>)] - Snapshot Info.
snapshot list [volname] - Snapshot List.
snapshot config [volname] ([snap-max-hard-limit <count>] [snap-max-soft-limit <percent>]) | ([auto-delete <enable|disable>])| ([activate-on-create <enable|disable>]) - Snapshot Config.
snapshot delete (all | snapname | volume <volname>) - Snapshot Delete.
snapshot activate <snapname> [force] - Activate snapshot volume.
snapshot deactivate <snapname> - Deactivate snapshot volume.
global help - list global commands
nfs-ganesha {enable| disable}  - Enable/disable NFS-Ganesha support

```


