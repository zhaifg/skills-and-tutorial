#shutil文件操作
---

## 常用的函数

1. `shutil.copy2(src, dst)`
2. `shutil.copytree(src, dst, symlinks=False, ignore=None)`
3. `shutil.rmtree(path[, ignore_errors[, onerror]])`
4. `shutil.move(src, dst)`

## 目录和文件操作

`shutil.copyfileobj(fsrc, fdst[, length])`
复制文件对象fsrc到fdst, length代表`buffer的大小, read(length)`


`shutil.copyfile(src, dst)`
复制文件src的内容(不包括metadata)到dst. dst必须是完整的文件名,dst也可以是个目录名称. src与dst不能是同一个文件, 如果是会抛出`Error`, 目标的目录必须是可写的,否则抛出`IOError`, 如果dst存在,则被替换. 特殊的文件如character与block devices和pipes不能被复制.


`shutil.copymode(src, dst)`
复制指定mode


`shutil.copystat(src, dst)`
复制文件的stat信息,如权限位,permission bits, last access time, last modification time, and flags 


`shutil.copy(src, dst)`

Copy the file src to the file or directory dst. If dst is a directory, a file with the same basename as src is created (or overwritten) in the directory specified. Permission bits are copied. src and dst are path names given as strings.

`shutil.copy2(src, dst)`
Similar to shutil.copy(), but metadata is copied as well – in fact, this is just `shutil.copy()` followed by `copystat()`. This is similar to the Unix command `cp -p`.

`shutil.ignore_patterns(*patterns)`
This factory function creates a function that can be used as a callable for copytree()‘s ignore argument, ignoring files and directories that match one of the glob-style patterns provided. See the example below.

`shutil.copytree(src, dst, symlinks=False, ignore=None)`
递归的复制目录,目标文件必须不存在. 使用copystat()复制,保留元信息.

- symlinks
 true:目录里的软连接会重新指定到目标文件,当symlinks为false或者忽略时,会复制一份到dst中.
- ignore: 
  如果此参数指定的话,参数必须是可以在copytree()调用的,使用os.listdir返回一个列表的内容


`shutil.rmtree(path[, ignore_errors[, onerror]])`


`shutil.move(src, dst)`



`exception shutil.Error`
This exception collects exceptions that are raised during a multi-file operation. For copytree(), the exception argument is a list of 3-tuples (srcname, dstname, exception).


##  Archiving operations


`shutil.make_archive(base_name, format[, root_dir[, base_dir[, verbose[, dry_run[, owner[, group[, logger]]]]]]])`
打包


`base_name` is the name of the file to create, including the path, minus any format-specific extension. format is the archive format: one of “zip”, “tar”, “bztar” or “gztar”.

`root_dir` is a directory that will be the root directory of the archive; ie. we typically chdir into root_dir before creating the archive.

`base_dir` is the directory where we start archiving from; ie. base_dir will be the common prefix of all files and directories in the archive.

`root_dir` and base_dir both default to the current directory.

`owner` and `group` are used when creating a tar archive. By default, uses the current owner and group.

`logger` must be an object compatible with PEP 282, usually an instance of logging.Logger.



`shutil.get_archive_formats()`
Return a list of supported formats for archiving. Each element of the returned sequence is a tuple (name, description).

By default shutil provides these formats:

gztar: gzip’ed tar-file
bztar: bzip2’ed tar-file
tar: uncompressed tar file
zip: ZIP file
You can register new formats or provide your own archiver for any existing formats, by using register_archive_format().



`shutil.register_archive_format(name, function[, extra_args[, description]])`
Register an archiver for the format name. function is a callable that will be used to invoke the archiver.

If given, extra_args is a sequence of (name, value) that will be used as extra keywords arguments when the archiver callable is used.

description is used by get_archive_formats() which returns the list of archivers. Defaults to an empty list.



`shutil.unregister_archive_format(name)`
Remove the archive format name from the list of supported formats.

New in version 2.7.

```python

from shutil import make_archive
>>> import os
>>> archive_name = os.path.expanduser(os.path.join('~', 'myarchive'))
>>> root_dir = os.path.expanduser(os.path.join('~', '.ssh'))
>>> make_archive(archive_name, 'gztar', root_dir)
'/Users/tarek/myarchive.tar.gz'
```

```
$ tar -tzvf /Users/tarek/myarchive.tar.gz
drwx------ tarek/staff       0 2010-02-01 16:23:40 ./
-rw-r--r-- tarek/staff     609 2008-06-09 13:26:54 ./authorized_keys
-rwxr-xr-x tarek/staff      65 2008-06-09 13:26:54 ./config
-rwx------ tarek/staff     668 2008-06-09 13:26:54 ./id_dsa
-rwxr-xr-x tarek/staff     609 2008-06-09 13:26:54 ./id_dsa.pub
-rw------- tarek/staff    1675 2008-06-09 13:26:54 ./id_rsa
-rw-r--r-- tarek/staff     397 2008-06-09 13:26:54 ./id_rsa.pub
-rw-r--r-- tarek/staff   37192 2010-02-06 18:23:10 ./known_hosts
```
