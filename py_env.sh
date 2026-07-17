PY_VER=3.12
PY=python${PY_VER}
SCRIPT_DIR="$(pwd)"
DEV=""

if [[ "$1" != "init_conda" && "$1" != "init_py" && "$1" != "active" ]] ; then
    echo "Please set param: 'init_py' or 'init_conda' or 'active'"
fi

if [[ "$1" == "init_py" ]] ; then
    deactivate || true
    ${PY} -m venv --clear ${SCRIPT_DIR}/py-env
    source ${SCRIPT_DIR}/py-env/bin/activate
    ${PY} -m pip install --no-cache-dir --upgrade pip
    ${PY} -m pip install --no-cache-dir -r ${SCRIPT_DIR}/requirements.txt
    DEV=""
fi

if [[ "$1" == "init_conda" ]] ; then
    conda deactivate || true
    conda create -y -p ${SCRIPT_DIR}/conda-env python=${PY_VER} poetry
    conda activate ${SCRIPT_DIR}/conda-env
    DEV="--without=dev"
fi


if [[ "$1" == "init_conda" || "$1" == "init_py" ]] ; then
    poetry install --no-cache --directory=${SCRIPT_DIR} ${DEV}
    poetry env info -C ${SCRIPT_DIR}

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
        deactivate || true
        source ${SCRIPT_DIR}/py-env/bin/activate
        poetry env info -C ${SCRIPT_DIR}

        if [ -f "${SCRIPT_DIR}/py_var.sh" ]; then
            source ${SCRIPT_DIR}/py_var.sh
            echo Read env. file.
        fi
    fi

fi
