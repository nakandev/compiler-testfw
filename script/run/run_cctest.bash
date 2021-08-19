#!/bin/bash

if [ -z $TEST_ROOT ]; then TEST_ROOT=$PWD; fi
if [ -z $TEST_LOGDIR ]; then TEST_LOGDIR=${TEST_ROOT}/log/cctest; fi
if [ -z $TEST_COMPILER ]; then TEST_COMPILER=/usr/bin/clang; fi
if [ -z $TEST_EXECUTER ]; then TEST_EXECUTER=exec_native; fi
TEST_SUITEDIR=${TEST_ROOT}/suite/cctest

# exec suite
if [ -d ${TEST_SUITEDIR} ]; then
  echo cctest start.
  # rm -rf ${TEST_LOGDIR}
  mkdir -p ${TEST_LOGDIR}
  pushd ${TEST_LOGDIR} > /dev/null

  cp ${TEST_SUITEDIR}/make.sh .
  cp ${TEST_SUITEDIR}/Makefile .
  cp ${TEST_SUITEDIR}/runner.sh .
  cp ${TEST_SUITEDIR}/testlist.cfg .
  runsuite(){
    ./runner.sh \
      --suite "${TEST_SUITEDIR}" \
      --work "work" \
      --cc "${TEST_COMPILER}" \
      --exec "${TEST_EXECUTER}" \
      --cflags "${TEST_CFLAGS}" \
      --testlist testlist.cfg \
      > test.log 2> result.txt
  }
  (time runsuite) 2> time.log
  echo cctest end.
fi

