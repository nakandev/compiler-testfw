#!/usr/bin/env python

from __future__ import absolute_import, print_function, unicode_literals
import argparse
import getpass
import os
import platform
import signal
import subprocess
from collections import OrderedDict
from config import Config
from contextlib import closing
from multiprocessing import Pool


def raise_exception(signum, frame):
    raise Exception('Catched SIGINT on PID:{}'.format(os.getpid()))


def run_all(args, config):
    runargs = []
    for option in config.options(args):
        optiond = OrderedDict(zip(config.optkeys, option))
        runargs.append([config, optiond])
    para = config.para if hasattr(config, 'para') else 2
    signal.signal(signal.SIGINT, raise_exception)  # set to all process
    with closing(Pool(processes=para)) as pool:
        try:
            pool.map(func=run_single, iterable=runargs)
        except Exception:
            pool.terminate()
            pool.join()
            os.killpg(os.getpid(), signal.SIGTERM)
        else:
            pool.close()
            pool.join()


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

    def get_envinfo(self):
        keys = ('system', 'node', 'release', 'version', 'machine', 'processor')
        info = {}
        info['Host'] = OrderedDict(zip(keys, platform.uname()))
        try:
            info['Host']['user'] = getpass.getuser()
        except Exception:
            info['Host']['user'] = '--'
        return info

    def set_osenv(self):
        cfg = self.config
        os.environ['TEST_ROOT'] = os.getcwd()
        os.environ['TEST_LOGDIR'] = os.path.join(cfg.logroot, cfg.logdir)
        os.environ['TEST_COMPILER'] = cfg.compiler[self.compiler]
        os.environ['TEST_EXECUTER'] = cfg.executer[self.executer]
        os.environ['TEST_CFLAGS'] = cfg.cflags[self.cflags]
        if self.testcase:
            os.environ['TEST_TESTCASE'] = self.testcase
        if not os.path.exists(os.environ['TEST_LOGDIR']):
            os.makedirs(os.environ['TEST_LOGDIR'])
        logfile = os.path.join(os.environ['TEST_LOGDIR'], 'osenv.log')
        with open(logfile, 'w') as f:
            print('[Host]', file=f)
            info = self.get_envinfo()
            for k, v in info['Host'].items():
                print('%s: %s' % (k, v), file=f)
            print('[Environ]', file=f)
            for key in os.environ:
                print("%s: '%s'" % (key, os.environ[key]), file=f)

    def run_script(self):
        cfg = self.config
        script = cfg.runscript[self.suite]
        try:
            proc = subprocess.Popen(
                script,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                shell=True,
            )
            outs, errs = proc.communicate()
            logdir = os.environ['TEST_LOGDIR']
            with open('%s/%s' % (logdir, 'run_script.log'), 'w') as f:
                f.write(outs.decode('utf-8'))
        except Exception as e:
            print(e, file=os.path.join(logdir, 'run_script.err'))
            if proc:
                proc.terminate()


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
