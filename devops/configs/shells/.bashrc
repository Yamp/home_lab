#!/usr/bin/env bash

export HISTSIZE=100000
export HISTFILESIZE=100000
export HISTCONTROL=ignoredups

[[ -f ~/.fzf.bash ]] && source ~/.fzf.bash

export LC_ALL=en_US.UTF-8
export LANG=en_US.UTF-8
if [[ -f $(brew --prefix)/etc/bash_completion ]]; then source $(brew --prefix)/etc/bash_completion; fi
source /Users/dimitrius/.ghcup/env
if [ -f $(brew --prefix)/etc/bash_completion ]; then source $(brew --prefix)/etc/bash_completion; fi
eval "$(pyenv init -)"
