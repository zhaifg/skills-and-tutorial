include:
  - pcre.install
  - user.www
nginx-source-install:
  file.managed:
    - name: /usr/local/src/nginx-1*.tar.gz
    - source: salt://nginx/files/
    - user: root
    - group: root
    - mode: root
  cmd.run:
    - name: cd /usr/local/src/nginx-1*.tar.gz && tar xf nginx-1*.tar.gz && cd * && make
    - unless: test -d /usr/local/nginx
    - require:
      - user: www-user-group
      - pkg: pkg.init
      - cmd: pcre-source-install

