
# git 学习手册
---

## 1. 基本使用
`Git 全局设置`:
```
git config --global user.name "JenGuo Zhai"
git config --global user.email "zhaifengguo@gmail.com"
```

`创建 git 仓库`:
```
mkdir iRedAdmin
cd iRedAdmin
git init
touch README.md
git add README.md
git commit -m "first commit"
git remote add origin https://git.oschina.net/zhaifengguo/iRedAdmin.git
#git remote add origin git@git.oschina.net:zhaifengguo/iRedAdmin.git
git push -u origin master
```

`已有项目`?
```
cd existing_git_repo
git remote add origin https://git.oschina.net/zhaifengguo/iRedAdmin.git
#git remote add origin git@git.oschina.net:zhaifengguo/iRedAdmin.git
git push -u origin master
```

## 常见操作
git init
git status
git add [file]/-A
git commit -m 'init commit'


- 克隆Git项目的版本库到本地
- 更新本版本库从远程: git fetch
- 执行清理工作, 避免前一次编译的遗留下文件对编译造成影响: 这样的操作会丢弃本地对Git代码的改动
```
git clean  -fdx
git reset --hard
```

- 查看git 的版本: git tagg
- 检出该版本代码 git checkout v1.7


在默认设置下, 中文文件名在工作区状态输出, 查看历史更改概要, 以及补丁文件中, 文件名的中文不能正确的显示, 而是显示为八进制的字符编码

通过将git配置变量 core.quotepath 设置为 false
```
git config --global core.quotepath false
git status -s
```



### 远端仓库
* 添加仓库
git remote add origin https://github.com/jenguo/test.git
origin 为通常的远端名称.

* 上传到服务器 git push

    git push origin master

git clone 
git pull 更新代码
git add files 把当前文件放入暂存区域。

git commit 给暂存区域生成快照并提交。

git reset -- files 用来撤销最后一次git add files，你也可以用git reset 撤销所有暂存区域文件。

git checkout -- files 把文件从暂存区域复制到工作目录，用来丢弃本地修改。

你可以用 git reset -p, git checkout -p, or git add -p进入交互模式。


## git的分支
在版本回退里，你已经知道，每次提交，Git都把它们串成一条时间线，这条时间线就是一个分支。截止到目前，只有一条时间线，在Git里，这个分支叫主分支，即master分支。HEAD严格来说不是指向提交，而是指向master，master才是指向提交的，所以，HEAD指向的就是当前分支。

一开始的时候，master分支是一条线，Git用master指向最新的提交，再用HEAD指向master，就能确定当前分支，以及当前分支的提交点：

###  1.创建分支
```
    git checkout -b dev
```
上面的命令相当于
```
git branch dev
git checkout dev
```

### 2. 查看当前的分支
```
git branch
```

### 3. 切换分支
```
git checkout master
```

### 4. 合并分支
```
git merge dev
```

### 5. 删除分支
```
git branch -d dev
```


## 高级
### 1.比对两个不同的提交之间的差别
每次提交都有一个唯一id，查看所有提交和他们的id，可以使用 git log:

```
$ git log
 
commit ba25c0ff30e1b2f0259157b42b9f8f5d174d80d7
Author: Tutorialzine
Date:   Mon May 30 17:15:28 2016 +0300
 
    New feature complete
 
commit b10cc1238e355c02a044ef9f9860811ff605c9b4
Author: Tutorialzine
Date:   Mon May 30 16:30:04 2016 +0300
 
    Added content to hello.txt
 
commit 09bd8cc171d7084e78e4d118a2346b7487dca059
Author: Tutorialzine
Date:   Sat May 28 17:52:14 2016 +0300
 
    Initial commit

```

id 很长，但是你并不需要复制整个字符串，前一小部分就够了。
查看某一次提交更新了什么，使用 git show:
```
git show b10cc123
 
commit b10cc1238e355c02a044ef9f9860811ff605c9b4
Author: Tutorialzine
Date:   Mon May 30 16:30:04 2016 +0300
 
    Added content to hello.txt
 
diff --git a/hello.txt b/hello.txt
index e69de29..b546a21 100644
--- a/hello.txt
+++ b/hello.txt
  -0,0 +1
+Nice weather today, isn't it?
```

查看两次提交的不同，可以使用git diff [commit-from]..[commit-to] 语法
```
git diff 09bd8cc..ba25c0ff
 
diff --git a/feature.txt b/feature.txt
new file mode 100644
index 0000000..e69de29
diff --git a/hello.txt b/hello.txt
index e69de29..b546a21 100644
--- a/hello.txt
+++ b/hello.txt
  -0,0 +1
+Nice weather today, isn't it?
```

### 2.回滚某个文件到之前的版本
git 允许我们将某个特定的文件回滚到特定的提交，使用的也是 git checkout。

下面的例子，我们将hello.txt回滚到最初的状态，需要指定回滚到哪个提交，以及文件的全路径。
```
 git checkout 09bd8cc1 hello.txt
```

### 3.回滚提交

如果你发现最新的一次提交完了加某个文件，你可以通过 `git commit —amend`来修复，它会把最新的提交打回暂存区，并尝试重新提交。

如果是更复杂的情况，比如不是最新的提交了。那你可以使用`git revert`。

最新的一次提交别名也叫HEAD。
```
 git revert HEAD
 #or
 git revert b10cc123
```

### 4.解决合并冲突

冲突经常出现在合并分支或者是拉去别人的代码。有些时候git能自动处理冲突，但大部分需要我们手动处理。

比如John 和 Tim 分别在各自的分支上写了两部分代码。

```
// John 喜欢 for:
// Use a for loop to console.log contents.
for(var i=0; i console.log(arr[i]);
}

//Tim 喜欢 forEach:

// Use forEach to console.log contents.
arr.forEach(function(item) {
console.log(item);
});
```

假设John 现在去拉取 Tim的代码:
```
$ git merge tim_branch
 
Auto-merging print_array.js
CONFLICT (content): Merge conflict in print_array.js
Automatic merge failed; fix conflicts and then commit the result.
```

这时候git并不知道如何解决冲突，因为他不知道John和Tim谁写得更好。

于是它就在代码中插入标记。
```
HEAD
// Use a for loop to console.log contents.
for(var i=0; iarr.length; i++) {
    console.log(arr[i]);
}
=======
// Use forEach to console.log contents.
arr.forEach(function(item) {
    console.log(item);
});
>>>>>>> Tim s commit.
```

`====` 号上方是当前最新一次提交，下方是冲突的代码。我们需要解决这样的冲突，经过组委会成员讨论，一致认定，在座的各位都是垃圾！两个都不要。改成下面的代码。

```
// Not using for loop or forEach.
// Use Array.toString() to console.log contents.
console.log(arr.toString());
```

```
git add -A
$ git commit -m "Array printing conflict resolved."
```
如果在大型项目中，这个过程可能容易出问题。你可以使用GUI 工具来帮助你。使用 git mergetool。



## troubleshoot
但是有时候在项目开发过程中，突然心血来潮想把某些目录或文件加入忽略规则，按照上述方法定义后发现并未生效，原因是.gitignore只能忽略那些原来没有被track的文件，如果某些文件已经被纳入了版本管理中，则修改.gitignore是无效的。那么解决方法就是先把本地缓存删除（改变成未track状态），然后再提交：

```
git rm -r --cached .
git add .
git commit -m 'update .gitignore'
```

`warning: LF will be replaced by CRLF in .gitignore.`
`git config core.autocrlf false`

git config --global core.autocrlf  false


产生这个问题的原因是，windows、Linux和Mac在处理文件换行时的标示符是不一致的。windows使用CRLF作为结束符，而Linux和Mac使用LF作为结束符。

同时呢，Git 有两种模式来对待换行符，你可以通过下面这行代码查看你的git配置。

`$ git config core.autocrlf`
如果显示为true，则每一次当你git commit时，如果存在文本文件，那么git会自动帮你将末尾的换行符改为CRLF，省去了烦心的转换工作。

如果显示为false，则git不会对换行符进行修改，保持原本的内容。

所以呢，作为Linux和Mac开发者，这个配置应当为false，而windows开发者，则应当设置为true。

Linux mac
`$ git config --global core.autocrlf  false`

windows
` git config --global core.autocrlf  true`

## git 权威指南

全局的设置, 提交代码的人和邮件
```
git  config  --global user.name "zhaifg"
git  config  --global user.email 'zhaifengguo@gmail.com'
```

Git命令 设置别名
git config --system alias.st status
git config --system alias.ci commit
git config --global color.ui true 开启颜色显示

全局中的config: ~/.gitconfig
项目中的config: .git/config


查看提交信息

git log   | git log --pretty=fuller

重新设置 user.name 和user.email 
重新修改最新提交, 改正坐着和提交者的错误信息
git commit --amend --allow-empty  --reset-author 
`--amend`: 对刚刚的提交锦溪修补, 这样既可以改正前面的提交中错误的用户和邮件地址, 不会产生另外的新提交

`--allow-empty`: 允许空白提交
`--reset-author`: 将 提交者的ID同步修改, 否则只会影响提交者(Commit)的ID


### 暂存区
git log --stat 提交的详情

通过git diff 命令看到修改后的文件域版本库中文件的差异

### git 重置

git reset 命令, 可以将 游标 指向任意一个不存在的提交ID

git reset --hard HEAD^ # 相当于将master重置到上一个老的提交

`--hard` 参数, 会破坏工作区未提交的改动

git reset --hard 短的提交ID

用法一
`git reset [-q]  [commit] [--] <paths>`

用法二

```
git reset [--soft| --mixed | --hard | --merge | -keep ]  [-q]  [commit]
```


#### 使用reflog 挽救错误的重置
通过 .git/logs
查看工作区版本日志是否打开
git config  core.logallrefupdates




## git 的组织架构

### 工作区 (work directory)
就是你在电脑中看到的目录

### 版本库
工作区有一个 .git 隐藏目录, 这个是 版本库

版本库里存放了很多东西, 其中最终钟要就是 `stage (或者 index)`的暂存区,  还有git 为我们自动创建第一个分支master , 以及指向master的一个指针叫做HEAD

stash:
 还未提交的修改内容以及新添加的文件, 留在索引区或者工作树的情况下切换到其他分支时, 修改内容会从原来的分支移动到目标分支

stash 是临时保存文件修改内容的区域. stash可以暂时保存工作树话索引里还没有提交的修改内容, 事后可以取出暂存区的修改, 应用到原先的分支或其他分支上.



`远程的fetch`:
执行pull, 远程数据库的内容就会自动合并, 但是, 有事只是想确认本地数据库的内容,而不想合并, 这种情况下, 使用fetch.
执行fetch就可以取得远程的最新历史记录, 取得的提交会导入到没有名字的分支, 这个分支可以从名为 FETCH_HEAD 的 提出.


### git reflog

### git 恢复
git stash :  可以用于保存和恢复工作进度, 掌握这个命令对于日常的工作会有很大的帮助.

`git stash`:
保存当前的工作进度. 会分别对暂存区和工作区的状态进行保存.

`git stash list`:
显示进度列表. 此命令显然暗示了 git stash 可以多次保存工作进度, 并且在恢复的时候进行选择

`git stash pop [--index]  [<stash>]`
* 如果不使用任何参数, 会恢复最新保存的工作进度, 并将恢复工作进度从存储的工作进度列表中清除.

* 如果提供<stash> 参数(来自于 git stash list 显示的列表), 则从该<stash>中恢复. 恢复完毕也将从进度列表中删除

* 选项 `--index` 除了恢复工作区文件外, 还尝试恢复暂存区.

`git stash [save [--patch] [-k|--[no-] keep-index] [-q | --quiet]  [<message>] ]`
这一条命令 实际上是第一条 Git stash 命令的完整版.

`git stash apply [--index]  [<stash>]`
处理不删除恢复的进度之外, 其余和git stash pop 命令一样

`git stash drop [<stash>]`
删除一个存储的进度. 默认删除最新的进度

`git stash clear`:
删除所有存储的进度

`git stash branch <branchname> <stash>` 
基于进度创建分支.

```bash
shell> git stash list
shell>  echo "Bye-Bye." >> welcome.txt 
shell> echo "hello." > hack-1.txt
shell> git add hack-1.txt 
shell> git status -s
A  hack-1.txt
 M welcome.txt
shell> git stash save "hack-1: hacked welcome.txt, newfile hack-1.txt"
Saved working directory and index state On master: hack-1: hacked welcome.txt, newfile hack-1.txt
HEAD is now at bc141ab Merge commit '17b5ec5'
shell> git status -s
shell> ls
detached-commit.txt  new-commit.text  welcome.txt
shell> echo "fix." > hack-2.txt
shell> git stash 
No local changes to save
shell> git add hack-2.txt 
shell> git stash
Saved working directory and index state WIP on master: bc141ab Merge commit '17b5ec5'
HEAD is now at bc141ab Merge commit '17b5ec5'
shell> git stash list
stash@{0}: WIP on master: bc141ab Merge commit '17b5ec5'
stash@{1}: On master: hack-1: hacked welcome.txt, newfile hack-1.txt


ls -l .git/refs/stash .git/logs/refs/stash 
-rw-r--r-- 1 root root 358 Oct 18 11:03 .git/logs/refs/stash
-rw-r--r-- 1 root root  41 Oct 18 11:03 .git/refs/stash

shell> git reflog show refs/stash
ae501b1 refs/stash@{0}: WIP on master: bc141ab Merge commit '17b5ec5'
5a8eefd refs/stash@{1}: On master: hack-1: hacked welcome.txt, newfile hack-1.txt


shell >  git log --graph  --pretty=raw refs/stash -2
*   commit ae501b1ed28668001cc6a5455f37bd323a4d2047
|\  tree 1e6052befcf84717cebf95d54a3e393ea8809809
| | parent bc141abc0579c54e252dbee1f29b3474cda00402
| | parent d26a4035e87604a0f4548d42ff69e836a9130d97
| | author zhaifg <zhaifengguo@1mi.cn> 1508295798 +0800
| | committer zhaifg <zhaifengguo@1mi.cn> 1508295798 +0800
| | 
| |     WIP on master: bc141ab Merge commit '17b5ec5'
| |   
| * commit d26a4035e87604a0f4548d42ff69e836a9130d97
|/  tree 1e6052befcf84717cebf95d54a3e393ea8809809
|   parent bc141abc0579c54e252dbee1f29b3474cda00402
|   author zhaifg <zhaifengguo@1mi.cn> 1508295798 +0800
|   committer zhaifg <zhaifengguo@1mi.cn> 1508295798 +0800
|   
|       index on master: bc141ab Merge commit '17b5ec5'

```


