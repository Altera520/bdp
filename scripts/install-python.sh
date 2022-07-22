#!/bin/bash

source '/tmp/env.sh'

function install_python 
{
    local PYTHON_VER=$1
    echo "install python ${PYTHON_VER}"

    # install python
    dnf install -y gcc \
                   openssl-devel \
                   bzip2-devel \
                   libffi-devel \
                   zlib-devel
    wget "https://www.python.org/ftp/python/${PYTHON_VER}/Python-${PYTHON_VER}.tar.xz"
    tar -xf "Python-${PYTHON_VER}.tar.xz"

    # compile and build
    pushd .
    cd "Python-${PYTHON_VER}"
    ./configure --enable-optimizations
    make -j 2
    nproc
    make altinstall
    popd

    rm "Python-${PYTHON_VER}.tar.xz"
    echo 'y' | rm -r "Python-${PYTHON_VER}"

    # install python pip and devel
    dnf install -y python3-pip \
                   python3-devel

    # pythonX -> python, pipX -> pip
    local -r PYTHON_MAJOR_VER="$(echo $PYTHON_VER | cut -d '.' -f1,2)"
    ln -s "/usr/local/bin/python${PYTHON_MAJOR_VER}" /usr/bin/python
    ln -s "/usr/local/bin/pip${PYTHON_MAJOR_VER}" /usr/bin/pip

    # upgrade latest pip version
    python -m pip install --upgrade pip

    # virtualenv and autoenv install
    pip install virtualenv \
                autoenv
    # autoenv run all user
    echo 'source /usr/local/bin/activate.sh' > /etc/profile.d/autoenv.sh
}

install_python $PYTHON_VER