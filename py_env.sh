PY_VER=3.12
SCRIPT_DIR="$(pwd)"

_abort_with_error() {
    if [ -t 0 ]; then
        echo ""
        read -p "Premi Invio per continuare..." _dummy 2>/dev/null || true
    fi
    if [[ "${BASH_SOURCE[0]}" != "${0}" ]]; then
        return 1
    else
        exit 1
    fi
}

if [[ "$1" != "init_conda" && "$1" != "init_py" && "$1" != "active" ]] ; then
    echo "Please set param: 'init_py' or 'init_conda' or 'active'"
    _abort_with_error
fi

if [[ "$1" == "init_py" || "$1" == "init_conda" ]] ; then
    if ! command -v uv >/dev/null 2>&1; then
        echo "❌ 'uv' non è installato sul sistema."
        echo "   Per favore installa uv (es. 'brew install uv' o 'curl -LsSf https://astral.sh/uv/install.sh') prima di proseguire."
        _abort_with_error
    fi
fi

if [[ "$1" == "init_py" ]] ; then
    type deactivate >/dev/null 2>&1 && deactivate || true
    unset VIRTUAL_ENV
    PATH=$(echo "$PATH" | tr ':' '\n' | grep -v 'py-env' | tr '\n' ':' | sed 's/:$//')
    export PATH

    uv venv ${SCRIPT_DIR}/py-env --python ${PY_VER} --clear || _abort_with_error
    source ${SCRIPT_DIR}/py-env/bin/activate
fi

if [[ "$1" == "init_conda" ]] ; then
    type deactivate >/dev/null 2>&1 && deactivate || true
    conda create -y -p ${SCRIPT_DIR}/conda-env python=${PY_VER} || _abort_with_error
    conda activate ${SCRIPT_DIR}/conda-env
fi

if [[ "$1" == "init_conda" || "$1" == "init_py" ]] ; then
    uv sync --active --directory ${SCRIPT_DIR} || _abort_with_error

    if [ -f "${SCRIPT_DIR}/py_var.sh" ]; then
       source ${SCRIPT_DIR}/py_var.sh
       echo Read env. file.
    fi
fi

if [[ "$1" == "active" ]] ; then

    if [ -d "${SCRIPT_DIR}/conda-env" ]; then
        echo Conda Activated...
        conda deactivate || true
        conda activate ${SCRIPT_DIR}/conda-env
    fi

    if [ -d "${SCRIPT_DIR}/py-env" ]; then
        type deactivate >/dev/null 2>&1 && deactivate || true
        source ${SCRIPT_DIR}/py-env/bin/activate

        if [ -f "${SCRIPT_DIR}/py_var.sh" ]; then
            source ${SCRIPT_DIR}/py_var.sh
            echo Read env. file.
        fi
    fi

fi
