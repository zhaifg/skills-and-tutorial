base:
  '*':
    - init.env_init
prod:
  '*':
    - cluster.haproxy-outside
    - cluster.haproxy-outside-keepalived
    - web.sls
  'saltstack-node2':
    - memcached.service


