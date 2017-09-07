mysql -usqladmin -pyz11235 -h127.0.0.1   -e "show slave status\G" | awk -F ":" '$1 ~ /Slave_IO_Running|Slave_SQL_Running$/{if($2~/Yes/)s++}END{print s}'





7485
sed -n '/# Time: 160420 13:00:00/, /# Time: 160420 18:00:00/'

160420 13:00:00

160420 18:00:00

# Time: 160420 13:00:00

grant ALL privileges  ON slow_query_log.* to 'anemometer'@'127.0.0.1' IDENTIFIED BY 'superSecurePass';



pt-table-checksum  --nocheck-replication-filters --replicate=test.checksums --databases=test h=127.0.0.1,u=root,p=yimiwork321 --port 10097

 mysql -uroot -pyimiwork321 -h 127.0.0.1

pt-table-sync --replicate=test.checksums h=127.0.0.1,u=root,p=yimiwork321 h=127.0.0.1,u=root,p=111111 --charset=utf8 --print


 pt-table-sync --replicate=test.checksums h=127.0.0.1,u=root,p=yimiwork321,P 10097,h=127.0.0.1,u=root,p=yimiwork321,P 10098 --charset=utf8 --print


  GRANT select,insert,update,delete,create,process,super,replication slave ON *.* TO monitor@'%' IDENTIFIED BY '111111';



pt-table-checksum  --nocheck-replication-filters --replicate=test.yimi_workchecksums --databases=yimi_work h=127.0.0.1,u=root,p=yimiwork321  --port 10097




pt-table-checksum  --nocheck-replication-filters --replicate=test.checksums --databases=yimi_im,yimi_work h=127.0.0.1,u=root,p=yimi20131111Jsqwbcxl --port 10097





 pt-table-sync --replicate=test.checksums h=127.0.0.1,u=root,p=yimiwork321,P 10097,h=127.0.0.1,u=root,p=yimiwork321,P 10098 --charset=utf8 --print


 pt-table-sync \
    --execute \
    --replicate=percona.checksums \
    --charset=<CHARSET> \
    --host=<MASTER_HOST> \
    --user=<MASTER_USER> \
    --password=<MASTER_PASSWORD>

    pt-table-sync \
    --print \
    --replicate=test.yimi_workchecksums \
    --charset=utf8 \
    --host=127.0.0.1 \
    --user=root \
    --password=yimiwork321 --port 10097


    1. 测试master有但是slave上
