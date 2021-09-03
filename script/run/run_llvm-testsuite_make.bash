#!/bin/bash

if [ -z "$TEST_ROOT" ]; then TEST_ROOT=$PWD; fi
if [ -z "$TEST_LOGDIR" ]; then TEST_LOGDIR=${TEST_ROOT}/log/llvm-testsuite; fi
if [ -z "$TEST_COMPILER" ]; then TEST_COMPILER=/usr/bin/clang; fi
if [ -z "$TEST_EXECUTER" ]; then TEST_EXECUTER=exec_native; fi
TEST_SUITEDIR=${TEST_ROOT}/suite/llvm-testsuite

if [ ! -z "$TEST_TESTCASE" ]; then
  TEST_TESTCASE_ARGS="-C $TEST_TESTCASE"
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
  rm -rf ${TEST_LOGDIR}
  mkdir -p ${TEST_LOGDIR}
  pushd ${TEST_LOGDIR} > /dev/null

  ${TEST_SUITEDIR}/configure \
    --without-llvmsrc \
    --without-llvmobj \
  > configure.log 2>&1
  make -k \
    TARGET_LLVMGCC="${TEST_COMPILER}" \
    TARGET_LLVMGXX="${TEST_COMPILER}" \
    CFLAGS="${TEST_CFLAGS}" \
    ENABLE_OPTIMIZED=1 \
    DISABLE_JIT=1 \
    TEST=simple \
    "${TEST_TESTCASE_ARGS}"
  > test.log 2>&1
    # USE_PREFERENCE_OUTPUT=1 \
  make \
    TEST=simple \
    report.csv \
  >> test.log 2>&1

  popd > /dev/null
  echo llvm-testsuite end.
fi

