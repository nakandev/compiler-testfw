#!/bin/bash

TEST_ROOT=$PWD

cd $TEST_ROOT

# 0. run/report script
# 0.1. python virtual env
if [ -d ./env/py ]; then
  echo python venv already exists.
else
  echo python venv build start.
  python3 -m venv ./env/py

  if [ ! -f ./env/py/bin/python ]; then
    echo Error: not found ./env/py/bin/python
    rm -rf ./env/py
    exit 1
  fi
  if [ ! -f ./env/py/bin/pip ]; then
    echo Error: not found ./env/py/bin/pip
    rm -rf ./env/py
    exit 1
  fi
  if [ ! -f ./env/py/bin/activate ]; then
    echo Error: not found ./env/py/bin/activate
    rm -rf ./env/py
    exit 1
  fi

  echo python venv build end.
fi
source ./env/py/bin/activate

# 0.2. python packages
python -c "import openpyxl" 2> /dev/null
if [ $? -eq 0 ]; then
  echo openpyxl aleady installed.
else
  echo python packages install start.
  pip install openpyxl
  echo python packages install end.
fi

# 1. llvm-testsuite
# 1.1. testsuite
if [ -d ./suite/llvm-testsuite ]; then
  echo ./suite/llvm-testsuite already exists.
else
  echo llvm-testsuite install start.
  pushd ./suite > /dev/null
  # tar xf test-suite-11.0.0.src.tar.xz
  # mv tar suite/test-suite-11.0.0.src llvm-testsuite
  git clone -b llvmorg-12.0.0 https://github.com/llvm/llvm-test-suite llvm-testsuite
  popd > /dev/null
  echo llvm-testsuite install end.
fi

# 1.2. python virtual env
if [ -d ./suite/llvm-testsuite/env ]; then
  echo python venv already exists.
else
  echo python venv build start.
  python3 -m venv ./suite/llvm-testsuite/env

  if [ ! -f ./suite/llvm-testsuite/env/bin/python ]; then
    echo Error: not found ./suite/llvm-testsuite/env/bin/python
    rm -rf ./suite/llvm-testsuite/env
    exit 1
  fi
  if [ ! -f ./suite/llvm-testsuite/env/bin/pip ]; then
    echo Error: not found ./suite/llvm-testsuite/env/bin/pip
    rm -rf ./suite/llvm-testsuite/env
    exit 1
  fi
  if [ ! -f ./suite/llvm-testsuite/env/bin/activate ]; then
    echo Error: not found ./suite/llvm-testsuite/env/bin/activate
    rm -rf ./suite/llvm-testsuite/env
    exit 1
  fi

  echo python venv build end.
fi
source ./suite/llvm-testsuite/env/bin/activate

# 1.3. lnt
which lnt > /dev/null
if [ $? -eq 0 ]; then
  echo lnt already installed.
else
  echo lnt install start.
  sudo apt install bison tcl -y
  git clone https://github.com/llvm/llvm-lnt.git ./suite/llvm-testsuite/env/lnt
  python ./suite/llvm-testsuite/env/lnt/setup.py develop
  pushd ./suite/llvm-testsuite/env/bin > /dev/null
  ln -s lit llvm-lit
  popd > /dev/null

  which lnt > /dev/null
  if [ $? -ne 0 ]; then
    echo Error: lnt not found
    exit 1
  fi

  echo lnt install end.
fi

# 1.4. lit
which lit > /dev/null
if [ $? -eq 0 ]; then
  echo lit already installed.
else
  echo lit install start.
  pip install svn+https://llvm.org/svn/llvm-project/llvm/trunk/utils/lit

  which lit > /dev/null
  if [ $? -ne 0 ]; then
    echo Error: lit not found
    exit 1
  fi

  echo lit install end.
fi

