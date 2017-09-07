# append

export HISTFILE=$HOME/.bash_history
export HISTSIZE=1200
export HISTFILESIZE=1200
export HISTCONTROL=ignoredups
export HISTTIMEFORMAT="`whoami` %F %T "

export PROMPT_COMMAND="history -a; history -c; history -r;"'.../OMAudit_agent.py $(history 1)'
shopt -s histappend # 将历史清单将添加形式加入到HISTFILE 变量指定的文件, 而不是覆盖
typeset -r PROMPT_COMMAND
typeset -r HISTTIMEFORMAT


export PROMPT_COMMAND="history -a; history -c; history -r;"'/root/audit.py $(history 1)'
export PROMPT_COMMAND="history -a; history -c; history -r;"' echo "${SSH_CLIENT:=Local}  ${SSH_TTY:=Linux} $(history 1)" >> /var/log/bash_history'



export PROMPT_COMMAND='{ date "+[ %Y%m%d %H:%M:%S `whoami` ] `history 1 | { read x cmd; echo "$cmd from ip:$SSH_CLIENT   $SSH_TTY"; }`"; }&gt;&gt; /home/pu/login.log'

export PROMPT_COMMAND='{ `history 1` | { read hid user date time  cmd; echo "$hid $user $date $time $cmd from ip:$SSH_CLIENT  $SSH_TTY"; }`"; }'

"{ history 1 | { read hid user date time  cmd ; echo \"$hid $user $date $time $cmd from ip:${SSH_CLIENT:=Local}  ${SSH_TTY:=Linux}\"; }; } &gt;&gt; /tmp/bash_history"
