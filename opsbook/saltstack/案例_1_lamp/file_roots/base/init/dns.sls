/etc/resolv.conf:
  file.managed:
    file.managed:
      - source: salt://init/files/resolv.conf
      - user: root
      - group: root
      - mode: 644
