# bash 用法常规技巧
---

## 打印错误
```
err() {
    echo "[$(date +'%Y-%m-%dT%H:%M:%S%z')]: $@" >&2
}

if ! do_something; then
    err "Unable to do_something"
    exit "${E_DID_NOTHING}"
fi
```

## bash 检查是否是数字
```bash
re='^[0-9]+$'
if ! [[ $yournumber =~ $re ]] ; then
   echo "error: Not a number" >&2; exit 1
fi
```

select  DATE(create_time), count(1) from ym_customer where create_time BETWEEN '2017-01-01 00:00:00' and '2018-05-31 23:59:59' group by  DATE(create_time) into outfile '/tmp/reg.csv' FIELDS TERMINATED BY ',' OPTIONALLY ENCLOSED BY'"';
