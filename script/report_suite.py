#!/usr/bin/env python

from config import Config
import argparse
import os


class CompilerTestReporter():
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

    def report(self):
        pass


def main():
    parser = argparse.ArgumentParser(description='TestSuite Reporter.')
    parser.add_argument('--config', help='Test target Config file', default=None)
    parser.add_argument('--suite', help='Test Suite', default='llvm')
    args = parser.parse_args()
    if args.config is None or not os.path.exists(args.config):
        raise Exception('Config file not exists: %s' % args.config)

    config = Config()
    config.load(args.config)
    reporter = CompilerTestReporter(vars(args), config)
    reporter.report()


if __name__ == '__main__':
    main()
