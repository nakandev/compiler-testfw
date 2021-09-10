from __future__ import absolute_import, print_function, unicode_literals
import csv
import glob
import os
from .report import ReportBuilder
from .report import TestCase
from .report import TestDiff


class LlvmTestsuiteReportBuilder(ReportBuilder):
    def __init__(self, config, logbase):
        super().__init__(config, logbase)
        self.suite = 'llvm'

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
        references = self.report.references
        ref_fpath = os.path.join(self.config.refroot, self.suite, self.config.reffile)
        if os.path.exists(ref_fpath):
            with open(ref_fpath, 'r') as f:
                reader = csv.reader(f)
                # name, result, [interim_results], comment
                head = next(reader)
                optkeys = head[2:-1]
                for row in reader:
                    name, result = row[0:2]
                    interim_results = dict(zip(optkeys, row[2:-1]))
                    comment = row[-1:]
                    references[name].name = name
                    references[name].result = result
                    references[name].interim_results = interim_results
                    references[name].comment = comment

    def build_result(self):
        self.collect_reference()
        self.collect_testcase()
        testcases = self.report.testcases
        for opt, logdir in self.logdirs.items():
            abslogdir = os.path.join(self.config.logroot, logdir)
            loganalyzer = LlvmTestsuiteLogAnalyzer(abslogdir)
            ret = loganalyzer.get_results()
            opt_results, opt_times = ret
            for name, result in opt_results.items():
                testcases[name].interim_results[opt] = result
            for name, time in opt_times.items():
                testcases[name].exec_time = time
        interim_keys = testcases.interim_keys
        for tc in testcases:
            new_interim_results = {}
            for opt in interim_keys:
                if opt in tc.interim_results:
                    new_interim_results[opt] = tc.interim_results[opt]
                else:
                    new_interim_results[opt] = '--'
            tc.interim_results = new_interim_results
        for tc in testcases:
            for opt in tc.interim_results.keys():
                tdiff = self._compare_result_ref(tc.name, opt)
                tc.interim_results[opt] = tdiff

    def _compare_result_ref(self, name, opt):
        tc_iresult = self.report.testcases[name].interim_results[opt]
        if name not in list(self.report.references.keys()):
            ref_iresult = None
        elif str(opt) not in list(self.report.references[name].interim_results.keys()):
            ref_iresult = None
        else:
            ref_iresult = self.report.references[name].interim_results[str(opt)]
        tdiff = TestDiff(tc_iresult, ref_iresult)
        return tdiff


class LlvmTestsuiteLogAnalyzer():
    def __init__(self, logdir):
        self.logdir = logdir
        self.get_true_logdir()

    def get_true_logdir(self):
        fname = 'report.simple.csv'
        pathfmt = '%s/**/%s' % (self.logdir, fname)
        fpaths = glob.glob(pathfmt, recursive=True)
        if len(fpaths) == 0:
            raise Exception('true_logdir not found: %s' % (pathfmt))
        self.true_logdir = os.path.dirname(fpaths[0])

    def get_results(self):
        report_fname = 'report.simple.csv'
        report_fpath = os.path.join(self.true_logdir, report_fname)
        results = {}
        exec_times = {}
        with open(report_fpath, 'r') as report_csv:
            reader = csv.reader(report_csv)
            next(reader)
            for row in reader:
                # name, c_result, e_result = row[0], row[1], row[4]
                name, c_result, c_time, c_rtime, e_result, e_time, e_rtime = row
                if c_result == 'pass' and e_result == 'pass':
                    result = 'PASS'
                elif c_result == 'pass' and e_result == '*':
                    result = 'E_FAIL'
                elif c_result == '*':
                    result = 'C_FAIL'
                else:
                    result = 'UNKNOWN'
                results[name] = result
                exec_times[name] = e_rtime
        return results, exec_times

    def get_execinfo(self):
        # dirname, elfname = name.rsplit('/', 1)
        # execdir = os.path.join(logdir, dirname, 'Output')
        pass
