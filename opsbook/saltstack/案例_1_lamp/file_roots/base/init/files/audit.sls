/etc/bashrc:
  file.append:
    - text: export PROMPT_COMMAND = '{msg=$(history 1 |read x)}'
