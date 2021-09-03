import os
from collections import OrderedDict

# [cover]
title = 'Compiler Report'
author = 'nakandev'

# [target]
sdk = "./target/clang-8/build/bin"
compiler = "/usr/bin/clang"
executer = "executer"

# [suite]
suite = OrderedDict([
    # ("cctest", "cctest"),
    ("llvm", "llvm-testsuite"),
])

# [option]
cflags = OrderedDict([
    ("OX", "   "),
    ("O0", "-O0"),
    ("O1", "-O1"),
    ("O2", "-O2"),
    ("O3", "-O3"),
    ("g_OX", "-g    "),
    ("g_O0", "-g -O0"),
    ("g_O1", "-g -O1"),
    ("g_O2", "-g -O2"),
    ("g_O3", "-g -O3"),
])
cc_cflags = ""
cc_ldflags = ""

# [run]
para = 3
optkeys = ('compiler', 'suite', 'cflags')
logroot = os.getcwd() + "/log"
reportroot = os.getcwd() + "/report"
logdir = '{target.suite}/{target.cflags}'
reportdir = '{target.suite}'
runcmd_prefix = ''
runscript = OrderedDict([
    ("cctest", runcmd_prefix + "script/run/run_cctest.bash"),
    ("llvm", runcmd_prefix + "script/run/run_llvm-testsuite_lnt_make.bash"),
])
