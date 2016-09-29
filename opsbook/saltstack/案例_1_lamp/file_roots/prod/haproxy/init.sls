include:
  - pkg.pkg-init
haproxy-install:
  file.managed:
    - name: /usr/local/src/haproxy-1.6.9.tar.gz
    - source: salt://haproxy/files/haproxy-1.6.9.tar.gz
    - mode: 755
    - user: root
    - group: root
  cmd.run:
    - name: cd /usr/local/src && tar -zxf haproxy.1.6.9.tar.gz -C haproxy && ./configure && make && make install
    - unless: test -d /usr/local/haproxy
    - require:
      - pkg: pkg-init
      - file: haprxoy-install

/etc/init.d/haproxy:
  file.managed:
    - source: salt://haproxy/files/haproxy.init.d
    - mode: 755
    - user: root
    - group: root
    - require:
      - cmd: haproxy-install

net.ipv4.ip_nonlocal_bind:
  sysctl.present:
    - value: 1

haproxy-config-dir:
  file.directory:
    - name: /etc/haproxy
    - mode: 755
    - user: root
    - group: root

haproxy-init:
  cmd.run:
    - name: chkconfig --add haproxy
    - unless: chkconfig --list |grep haproxy
    - require:
      - file: /etc/init.d/haproxy

