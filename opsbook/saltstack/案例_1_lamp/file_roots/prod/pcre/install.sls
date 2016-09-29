pcre-source-install:
  file.managed:
    - name: /usr/local/src/pcre-*.tar.gz
    - source: salt://pcre/files/pcre-*.tar.gz
    - user: root
    - group: root
    - mode: 755
  cmd.run:
    - name: cd /usr/local/src/ && tar xf && cd pcre && ./configure && make && make install
    - unless: tset -d /usr/local/pcre
    - require:
      - file: pcre-source-install
