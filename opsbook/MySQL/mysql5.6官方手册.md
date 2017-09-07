# mysql 5.6 手册
---

##  PURGE BINARY LOGS 语法
```
PURGE { BINARY | MASTER } LOGS
    { TO 'log_name' | BEFORE datetime_expr }
```

```
PURGE BINARY LOGS TO 'mysql-bin.010';
PURGE BINARY LOGS BEFORE '2008-04-02 22:46:26';
```

在master上执行purge时,如果slave连着master这时purge是安全的, 如果slave没有的话,可能会导致slave连不上.

**怎么安全的purge log file**:
1. On each slave server, use `SHOW SLAVE STATUS` to check which log file it is reading.

2. Obtain a listing of the binary log files on the master server with `SHOW BINARY LOGS`.

3. Determine the earliest log file among all the slaves. This is the target file. If all the slaves are up to date, this is the last log file on the list.

4. Make a backup of all the log files you are about to delete. (This step is optional, but always advisable.)

5. Purge all log files up to but not including the target file.

变量:`expire_logs_days`
