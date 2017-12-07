# 利用curl 对url请求的时间的
---


curl-format.txt 
```
time_namelookup:  %{time_namelookup}\n
       time_connect:  %{time_connect}\n
    time_appconnect:  %{time_appconnect}\n
      time_redirect:  %{time_redirect}\n
   time_pretransfer:  %{time_pretransfer}\n
 time_starttransfer:  %{time_starttransfer}\n
                    ----------\n
         time_total:  %{time_total}\n
```

curl  -w "@curl-format.txt" -o /dev/null -s -L  http://www.baidu.com
