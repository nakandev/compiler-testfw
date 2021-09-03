import csv
import os


class CsvWriter():
    def __init__(self, report, reportdir):
        self.report = report
        self.reportdir = reportdir

    def write(self):
        self.write_envinfo()
        self.write_results()

    def write_envinfo(self):
        envinfo = self.report.envinfo
        report_path = os.path.join(self.reportdir, 'report.envinfo.csv')
        with open(report_path, 'w') as f:
            for info_key, info in envinfo.items():
                print('[%s]' % (info_key), file=f)
                for key, val in info.items():
                    print('%s,"%s"' % (key, val), file=f)

    def write_results(self):
        report_path = os.path.join(self.reportdir, 'report.result.csv')
        with open(report_path, 'w') as f:
            writer = csv.writer(f)
            tc = self.report.testcases[0]
            writer.writerow(['testcase'] + list(tc.interim_results.keys()))
            for tc in self.report.testcases:
                writer.writerow([tc.name] + list(tc.interim_results.values()))
