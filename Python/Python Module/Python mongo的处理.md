# Python的mongo处理
---

```python
import pymongo
# 导入MongoClient
from pymongo import MongoClient
# 创建client
client = MongoClient()
client = MonogoClient("localhost", 27017)
client = MonogoClient("mogno://localhost:27017")

# 连接数据库
db = client.test_database
db = client["test_database"]

# 得到数据集
collection = db.test_collection
collection = db['test_collection']

# post实例
import datetime
post = {"author": "Mike",
        "text": "My first blog post!",
        "tags": ["mongodb", "python", "pymongo"],
        "date": datetime.datetime.utcnow()}
posts = db.posts
post_id = posts.insert_one(post).inserted_id

# get one
posts.find_one()
posts.find_one(["author": "mike"])

# 批量插入
new_posts = [{"author": "Mike",
              "text": "Another post!",
              "tags": ["bulk", "insert"],
              "date": datetime.datetime(2009, 11, 12, 11, 14)},
             {"author": "Eliot",
              "title": "MongoDB is fun",
              "text": "and pretty easy too!",
              "date": datetime.datetime(2009, 11, 10, 10, 45)}]

result = posts.insert_many(new_posts)
# 批量查询
posts.find()

# 计数
posts.count()
```
