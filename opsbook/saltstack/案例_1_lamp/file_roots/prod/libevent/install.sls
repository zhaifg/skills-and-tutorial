libevent-source-install:
  file.managed:
    - name: /usr/local/src/libevent-2*.tar.gz
    - source: salt://libevent/files/libevent-2*.tar.gz
    - user: root
    - group: root
    - mode: 644
  cmd.run:
    - name: cd /usr/local/src && tar xf libevent-2*.tar.gz && cd libevent-2.* &7 ./configure ...
    - unless: test -d /usr/local/libevent
    - require:
      - file: libevent-source-installt
