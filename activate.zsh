export UENV_CMD=/home/bcumming/software/test/cli/uenv-impl
export VERSION=0.1-dev

function usage {
    echo "uenv - for using user environments [version ${VERSION}]"
    echo ""
    echo "Usage:   uenv [--version] [--help] <command> [<args>]"
    echo ""
    echo "the following commands are available"
    echo "  start      start a new shell with an environment loaded"
}

script_file="${(%):-%x}"
script_dir="$( cd "$( dirname "${(%):-%x}" )" && pwd )"
export UENV_ACTIVATE_SCRIPT="$script_dir/$script_file"

function uenv {
    if [ "$1" = "--version" ]; then
        echo "uenv version ${VERSION}";
    elif [[ $# -eq 0 || "$1" = "--help" ]]; then
        usage;
    else
        eval $($UENV_CMD "$@")
    fi
}
