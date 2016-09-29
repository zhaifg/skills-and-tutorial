zabbix_agent:
  pkg.installed:
    - name: zabbix22-agent
  file.managed:
    - name: /etc/zabbix_agentd.conf
    - source: salt://zabbix/files/zabbix_agentd.conf
    - template: jinja
    - defaults:
      Server: {{ pillar['Zabbix-agent']['Zabbix_Server'] }}
    - require:
      - pkg: zabbix-agent

  service.running:
    - enable: True
    - watch:
      - pkg: zabbix-agent
      - file: zabbix-agent

