# MySQLdb与DBUtils的使用
---
MySQLdb

## _mysql module
_mysql模块直接MySQL的C语言的api, 不是很兼容Python DB API接口. 大多数程序园使用`MySQLdb`

```python
#!/usr/bin/python
# -*- coding: utf-8 -*-

import _mysql
import sys

try:
    con = _mysql.connect('localhost', 'testuser', 'test623', 'testdb')
        
    con.query("SELECT VERSION()")
    result = con.use_result()
    
    print "MySQL version: %s" % \
        result.fetch_row()[0]
    
except _mysql.Error, e:
  
    print "Error %d: %s" % (e.args[0], e.args[1])
    sys.exit(1)

finally:
    
    if con:
        con.close()
```


## MySQLdb module
MySQLdb 重新包装了 `_mysql`

### 基本语法
```python
#连接数据库,得到一个数据库连接
conn_db = MySQLdb.connect(host=MY_HOST, user=MY_USER, passwd=MY_PASS, db=MY_DB)

# 得到一个游标
cursor = conn_db.cursor()

# 执行一个sql语句
cursor.execute(sql)

# 得到结果
results = cursor.fetchall()

# 关闭连接
cursor.close()
conn_db.close()
```

### Exceptions & Errors
'MySQLdb.Error'


```python
# Get data from database
try:
    cur.execute("SELECT * FROM song")
    rows = cur.fetchall()
except MySQLdb.Error, e:
    try:
        print "MySQL Error [%d]: %s" % (e.args[0], e.args[1])
    except IndexError:
        print "MySQL Error: %s" % str(e)
# Print results in comma delimited format
for row in rows:
    for col in row:
        print "%s," % col
    print "\n"
```

## example

### First example


```python
#!/usr/bin/python
# -*- coding: utf-8 -*-

import MySQLdb as mdb
import sys

try:
    con = mdb.connect('localhost', 'testuser', 'test623', 'testdb');

    cur = con.cursor()
    cur.execute("SELECT VERSION()")

    ver = cur.fetchone()
    
    print "Database version : %s " % ver
    
except mdb.Error, e:
  
    print "Error %d: %s" % (e.args[0],e.args[1])
    sys.exit(1)
    
finally:    
        
    if con:    
        con.close()
```

### 2. Creating and populating a table

```python
#!/usr/bin/python
# -*- coding: utf-8 -*-

import MySQLdb as mdb

con = mdb.connect('localhost', 'testuser', 'test623', 'testdb');

with con:
    
    cur = con.cursor()
    cur.execute("DROP TABLE IF EXISTS Writers")
    cur.execute("CREATE TABLE Writers(Id INT PRIMARY KEY AUTO_INCREMENT, \
                 Name VARCHAR(25))")
    cur.execute("INSERT INTO Writers(Name) VALUES('Jack London')")
    cur.execute("INSERT INTO Writers(Name) VALUES('Honore de Balzac')")
    cur.execute("INSERT INTO Writers(Name) VALUES('Lion Feuchtwanger')")
    cur.execute("INSERT INTO Writers(Name) VALUES('Emile Zola')")
    cur.execute("INSERT INTO Writers(Name) VALUES('Truman Capote')")
```

`with con:`
With the with keyword, the Python interpreter automatically releases the resources. It also provides error handling.

```
mysql> SELECT * FROM Writers;
+----+-------------------+
| Id | Name              |
+----+-------------------+
|  1 | Jack London       |
|  2 | Honore de Balzac  |
|  3 | Lion Feuchtwanger |
|  4 | Emile Zola        |
|  5 | Truman Capote     |
+----+-------------------+
5 rows in set (0.00 sec)
```


### 取数据

```python
#!/usr/bin/python
# -*- coding: utf-8 -*-

import MySQLdb as mdb

con = mdb.connect('localhost', 'testuser', 'test623', 'testdb');

with con: 

    cur = con.cursor()
    cur.execute("SELECT * FROM Writers")

    rows = cur.fetchall()

    for row in rows:
        print row
```

`rows = cur.fetchall()`
`fetchall()` 方法是得到所有的结果集.得到一个tuple.((col1,col2,..),(col1,col2,...),...)
The fetchall() method gets all records. It returns a result set. Technically, it is a tuple of tuples. Each of the inner tuples represent a row in the table.


### 按行取得数据
```python
#!/usr/bin/python
# -*- coding: utf-8 -*-

import MySQLdb as mdb

con = mdb.connect('localhost', 'testuser', 'test623', 'testdb');

with con:

    cur = con.cursor()
    cur.execute("SELECT * FROM Writers")

    for i in range(cur.rowcount):
        
        row = cur.fetchone()
        print row[0], row[1]
```


### 字典类型的光标
MySQLdb有多个cursor的类型.默认是元组的类型. 字典类型的cursor,会返回列名.

```python
#!/usr/bin/python
# -*- coding: utf-8 -*-

import MySQLdb as mdb

con = mdb.connect('localhost', 'testuser', 'test623', 'testdb')

with con:

    cur = con.cursor(mdb.cursors.DictCursor)
    cur.execute("SELECT * FROM Writers LIMIT 4")

    rows = cur.fetchall()

    for row in rows:
        print row["Id"], row["Name"]
```

```
$ ./dictcur.py
1 Jack London
2 Honore de Balzac
3 Lion Feuchtwanger
4 Emile Zola
```

### 表头

```python
#!/usr/bin/python
# -*- coding: utf-8 -*-

import MySQLdb as mdb

con = mdb.connect('localhost', 'testuser', 'test623', 'testdb')

with con:

    cur = con.cursor()
    cur.execute("SELECT * FROM Writers LIMIT 5")

    rows = cur.fetchall()

    desc = cur.description

    print "%s %3s" % (desc[0][0], desc[1][0])

    for row in rows:    
        print "%2s %3s" % row
```
```

$ ./columnheaders.py
Id Name
 1 Jack London
 2 Honore de Balzac
 3 Lion Feuchtwanger
 4 Emile Zola
 5 Truman Capote
```


### Prepared statements

```python

#!/usr/bin/python
# -*- coding: utf-8 -*-

import MySQLdb as mdb

con = mdb.connect('localhost', 'testuser', 'test623', 'testdb')
    
with con:    

    cur = con.cursor()
        
    cur.execute("UPDATE Writers SET Name = %s WHERE Id = %s", 
        ("Guy de Maupasant", "4"))        

    print "Number of rows updated:",  cur.rowcount
```

### Inserting images

```python
#!/usr/bin/python
# -*- coding: utf-8 -*-

import MySQLdb as mdb


def read_image():
    
    fin = open("woman.jpg")    
    img = fin.read()
    
    return img
    

con = mdb.connect('localhost', 'testuser', 'test623', 'testdb')
 
with con:
    
    cur = con.cursor()
    data = read_image()
    cur.execute("INSERT INTO Images VALUES(1, %s)", (data, ))
```

### Reading images

```python
#!/usr/bin/python
# -*- coding: utf-8 -*-

import MySQLdb as mdb 

def writeImage(data):
    
    fout = open('woman2.jpg', 'wb')
    
    with fout:
        
        fout.write(data)

con = mdb.connect('localhost', 'testuser', 'test623', 'testdb')

with con:

    cur = con.cursor()

    cur.execute("SELECT Data FROM Images WHERE Id=1")
    data = cur.fetchone()[0]
    writeImage(data)    
```

###  事务支持Transaction support

```python
#!/usr/bin/python
# -*- coding: utf-8 -*-

import MySQLdb as mdb
import sys


try:
    con = mdb.connect('localhost', 'testuser', 'test623', 'testdb')

    cur = con.cursor()
    cur.execute("DROP TABLE IF EXISTS Writers")
    cur.execute("CREATE TABLE Writers(Id INT PRIMARY KEY AUTO_INCREMENT, \
                 Name VARCHAR(25)) ENGINE=INNODB")
    cur.execute("INSERT INTO Writers(Name) VALUES('Jack London')")
    cur.execute("INSERT INTO Writers(Name) VALUES('Honore de Balzac')")
    cur.execute("INSERT INTO Writers(Name) VALUES('Lion Feuchtwanger')")
    cur.execute("INSERT INTO Writers(Name) VALUES('Emile Zola')")
    cur.execute("INSERT INTO Writers(Name) VALUES('Truman Capote')")
    cur.execute("INSERT INTO Writers(Name) VALUES('Terry Pratchett')")
    
    con.commit()

    
except mdb.Error, e:
  
    if con:
        con.rollback()
        
    print "Error %d: %s" % (e.args[0],e.args[1])
    sys.exit(1)
    
finally:    
            
    if con:    
        con.close()
```


>> MySQLdb 的 Connection 对象支持上下文管理, 它可以自动提交或者回滚事务
使用上下文管理可以简洁代码.

打发

```python
#!/usr/bin/python
# -*- coding: utf-8 -*-

import MySQLdb as mdb

con = mdb.connect('localhost', 'testuser', 'test623', 'testdb')

with con:
    
    cur = con.cursor()
    cur.execute("DROP TABLE IF EXISTS Writers")
    cur.execute("CREATE TABLE Writers(Id INT PRIMARY KEY AUTO_INCREMENT, \
                 Name VARCHAR(25))")
    cur.execute("INSERT INTO Writers(Name) VALUES('Jack London')")
    cur.execute("INSERT INTO Writers(Name) VALUES('Honore de Balzac')")
    cur.execute("INSERT INTO Writers(Name) VALUES('Lion Feuchtwanger')")
    cur.execute("INSERT INTO Writers(Name) VALUES('Emile Zola')")
    cur.execute("INSERT INTO Writers(Name) VALUES('Truman Capote')")
    cur.execute("INSERT INTO Writers(Name) VALUES('Terry Pratchett')"
```
### 批量插入

`executemany(sql, param)`  param为[(col1,col2),(col1,col2)]


```python
#  要插入的结果集为[(col1,col2),(col1,col2),(col1,col2)]
sql =  """insert into ym_analysis_browsejob (token, user_id, os, job_id, browse_time, create_time) values (%s, %s, %s, %s, %s, %s)"""

# 生成相应的param结构:[(),()]

params= [rst for rst in results]

slave = MySQLdb.connect('127.0.0.1', user='root', passwd='', port=10097, db='yimi_work')
cursor = slave.cursor()
cursor.excutemany(sql, params)
slave.commit()

```
