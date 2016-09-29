include:
  - memcached.install
  - user.www

memcached-service:
  cmd.run:
    - name: /usr/local/memcached/bin/memcached -d
    - unless: netstat -antpl|grep 11211
    - require:
      - cmd: memcached-source-install
      - user: www-user-group

