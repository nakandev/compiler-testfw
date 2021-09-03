#!/bin/bash

if [ -z "$TEST_ROOT" ]; then TEST_ROOT=$PWD; fi
if [ -z "$TEST_LOGDIR" ]; then TEST_LOGDIR=${TEST_ROOT}/log/llvm-testsuite; fi
if [ -z "$TEST_COMPILER" ]; then TEST_COMPILER=/usr/bin/clang; fi
if [ -z "$TEST_EXECUTER" ]; then TEST_EXECUTER=exec_native; fi
TEST_SUITEDIR=${TEST_ROOT}/suite/llvm-testsuite

if [ ! -z "$TEST_TESTCASE" ]; then
  TEST_TESTCASE_ARGS="--only-test $TEST_TESTCASE"
fi

# activate env
if [ ! -f ./suite/llvm-testsuite/env/bin/activate ]; then
  echo Error: not found ./suite/llvm-testsuite/env/bin/activate
  exit 1
fi
source ./suite/llvm-testsuite/env/bin/activate

# exec llvm-testsuite
if [ -d ${TEST_SUITEDIR} ]; then
  echo llvm-testsuite start.
  # rm -rf ${TEST_LOGDIR}
  mkdir -p ${TEST_LOGDIR}
  pushd ${TEST_LOGDIR} > /dev/null
  lnt runtest nt \
    --no-timestamp \
    --test-suite "${TEST_SUITEDIR}" \
    --sandbox "$PWD" \
    --cc "${TEST_COMPILER}" \
    --cxx "${TEST_COMPILER}" \
    --cflags "${TEST_CFLAGS} -no-pie" \
    "${TEST_TESTCASE_ARGS}"
  popd > /dev/null
  echo llvm-testsuite end.
fi

