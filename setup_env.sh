#!/bin/bash

TEST_ROOT=$PWD

cd $TEST_ROOT

# 1. llvm-testsuite
# 1.1. python virtual env
if [ -d ./env/py3 ]; then
  echo python venv already exists.
else
  echo python venv build start.
  python3 -m venv ./env/py3

  if [ ! -f ./env/py3/bin/python ]; then
    echo Error: not found ./env/py3/bin/python
    rm -rf ./env/py3
    exit 1
  fi
  if [ ! -f ./env/py3/bin/pip ]; then
    echo Error: not found ./env/py3/bin/pip
    rm -rf ./env/py3
    exit 1
  fi
  if [ ! -f ./env/py3/bin/activate ]; then
    echo Error: not found ./env/py3/bin/activate
    rm -rf ./env/py3
    exit 1
  fi

  echo python venv build end.
fi
source ./env/py3/bin/activate

# 1.2. lnt
which lnt > /dev/null
if [ $? -eq 0 ]; then
  echo lnt already installed.
else
  echo lnt install start.
  sudo apt install bison tcl -y
  git clone https://github.com/llvm/llvm-lnt.git ./env/lnt
  python ./env/lnt/setup.py develop
  pushd ./env/py3/bin > /dev/null
  ln -s lit llvm-lit
  popd > /dev/null

  which lnt > /dev/null
  if [ $? -ne 0 ]; then
    echo Error: lnt not found
    exit 1
  fi

  echo lnt install end.
fi

# 1.3. lit
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

# 1.4. testsuite
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

