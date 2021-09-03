#!/usr/bin/env python

from __future__ import absolute_import, print_function, unicode_literals
import argparse
import errno
import os
import subprocess
from collections import OrderedDict
from contextlib import closing
from multiprocessing import Pool
from config import Config


def run_all(args, config):
    runargs = []
    for option in config.param_products(config.optkeys, restrictions=args):
        optiond = OrderedDict(zip(config.optkeys, option))
        runargs.append([config, optiond])
    para = config.para if hasattr(config, 'para') else 2
    with closing(Pool(processes=para)) as pool:
        pool.map(func=run_single, iterable=runargs)
        pool.terminate()


def run_single(args):
    config, optiond = args
    print('Start: %s' % optiond)
    runner = CompilerTestRunner(config, optiond)
    runner.set_osenv()
    runner.run_script()


class CompilerTestRunner:
    def __init__(self, config, option):
        self.config = config
        self.config._target = self
        self.root = option.get('root')
        self.suite = option.get('suite')
        self.testcase = option.get('testcase')
        self.compiler = option.get('compiler')
        self.executer = option.get('executer')
        self.cflags = option.get('cflags')
        self.ldflags = option.get('ldflags')
        self.cc_cflags = option.get('cc_cflags')
        self.cc_ldflags = option.get('cc_ldflags')
        self.logroot = option.get('logroot')
        self.logdir = option.get('logdir')

    def set_osenv(self):
        cfg = self.config
        os.environ['TEST_ROOT'] = os.getcwd()
        os.environ['TEST_LOGDIR'] = os.path.join(cfg.logroot, cfg.logdir)
        os.environ['TEST_COMPILER'] = cfg.compiler
        os.environ['TEST_EXECUTER'] = cfg.executer
        os.environ['TEST_CFLAGS'] = cfg.cflags[self.cflags]
        try:
            os.makedirs(os.environ['TEST_LOGDIR'])
        except Exception:
            pass
        logfile = os.path.join(os.environ['TEST_LOGDIR'], 'osenv.log')
        with open(logfile, 'w') as f:
            for key in os.environ:
                if key[:5] == 'TEST_':
                    print("'%s': '%s'" % (key, os.environ[key]), file=f)

    def run_script(self):
        cfg = self.config
        script = cfg.runscript[self.suite]
        if not os.path.exists(script):
            raise OSError(errno.EEXIST, 'File not found', script)
        proc = subprocess.Popen(
            script,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            shell=True,
        )
        outs, errs = proc.communicate()
        logdir = os.environ['TEST_LOGDIR']
        with open('%s/%s' % (logdir, 'run_script.log'), 'w') as f:
            f.write(str(outs))


def main():
    parser = argparse.ArgumentParser(description='TestSuite Runner.')
    parser.add_argument('--config', help='Test target Config file', default=None)
    parser.add_argument('--suite', help='Test Suite', default=None)
    parser.add_argument('--testcase', help='Testcase', default=None)
    parser.add_argument('--compiler', help='Test Compiler', default=None)
    parser.add_argument('--executer', help='Test Executer', default=None)
    parser.add_argument('--cflags', help='Test CFLAGS', default=None)
    parser.add_argument('--logroot', help='Log directory', default=None)
    parser.add_argument('--logdir', help='Log directory', default=None)
    args = parser.parse_args()
    if args.config is None or not os.path.exists(args.config):
        raise Exception('Config file not exists: %s' % args.config)

    config = Config()
    config.load(args.config)
    run_all(args, config)


if __name__ == '__main__':
    main()
