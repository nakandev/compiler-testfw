import os
import itertools
from collections import OrderedDict

# [target]
project = 'CC-X.X'
sdk = "./target/clang-8/build/bin"
compiler = OrderedDict([
    ("gcc", "/usr/bin/gcc"),
    ("clang", "/usr/bin/clang"),
])
executer = OrderedDict([
    ("native", "exec_native"),
])

# [suite]
suite = OrderedDict([
    ("cctest", "cctest"),
    ("llvm", "llvm-testsuite"),
])

# [option]
cflags = OrderedDict([
    ("OX", "   "),
    ("O0", "-O0"),
    # ("O1", "-O1"),
    # ("O2", "-O2"),
    # ("O3", "-O3"),
    # ("g_OX", "-g    "),
    # ("g_O0", "-g -O0"),
    # ("g_O1", "-g -O1"),
    # ("g_O2", "-g -O2"),
    # ("g_O3", "-g -O3"),
])
cc_cflags = ""
cc_ldflags = ""

suite_sp_var = {
    'llvm': {
        'makeparam': 'DISABLE_DIFFS=1'
    }
}

# [run]
para = 3
optkeys = ('compiler', 'executer', 'suite', 'cflags')
optvalues = list(itertools.product(*[locals()[k] for k in optkeys]))
logroot = os.getcwd() + "/log/log_" + project
logdir = '{target.suite}/{target.cflags}'  # must be started with {target.suite}
runcmd_prefix = ''
runscript = OrderedDict([
    ("cctest", runcmd_prefix + "script/run/run_cctest.bash"),
    ("llvm", runcmd_prefix + "script/run/run_llvm-testsuite_lnt_make.bash"),
])

# [report]
refroot = os.getcwd() + "/ref"
reffile = 'ref-sample.csv'
reportroot = os.getcwd() + "/report/report_" + project
reportdir = '{target.suite}'  # must be started with {target.suite}
reportfile = project + '_{target.config.value_suite}_Report'
report_template_xlsx = os.getcwd() + '/conf/report_template.xlsx'
report_cover = {
    'title': project + ' {target.config.value_suite} Report',
    'company': 'ABC Company',
    'group': 'DEF Group',
    'author': 'Name NAME',
}
