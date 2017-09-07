# Docker常用命令
---
清理所有未打过标签的本地镜像
`docker rmi $(docker images -q -f "dangling=true")`
`docker rmi $(docker images --quiet --filter "dangling=true")`
