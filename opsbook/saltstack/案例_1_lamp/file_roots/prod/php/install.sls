pkg-php:
  pkg.installed:
    - names:
      - mysql-devel
      - openssl-devel
      - swig
      - libjpeg-turbo
      - libjpeg-turbo-devel
      - libpng
      - libpng-devel
      - freetype
      - freetype-devel
      - libxml2
      - libxml2-devel
      - zlib
      - zlib-devel
      - libcurl
      - libcurl-devel

php-source-install:
  file.managed:
    - name: /usr/local/src/php-*.tar.gz
    - source: salt://php/files/php-*.tar.gz
    - user: root
    - group: root
    - mode: 755

  cmd.run:
    - name: cd /usr/local/src && tar xf php-*.tar.gz && cd php-* && ./configure &&make && make install
    - require:
      - file: php-source-install
      - user: www-user-group
    - unless: test -d /usr/local/php-fastcgi

pdo-plugin:
  cmd.run:
    - name: cd /usr/local/src/php-*/ext/pdo_mysql && phpize && ./configure && make && make install
    - unless: test -f /usr/local/php-fastcgi/lib/extensions/*/pdo_mysql.so
    - require:
      - cmd: php-source-install

php-ini:
  file-managed:
    - name: /usr/local/php-fastcgi/etc/php.ini
    - source: salt://php/files/php.ini-production
    - user: root
    - group: root
    - mode: 644

php-fpm:
  file.managed:
    - name: /usr/local/php-fastcgi/etc/php-fpm.conf
    - source: salt://php/files/php-fpm.conf.default
    - user: root
    - group: root
    - mode: 644

php-fastcgi-service:
  file.managed:
    - name: /etc/init.d/php-fpm- source: salt://php/files/init.d.php-fpm
    - user: root
    - group: root
    - mode: 755
  cmd.run:
    - name: chkconfig --add php-fpm
    - unless: chkconfig --list | grep php-fpm
    - require:
      - file: php-fastcgi-service

service.running:
  - name: php-fpm
  - enable: True
  - require:
    - cmd: php-fastcgi-service
  - watch:
    - file: php-ini
    - file: php-fpm
