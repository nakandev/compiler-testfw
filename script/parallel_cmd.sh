#!/bin/bash
# https://www.it-swarm-ja.com/ja/shell-script/bash-forループを並列化する/960741948/

task(){
  r=$(($RANDOM % 3))
  echo "$1"; sleep $((3+$r));
}

# initialize a semaphore with a given number of tokens
open_sem(){
    mkfifo pipe-$$
    exec 3<>pipe-$$
    rm pipe-$$
    local i=$1
    for((;i>0;i--)); do
        printf %s 000 >&3
    done
}

# run the given command asynchronously and pop/Push tokens
run_with_lock(){
    local x
    # this read waits until there is something to read
    read -u 3 -n 3 x && ((0==x)) || exit $x
    (
     ( "$@"; )
    # Push the return code of the command to the semaphore
    printf '%.3d' $? >&3
    )&
}

N=4
open_sem $N
for thing in {1..60}; do
    run_with_lock task $thing
done

wait
