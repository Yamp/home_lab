source "~/.iterm2_shell_integration.zsh"

PATH="/opt/local/bin:/opt/local/sbin:$PATH"
PATH="/Library/Frameworks/Python.framework/Versions/3.7/bin:$PATH"
PATH="/usr/local/sbin:$PATH"
PATH="$PATH:$HOME/.rvm/bin"
export PATH

[[ -s "$HOME/.rvm/scripts/rvm" ]] && source "$HOME/.rvm/scripts/rvm" # Load RVM into a shell session *as a function*
export ARCHFLAGS=-Wno-error=unused-command-line-argument-hard-error-in-future

export PYENV_ROOT="$HOME/.pyenv"
export PATH="$PYENV_ROOT/bin:$PATH"
export PATH="$HOME/.poetry/bin:$PATH"
export PATH="$HOME/.cargo/bin:$PATH"
