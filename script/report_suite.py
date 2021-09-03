#!/usr/bin/env python

import argparse
import os
from collections import OrderedDict
from config import Config
from report import LlvmTestsuiteReportBuilder
from report import CsvWriter, XlsxWriter


def report_all(args, config):
    reportargs = []
    optkeys = ('suite',)
    for option in config.param_products(optkeys, restrictions=args):
        optiond = OrderedDict(zip(optkeys, option))
        reportargs.append([config, optiond])
    for config_, optiond_ in reportargs:
        print('Start: %s' % optiond_)
        reporter = CompilerTestReporter(config_, optiond_)
        reporter.report()


class CompilerTestReporter():
    builder_cls = {
        'llvm': LlvmTestsuiteReportBuilder,
    }
    writer_cls = {
        'csv': CsvWriter,
        'xlsx': XlsxWriter,
    }

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
        cfg = self.config
        logbase = os.path.join(cfg.logroot, cfg.reportdir)
        builder = self.builder_cls[self.suite](cfg, logbase)
        builder.build()
        reportdir = os.path.join(cfg.reportroot, cfg.reportdir)
        if not os.path.exists(reportdir):
            os.makedirs(reportdir)
        writer = self.writer_cls['xlsx'](builder.report, reportdir)
        writer.write()


def main():
    parser = argparse.ArgumentParser(description='TestSuite Reporter.')
    parser.add_argument('--config', help='Test target Config file', default=None)
    parser.add_argument('--suite', help='Test Suite', default='llvm')
    args = parser.parse_args()
    if args.config is None or not os.path.exists(args.config):
        raise Exception('Config file not exists: %s' % args.config)

    config = Config()
    config.load(args.config)
    report_all(args, config)
    # reporter = CompilerTestReporter(vars(args), config)
    # reporter.report()


if __name__ == '__main__':
    main()
