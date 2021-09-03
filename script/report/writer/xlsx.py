import openpyxl
import os


class XlsxWriter():
    def __init__(self, report, reportdir):
        self.report = report
        self.reportdir = reportdir
        self.book = openpyxl.Workbook()

    def write(self):
        self.write_cover()
        self.write_envinfo()
        self.write_results()
        report_path = os.path.join(self.reportdir, 'report.xlsx')
        self.book.save(report_path)

    def write_cover(self):
        sheet = self.book.worksheets[0]
        sheet.title = 'cover'
        sheet.cell(2, 2).value = self.report.cover['title']

        sheet.cell(4, 2).value = 'History:'
        sheet.cell(5, 2).value = 'date'
        sheet.cell(5, 3).value = 'author'
        sheet.cell(5, 4).value = 'comment'
        sheet.cell(6, 2).value = self.report.cover['history']['date']
        sheet.cell(6, 3).value = self.report.cover['history']['author']
        sheet.cell(6, 4).value = self.report.cover['history']['comment']

    def write_envinfo(self):
        sheet = self.book.create_sheet(title='envinfo')
        envinfo = self.report.envinfo
        i = 1
        for info_key, info in envinfo.items():
            sheet.cell(i, 1).value = '[%s]' % (info_key)
            i += 1
            for key, val in info.items():
                sheet.cell(i, 1).value = key
                if isinstance(val, dict):
                    for vk, vv in val.items():
                        sheet.cell(i, 2).value = str(vk)
                        sheet.cell(i, 3).value = str(vv)
                        i += 1
                elif isinstance(val, list):
                    for vv in val:
                        sheet.cell(i, 2).value = str(vv)
                        i += 1
                else:
                    sheet.cell(i, 2).value = str(val)
                    i += 1

    def write_results(self):
        sheet = self.book.create_sheet(title='results')
        tc = self.report.testcases[0]
        row = ['testcase'] + list(tc.interim_results.keys())
        for j in range(len(row)):
            sheet.cell(1, j + 1).value = row[j]
        for i, tc in enumerate(self.report.testcases):
            row = [tc.name] + list(tc.interim_results.values())
            for j in range(len(row)):
                sheet.cell(i + 2, j + 1).value = row[j]
