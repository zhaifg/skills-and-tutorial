yum_repo_release:
  pkg.installed:
    - sources:
      - epel-release: http://mirrors.aliyun.com/
      - unless: rpm -qa | grep epel-release-6-8
