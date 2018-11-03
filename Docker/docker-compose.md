# docker compose 语法
---
Version 3

## Services

### build
```yaml
version: '3'
services:
  webapp:
    build: ./dir

# 
version: '3'
services:
  webapp:
    build:
      context: ./dir
      dockerfile: Dockerfile-alternate
      args:
        buildno: 1

# 指定image build
build: ./dir
image: webapp:tag


```

* build
  * context: 指向dockerfile的目录或者git url
  * dockerfile: 
  * args: 添加生成参数，这些参数是仅在生成过程中访问的环境变量。
  * cache_from
  * labels
  * shm_size
  * target
  
* cap_add, cap_drop
* command
* configs
  * short syntax
  * long syntax
* cgroup_parent
* container_name
* credential_spec

* deploy
  * ENDPOINT_MODE
  * LABELS
  * MODE
  * PLACEMENT
  * replicas
  * resources
  * restart_policy
  * ROLLBACK_CONFIG
  * UPDATE_CONFIG
  * not supported for docker stack deploy

* devices
* depends_on
* dns:
* dns_search
* tmpfs
* entrypoint
* env_file
* environment
* expose
* external_links
* extra_hosts
* healthcheck
* image
* init
* isolation
* labels
* links
* logging
* network_mode
* networks
  * alias
  * ipv4_address, ipv6_address
* pid
* ports
  1. short syntax
  2. long syntax
* sercets:
  1. short
  2. long
* security_opt
* stop_grace_period
* stop_signal
* sysctls
* ulimits
* userns_mode
* voluems
  1. short
  2. long
  3. volumesfor servicesx, swarms, and stack files
  4. caching options for volume mounts(docker for mac)
* domainname, hostname, ipc, mac_address, privileged, read_only, shm_size, stdin_open, tty, user, working_dir

ALIASES

IPV4_ADDRESS, IPV6_ADDRESS
