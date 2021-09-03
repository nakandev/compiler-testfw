#!/bin/bash

if [ -z $TEST_ROOT ]; then TEST_ROOT=$PWD; fi
if [ -z $TEST_LOGDIR ]; then TEST_LOGDIR=${TEST_ROOT}/log/llvm-testsuite; fi
if [ -z $TEST_COMPILER ]; then TEST_COMPILER=/usr/bin/clang; fi
if [ -z $TEST_EXECUTER ]; then TEST_EXECUTER=exec_native; fi
TEST_SUITEDIR=${TEST_ROOT}/suite/llvm-testsuite

# activate env
if [ ! -f ./env/py3/bin/activate ]; then
  echo Error: not found ./env/py3/bin/activate
  rm -rf ./env/py3
  exit 1
fi
source ./env/py3/bin/activate

# exec llvm-testsuite
if [ -d ${TEST_SUITEDIR} ]; then
  echo llvm-testsuite start.
  rm -rf ${TEST_LOGDIR}
  mkdir -p ${TEST_LOGDIR}
  pushd ${TEST_LOGDIR} > /dev/null
  cmake \
    -DCMAKE_C_COMPILER="${TEST_COMPILER}" \
    -DCMAKE_CFLAGS="${TEST_CFLAGS}" \
    -DCMAKE_EXE_LINKER_FLAGS="-no-pie" \
    -C${TEST_SUITEDIR}/cmake/caches/O3.cmake \
    ${TEST_SUITEDIR}
  make
  lit -v -j 1 -o results.json .
  popd > /dev/null
  echo llvm-testsuite end.
fi

