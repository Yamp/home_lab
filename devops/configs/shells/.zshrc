#!/usr/bin/env bash
set -o noclobber  # do not owerwrite existing files with >
set -o nocaseglob  # Case insensitive globs
set -o globdots    # Wildcards match dotfiles ("*.sh" => ".foo.sh")

# global variables
export ZSH="/Users/dimitrius/.oh-my-zsh"
export ZSH_CACHE_DIR="$ZSH/cache"
export HISTFILE=~/.histfile
export HISTFILESIZE=100000
export HISTSIZE=100000
export SAVEHIST=100000
export WORKON_HOME=$HOME/.virtualenvs
export MACOSX_DEPLOYMENT_TARGET=10.15
export OSX_VERSION=10.15
export SDKROOT=/Applications/Xcode.app/Contents/Developer/Platforms/MacOSX.platform/Developer/SDKs/MacOSX10.15.sdk

export OPENBLAS_NUM_THREADS=12
export VECLIB_MAXIMUM_THREADS=12
export MKL_NUM_THREADS=12
export CFLAGS='-Ofast -march=native'

export LANG=ru_RU.UTF-8
export LC_ALL=ru_RU.UTF-8

#export ARCHFLAGS="-arch x86_64"  # compilation (ruby?)
export SSH_KEY_PATH="~/.ssh/id_rsa"
export MANPATH="/usr/local/man:$MANPATH"
export MSF_DATABASE_CONFIG=/Users/dimitrius/.msf4/database.yml  # DB for metasploit
export HOMEBREW_CASK_OPTS=--require-sha
export HOMEBREW_NO_INSECURE_REDIRECT=1
export PAGER=/usr/local/bin/eless
export EDITOR='subl -w'
export CDPATH=.:~:..
export PYTHON=/usr/local/bin/python
export LD_LIBRARY_PATH=/opt/intel/mkl/lib:${LD_LIBRARY_PATH}:/usr/local/lib/:/opt/local/lib:/usr/lib
export LIBRARY_PATH=$LIBRARY_PATH:/usr/local/opt/openssl/lib/
export TERM="xterm-256color"
export GDAL_DATA="/usr/local/Cellar/gdal/2.4.2_2/share/gdal/"

#export PYTHONUNBUFFERED=1

export ANSIBLE_NOCOWS=1

export FZF_DEFAULT_COMMAND='fd --type file --follow --hidden --exclude .git'
export FZF_CTRL_T_COMMAND="$FZF_DEFAULT_COMMAND"

# export CC=icc  # inter compiler everywhere, hope this is not an error
# export LD=xild
# export AR=xiar
# export CXX=icpc
# sudo -H -E CC=icc FC=ifort CXX=icpc CFLAGS='-O3 -xHost -ipo -no-prec-div' LD=xild AR=xiar
# export INTEL_FLAGS = "-no-prec-sqrt -xHost -no-prec-div -no-inline-max-size -no-inline-max-total-size -ip -IPF-fltacc -IPF-fma -IPF-fp-relaxed -IPF-fp-speculation=fast"

# zsh theme
ZSH_THEME="powerlevel10k/powerlevel10k"
DEFAULT_USER="dimitrius" #To not show dimitrius when possible

POWERLEVEL9K_MODE='nerdfont-complete'
POWERLEVEL9K_DIR_HOME_FOREGROUND="white"
POWERLEVEL9K_DIR_HOME_SUBFOLDER_FOREGROUND="white"
POWERLEVEL9K_DIR_DEFAULT_FOREGROUND="white"

POWERLEVEL9K_PROMPT_ON_NEWLINE=true
POWERLEVEL9K_SHORTEN_DIR_LENGTH=2
POWERLEVEL9K_SHORTEN_STRATEGY="trancate_left"

POWERLEVEL9K_VIRTUALENV_BACKGROUND="006"
POWERLEVEL9K_VCS_SHORTEN_LENGTH=5
POWERLEVEL9K_LEFT_PROMPT_ELEMENTS=(context dir ssh aws virtualenv vcs)
POWERLEVEL9K_RIGHT_PROMPT_ELEMENTS=(dir_writable root_indicator background_jobs time)
POWERLEVEL9K_TIME_FORMAT="%D{%H:%M:%S %d}"

POWERLEVEL9K_VCS_GIT_HOOKS=(vcs-detect-changes git-untracked git-aheadbehind git-stash git-remotebranch git-tagname)
POWERLEVEL9K_HIDE_BRANCH_ICON=true
POWERLEVEL9K_VCS_SHORTEN_LENGTH=5
POWERLEVEL9K_VCS_SHORTEN_STRATEGY="truncate_middle"
POWERLEVEL9K_SHOW_CHANGESET=false
POWERLEVEL9K_CHANGESET_HASH_LENGTH=6

# zsh settings
ZSH_HIGHLIGHT_HIGHLIGHTERS=(main brackets pattern line)
ZSH_AUTOSUGGEST_USE_ASYNC=true


#plugins
plugins=(
  git
  dotenv
  osx
  zsh-autosuggestions
  aws
  django
  colored-man-pages
  colorize
  npm
  git-flow
  pip
  poetry
  python
  dircycle
  dirhistory
  sudo
  wd
  virtualenv
  virtualenvwrapper
  copydir
  web-search
  docker
  autojump
  zsh-navigation-tools
  zsh-interactive-cd
  history-substring-search
  zsh-completions
  zsh-apple-touchbar
  zsh-syntax-highlighting
  auto-notify
  autoupdate
  tmux
)

fpath+=~/.zfunc  # poetry completions
export fpath

autoload -U compinit && compinit

source $ZSH/oh-my-zsh.sh

# plugin vars
export HISTORY_SUBSTRING_SEARCH_ENSURE_UNIQUE=true
export HISTORY_SUBSTRING_SEARCH_FUZZY=true
setopt HIST_IGNORE_ALL_DUPS  # all
setopt HIST_FIND_NO_DUPS  # just ajasten
setopt EXTENDED_HISTORY
setopt histreduceblanks  # blank lines not in hist
setopt histignorespace
setopt histignorealldups
setopt autocd
setopt extendedglob # more glob funcs
setopt globdots # Do not require a leading '.' in a filename to be matched explicitly
setopt listpacked
# # setopt correct
setopt alwaystoend
setopt no_nomatch

function finish { jobs -p | xargs kill }
trap finish EXIT

genpasswd() {pwgen $1 1 |pbcopy |pbpaste; echo “Has been copied to clipboard”}

cdf() {
    target=`osascript -e 'tell application "Finder" to if (count of Finder windows) > 0 then get POSIX path of (target of front Finder window as text)'`
    if [ "$target" != "" ]; then
        cd "$target"; pwd
    else
        echo 'No Finder window found' >&2
    fi
}

pman () {
    man -t "${1}" | open -f -a /Applications/Preview.app
}

# Aliases (recommended to define within ZSH_CUSTOM)
alias py2="python2 -m bpython"
alias py3="python3 -m bpython"
alias py=py3
alias del="rmtrash"
alias la='exa -lahmHF@ --git'
function cs () {cd "$@" && ls}
alias cds=cs
alias mkcd='foo(){ mkdir -p "$1"; cd "$1" }; foo '
alias myip="curl http://ipecho.net/plain; echo"  # print my ip
alias mc="mc --nosubshell"  # fast midnight commander start and work
alias locate="glocate -br"
alias setdns="networksetup -setdnsservers Wi-Fi"
alias update-all-git="find . -name ".git" -type d | xargs -P10 -I{} git --git-dir={} upull"
alias dex="docker exec -it"
alias rgrep="rg --files | grep "
alias poetry_shell='. "$(dirname $(poetry run which python))/activate"'

alias update_mac_cli='sh -c "$(curl -fsSL https://raw.githubusercontent.com/guarinogabriel/mac-cli/master/mac-cli/tools/update)"'

function swap()
{
    local TMPFILE=tmp.$$
    sudo mv "$1" $TMPFILE && sudo mv "$2" "$1" && sudo mv $TMPFILE "$2"
}

alias swap='swap'
alias swap_hosts='swap /etc/hosts /etc/hosts.bak && la /etc/hosts /etc/hosts.bak'


function tsh { ssh -Y -C $1 -t "tmux -CC attach -t $2 || tmux -CC new -s $2"; }
function vsh { ssh -L 5901:127.0.0.1:5901 -C -N $1; }

function upull() {
  echo "Updating git repo at $(pwd)"
  git add . >>/dev/null 2>&1

  if output=$(git status --porcelain) && [[ -z "$output" ]]; then
      echo "No local changes, pulling..."
      git pull >>/dev/null 2>&1 # workdir is clean
  else
      echo "Using stash for updating"
      git stash >>/dev/null 2>&1 && git pull >>/dev/null 2>&1
      git stash pop
  fi
}

function upush() {
  upull

  if [[ -z $1 ]]; then
    git commit -a
  else
    git commit -a -m $1
  fi

  git push
}

PATH="/Users/dimitrius/.nimble/bin:$PATH"  # nim
PATH=$HOME/bin:/usr/local/bin:$PATH
PATH="$PATH:/opt/local/sbin" #macports
PATH="/usr/local/sbin:$PATH"
PATH="$PATH:/opt/local/bin"
PATH="~/scripts:$PATH"
PATH="/usr/local/opt/dart@2/bin:$PATH"
PATH="$PATH:/Users/dimitrius/.local"
PATH="$PATH:/opt/metasploit-framework/bin"
PATH="/usr/local/sbin:$PATH"
PATH="/usr/local/opt/curl-openssl/bin:$PATH"
PATH="/usr/local/opt/openssl@1.1/bin:$PATH"
PATH="/usr/local/opt/tcl-tk/bin:$PATH"
# PATH="/usr/local/opt/llvm/bin:$PATH" # llvm
PATH="$PATH:/Applications/CPLEX_Studio_Community129/cplex/bin/x86-64_osx/"  # cplex
PATH="$PATH:/Users/dimitrius/bin/mosek/8/tools/platform/osx64x86/bin" # MOSEK
PATH="$PATH:/Users/dimitrius/Library/Python/3.7/bin"  # for now just for line_profiler
PATH="$PATH:~/.cabal/bin"
PATH=$PATH:~/homebrew/sbin:~/homebrew/bin
PATH="/usr/local/opt/sqlite/bin:$PATH"
PATH="/usr/local/opt/qt/bin:$PATH"
PATH="$PYENV_ROOT/bin:$PATH"
PATH="$PATH:/Users/dimitrius/.composer/vendor/bin"  # composer (PHP packages)
export PATH

[[ -f ~/.p10k.zsh ]] && source ~/.p10k.zsh

if command -v pyenv 1>/dev/null 2>&1; then eval "$(pyenv init -)"; fi
# eval "$(thefuck --alias  --enable-experimental-instant-mode)"
[ -f /usr/local/etc/profile.d/autojump.sh ] && . /usr/local/etc/profile.d/autojump.sh  # autojump init
if brew command command-not-found-init > /dev/null 2>&1; then eval "$(brew command-not-found-init)"; fi
#should be in the end!
source ~/.iterm2_shell_integration.zsh

# export NVM_DIR="$HOME/.nvm"
# [ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"  # This loads nvm
# [ -s "$NVM_DIR/bash_completion" ] && \. "$NVM_DIR/bash_completion"  # This loads nvm bash_completion

# eval "$(pipenv --completion)"
# eval "$(rbenv init -)"
