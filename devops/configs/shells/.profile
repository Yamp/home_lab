#!/usr/bin/env bash

export HOMEBREW_NO_ANALYTICS=1
export PYENV_ROOT="$HOME/.pyenv"
export ARCHFLAGS=-Wno-error=unused-command-line-argument-hard-error-in-future

PATH=$HOME/bin:/usr/local/bin:$PATH
PATH="$PATH:/opt/local/sbin" #macports
PATH="/opt/local/bin:/opt/local/sbin:$PATH"
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
PATH="$HOME/.poetry/bin:$PATH"
PATH="$HOME/.cargo/bin:$PATH"
PATH="/Users/dimitrius/.nimble/bin:$PATH"  # nim
PATH=$PATH:~/homebrew/sbin:~/homebrew/bin
PATH="/usr/local/opt/sqlite/bin:$PATH"
PATH="/usr/local/opt/qt/bin:$PATH"
PATH="$PYENV_ROOT/bin:$PATH"
PATH="$PATH:/Users/dimitrius/.composer/vendor/bin"  # composer (PHP packages)
export PATH

eval "$(pyenv init -)"
