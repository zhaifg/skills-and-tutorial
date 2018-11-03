# SQLAlchemy Model to Dictionary
---


https://wakatime.com/blog/32-flask-part-1-sqlalchemy-models-to-json
## SQLAlchemy Model to Dictionary
```python
from flask import json
from cmdb.extensions import db
from sqlalchemy.orm.attributes import QueryableAttribute


class BaseModel(db.Model):
    __abstract__ = True

    def to_dict(self, show=None, _hide=[], _path=None):
        """
            返回这个的model 的字典
        """
        show = show or []

        hidden = self._hidden_fields if hasattr(self, "_hidden_fields") else []
        default = self._default_fields if hasattr(self, "_default_fields") else []
        default.extend(["id", "modified_at", "created_at"])

        if not _path:
            _path = self.__tablename__.lower()

            def prepend_path(item):
                item = item.lower()
                if item.split(".", 1)[0] == _path:
                    return item
                if len(item) == 0:
                    return item
                if item[0] != ".":
                    item = ".%s" % item
                item = "%s%s" %(_path, item)
                return item

            _hide[:] = [prepend_path(x) for x in _hide]
            show[:] = [prepend_path(x) for x in show ]

        columns = self.__table__.columns.keys()
        relationships = self.__mapper__.relationships.keys()
        properties = dir(self)

        ret_data = {}

        for key in columns:
            if key.startswith("_"):
                continue
            check = "%s.%s" %(_path, key)
            if check in _hide or key in hidden:
                continue
            if check in show or key in default:
                ret_data[key] = getattr(self, key)

        for key in relationships:
            if key.startswith("_"):
                continue
            check = "%s.%s" % (_path, key)
            if check in _hide or key in hidden:
                continue
            if check in show or key in default:
                _hide.append(check)
                is_list = self.__mapper__.relationships[key].uselist
                if is_list:
                    items = getattr(self, key)
                    if self.__mapper__.relationships[key].query_class is not None:
                        if hasattr(items, "all"):
                            items = items.all()
                    ret_data[key] = []
                    for item in items:
                        ret_data[key].append(
                            item.to_dict(
                                show=list(show),
                                _hide=list(_hide),
                                _path=("%s.%s" %(_path, key.lower())),
                            )
                        )
                else:
                    if (
                        self.__mapper__.relations[key].query_class is not None
                        or self.__mapper__.relations[key].instrument_class is not None
                    ):
                        item = getattr(self, key)
                        if item is not None:
                            ret_data[key] = item.to_dict(
                                show=list(show),
                                _hide=list(_hide),
                                _path=("%s.%s" % (_path, key.lower()))
                            )
                        else:
                            ret_data[key] = None
                    else:
                        ret_data[key] = getattr(self, key)

        for key in list(set(properties) - set(columns) - set(relationships)):
            if key.startswith("_"):
                continue
            if not hasattr(self._class__, key):
                continue
            attr = getattr(self.__class__, key)
            if not (isinstance(attr, property) or isinstance(attr, QueryableAttribute)):
                continue

            check = "%s.%s" % (_path, key)
            if check in _hide or key in hidden:
                continue
            if check in show or key in default:
                val = getattr(self, key)
                if hasattr(val, "to_dict"):
                    ret_data[key] = val.to_dict(
                        show=list(show),
                        _hide=list(_hide),
                        _path=("%s.%s" % (_path, key.lower()))
                    )
                else:
                    try:
                        ret_data[key] = json.loads(json.dumps(val))
                    except:
                        pass

        return ret_data



class User(BaseModel):
    id = db.Column(UUID(), primary_key=True, default=uuid.uuid4)
    username = db.Column(db.String(), nullabe=False, unique=True)
    password = db.Column(db.String())
    email_confirmed = db.Column(db.Boolean())
    modified_at = db.Column(db.DateTime())
    created_at = db.Column(db.DateTime(), nullable=False, default=datetime.utcnow)

    _default_fields = [
        "username",
        "joined_recently",
    ]
    _hidden_fields = [
        "password",
    ]
    _readonly_fields = [
        "email_confirmed",
    ]

    @property
    def joined_recently(self):
        return self.created_at > datetime.utcnow() - timedelta(days=3)

user = User(username="zzzeek")
db.session.add(user)
db.session.commit()

print(user.to_dict())

```


output
```
{
    'id': UUID('488345de-88a1-4c87-9304-46a1a31c9414'),
    'username': 'zzzeek',
    'joined_recently': True,
    'modified_at': None,
    'created_at': datetime.datetime(2018, 7, 11, 6, 28, 56, 905379),
}


json.dumps(user.to_dict())
```
