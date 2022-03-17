#!/usr/bin/env python

import argparse
import os
from collections import OrderedDict
from config import Config
from report import LlvmTestsuiteReportBuilder
from report import CsvWriter
from report import XlsxWriter


def report_all(args, config):
    reportargs = []
    reportoptkeys = ('suite',)
    for option in config.param_products(reportoptkeys, restrictions=args):
        optiond = OrderedDict(zip(reportoptkeys, option))
        optiond['writer'] = args.writer
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
        self.writer = option.get('writer')

    def report(self):
        cfg = self.config
        log_suitedir, log_optdir = cfg.logdir.split('/', 1)
        logbase = os.path.join(cfg.logroot, log_suitedir)
        builder = self.builder_cls[self.suite](cfg, logbase)
        builder.build()
        reportdir = os.path.join(cfg.reportroot, cfg.reportdir)
        if not os.path.exists(reportdir):
            os.makedirs(reportdir)
        writer = self.writer_cls[self.writer](cfg, builder.report, reportdir)
        writer.write()


def main():
    parser = argparse.ArgumentParser(description='TestSuite Reporter.')
    parser.add_argument('--config', help='Test target Config file', default=None)
    parser.add_argument('--suite', help='Test Suite', default='llvm')
    parser.add_argument('--writer', help='Report Writer', default='xlsx')
    args = parser.parse_args()
    if args.config is None or not os.path.exists(args.config):
        raise Exception('Config file not exists: %s' % args.config)

    config = Config()
    config.load(args.config)
    report_all(args, config)


if __name__ == '__main__':
    main()
