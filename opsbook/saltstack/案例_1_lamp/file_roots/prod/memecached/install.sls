include:
  - libevent.install

memcached-source-install:
   file.managed:
     - name: /usr/local/src/memcached-1.4.24.tar.gz
     - source: salt://memcached/files/memcached-1.4.24.tar.gz
     - user: root
     - group: root
     - mode: 644
  cmd.run:
    - name: cd /usr/local/src/ && tar xf memcached-1.4.24.tar.gz && cd memcached-1.4.24 && ./configure && make && make install
    - unless: test -d /usr/local/memcached
    - require:
      - cmd: libevent-source-isntall
      - file: memcached-source-install

