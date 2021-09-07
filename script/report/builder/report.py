from __future__ import absolute_import, print_function, unicode_literals


class ReportBuilder():
    def __init__(self):
        self.report = TestReport()

    def build_cover(self):
        cover = {}
        cover['title'] = None
        self.report.cover = cover

    def build_envinfo(self):
        info = {}
        info['Host'] = None
        self.report.envinfo = info

    def build_result(self):
        pass


class TestReport():
    def __init__(self):
        self.cover = {}
        self.envinfo = {}
        self.testcases = TestCaseList()


class TestCaseList():
    def __init__(self):
        self._testcase = []

    def __getitem__(self, key):
        if isinstance(key, int):
            return self._testcase[key]
        else:
            for tc in self._testcase:
                if tc.name == key:
                    return tc
            else:
                raise KeyError('key:{} not in {}'.format(key, self.keys()))

    def __setitem__(self, key, value):
        if not isinstance(value, TestCase):
            raise ValueError('value must TestCase')
        if isinstance(key, int):
            self._testcase[key] = value
        else:
            for i, tc in enumerate(self._testcase):
                if tc.name == key:
                    self._testcase[i] = value
            else:
                raise KeyError()

    def __delitem__(self, key):
        if isinstance(key, int):
            del self._testcase[key]
        else:
            for i, tc in enumerate(self._testcase):
                if tc.name == key:
                    del self._testcase[i]
                    break
            else:
                raise KeyError()

    def __iter__(self):
        return self._testcase.__iter__()

    def append(self, value):
        if not isinstance(value, TestCase):
            raise ValueError('value must TestCase')
        self._testcase.append(value)

    def insert(self, idx, value):
        if not isinstance(value, TestCase):
            raise ValueError('value must TestCase')
        self._testcase.insert(idx, value)

    def clear(self):
        self._testcase.clear()

    def keys(self):
        return [tc.name for tc in self._testcase]

    def values(self):
        return list(self._testcase)


class TestCase():
    RESULT_TYPE = ('pass', 'fail', 'xpass', 'xfail', 'skip', 'ignore', '--')

    def __init__(self):
        self.id = str()
        self.name = str()
        self.brief = str()
        self.detail = str()
        self.author = str()
        self.exec_user = str()
        self.exec_date = str()
        self.exec_time = str()
        self.interim_results = {}
        self.interim_messages = {}
        self.result = '--'
        self.comment = str()

    @property
    def interim_results_keys(self):
        return list(self.interim_results.keys())

    @property
    def interim_results_values(self):
        return list(self.interim_results.values())
