from __future__ import absolute_import, print_function, unicode_literals
import csv
import datetime
import getpass
import glob
import os
import platform
from .report import ReportBuilder
from .report import TestCase


class LlvmTestsuiteReportBuilder(ReportBuilder):
    def __init__(self, config, logbase):
        super().__init__()
        self.config = config
        self.logbase = logbase
        self._logdirs = None

    @property
    def logdirs(self):
        if self._logdirs is None:
            logfiles = os.listdir(self.logbase)
            self._logdirs = {}
            for f in logfiles:
                absf = os.path.join(self.logbase, f)
                if os.path.isdir(absf):
                    self._logdirs[f] = absf
        return self._logdirs

    def build(self):
        self.build_cover()
        self.build_envinfo()
        self.build_result()

    def build_cover(self):
        cfg = self.config
        cover = {}
        cover['title'] = cfg.title
        cover['history'] = {
            'date': datetime.datetime.now().strftime('%Y-%m-%d'),
            'author': cfg.author,
            'comment': 'First publish',
        }
        self.report.cover = cover

    def build_envinfo(self):
        cfg = self.config
        info = {}
        info['Host'] = platform.uname()._asdict()
        info['Host']['user'] = getpass.getuser()
        info['Target'] = {
            'compiler': cfg.compiler,
            'executer': cfg.executer,
        }
        info['Option'] = {
            'cflags': cfg.cflags,
            'cc_cflags': cfg.cc_cflags,
            'cc_ldflags': cfg.cc_ldflags,
        }
        self.report.envinfo = info

    def collect_testcase(self):
        self.report.testcases.clear()
        testlist_fpath = os.path.join(self.logbase, 'testlist.txt')
        if os.path.exists(testlist_fpath):
            with open(testlist_fpath, 'r') as f:
                for line in f:
                    tc = TestCase()
                    tc.name = line.strip()
                    self.report.testcases.append(tc)

    def collect_reference(self):
        # testlist_fpath = os.path.join(self.logbase, 'reference.csv')
        pass

    def build_result(self):
        self.collect_testcase()
        testcases = self.report.testcases
        for opt, logdir in self.logdirs.items():
            loganalyzer = LlvmTestsuiteLogAnalyzer(logdir)
            opt_results = loganalyzer.get_results()
            for name, result in opt_results.items():
                if name not in testcases.keys():
                    new_tc = TestCase()
                    new_tc.name = name
                    testcases.append(new_tc)
                testcases[name].interim_results[opt] = result


class LlvmTestsuiteLogAnalyzer():
    def __init__(self, logdir):
        self.logdir = logdir

    def get_results(self):
        report_fname = 'report.simple.csv'
        pathfmt = '%s/**/%s' % (self.logdir, report_fname)
        report_fpath = glob.glob(pathfmt, recursive=True)[0]
        results = {}
        with open(report_fpath, 'r') as report_csv:
            reader = csv.reader(report_csv)
            next(reader)
            for row in reader:
                name, c_result, e_result = row[0], row[1], row[4]
                if c_result == 'pass' and e_result == 'pass':
                    result = 'pass'
                elif c_result == 'pass' and e_result == '*':
                    result = 'e_fail'
                elif c_result == '*' and e_result == '*':
                    result = 'c_fail'
                else:
                    result = 'c_fail'
                results[name] = result
        return results