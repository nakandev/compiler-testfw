import csv
import os


class CsvWriter():
    def __init__(self, config, report, reportdir):
        self.config = config
        self.report = report
        self.reportdir = reportdir

    def write(self):
        self.write_envinfo()
        self.write_references()
        self.write_results()

    def write_envinfo(self):
        envinfo = self.report.envinfo
        if hasattr(self.config, 'reportfile'):
            fname = self.config.reportfile + '.envinfo.csv'
            report_path = os.path.join(self.reportdir, fname)
        else:
            report_path = os.path.join(self.reportdir, 'report.envinfo.csv')
        with open(report_path, 'w') as f:
            for info_key, info in envinfo.items():
                print('[%s]' % (info_key), file=f)
                for key, val in info.items():
                    print('%s,"%s"' % (key, val), file=f)

    def write_references(self):
        if hasattr(self.config, 'reportfile'):
            fname = self.config.reportfile + '.ref.csv'
            report_path = os.path.join(self.reportdir, fname)
        else:
            report_path = os.path.join(self.reportdir, 'report.ref.csv')
        with open(report_path, 'w') as f:
            writer = csv.writer(f)
            writer.writerow(['testcase', 'result'] + self.report.testcases.interim_keys)
            for tc in self.report.testcases:
                writer.writerow([tc.name, tc.result] + tc.interim_results_values)

    def write_results(self):
        if hasattr(self.config, 'reportfile'):
            fname = self.config.reportfile + '.result.csv'
            report_path = os.path.join(self.reportdir, fname)
        else:
            report_path = os.path.join(self.reportdir, 'report.result.csv')
        with open(report_path, 'w') as f:
            writer = csv.writer(f)
            writer.writerow(['testcase', 'result'] + self.report.testcases.interim_keys)
            for tc in self.report.testcases:
                writer.writerow([tc.name, tc.result] + tc.interim_results_values)
