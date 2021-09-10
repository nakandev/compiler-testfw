from __future__ import absolute_import, print_function, unicode_literals
import datetime
import getpass
import os
import platform
from collections import namedtuple
from collections import OrderedDict


class ReportBuilder():
    def __init__(self, config, logbase):
        self.report = TestReport()
        self.config = config
        self.suite = None
        log_suitedir, log_optdir = self.config.logdir.split('/', 1)
        self.logbase = os.path.join(self.config.logroot, log_suitedir)
        self._logdirs = None

    @property
    def logdirs(self):
        if self._logdirs is None:
            config = self.config
            logdirs = {}
            args = {'suite': self.suite}
            Target = namedtuple('Target', ' '.join(config.optkeys))
            for option in config.param_products(config.optkeys, restrictions=args):
                optiond = OrderedDict(zip(config.optkeys, option))
                lconfig = config.copy()
                lconfig._target = Target(**optiond)
                logdirs[tuple(optiond.items())] = lconfig.logdir
            self._logdirs = logdirs
        return self._logdirs

    def build(self):
        self.build_cover()
        self.build_envinfo()
        self.build_result()

    def build_cover(self):
        cfg = self.config
        cover = {}
        # cover.update(cfg.report_cover)
        for k, v in cfg.report_cover.items():
            cover[k] = v.format(target=self, report=self.report)
        cover['history'] = {
            'date': datetime.datetime.now().strftime('%Y-%m-%d'),
            'author': cover['author'],
            'comment': 'First publish',
        }
        self.report.cover = cover

    def build_envinfo(self):
        cfg = self.config
        info = {}
        info['Host'] = platform.uname()._asdict()
        try:
            info['Host']['user'] = getpass.getuser()
        except Exception:
            info['Host']['user'] = '--'
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

    def build_result(self):
        pass


class TestReport():
    def __init__(self):
        self.cover = {}
        self.envinfo = {}
        self.testcases = TestCaseList()
        self.references = TestCaseList()

    @property
    def today(self):
        return datetime.datetime.today().strftime('%Y/%m/%d')


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
                # raise KeyError(key)
                new_tc = TestCase()
                new_tc.name = key
                self.append(new_tc)
                return new_tc

    def __setitem__(self, key, value):
        if not isinstance(value, TestCase):
            raise ValueError('value must TestCase')
        if isinstance(key, int):
            self._testcase[key] = value
            value._list = self
        else:
            for i, tc in enumerate(self._testcase):
                if tc.name == key:
                    self._testcase[i] = value
                    value._list = self
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
        value._list = self

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

    @property
    def interim_keys(self):
        keys = []
        for ts in self._testcase:
            keys += list(ts.interim_results.keys())
            keys = sorted(set(keys), key=keys.index)
        return keys


class TestCase():
    RESULT_TYPE = ('pass', 'fail', 'xpass', 'xfail', 'skip', 'ignore', '--')

    def __init__(self):
        self._list = None
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
    def interim_results_values(self):
        if self._list:
            values = []
            for key in self._list.interim_keys:
                if key in self.interim_results:
                    values.append(self.interim_results[key])
                else:
                    values.append('--')
        else:
            values = list(self.interim_results.values())
        return values

    @property
    def interim_messages_values(self):
        if self._list:
            values = []
            for key in self._list.interim_keys:
                if key in self.interim_messages:
                    values.append(self.interim_messages[key])
                else:
                    values.append('--')
        else:
            values = list(self.interim_messages.values())
        return values


class TestDiff():
    def __init__(self, result, ref):
        self.result = result
        self.ref = ref

    def __str__(self):
        if self.diff == 'new':
            return '!%s' % (self.result)
        if self.diff == 'same':
            return '%s' % (self.result)
        return '%s (%s)' % (self.result, self.ref)

    @property
    def diff(self):
        if self.ref is None:
            return 'new'
        if self.result == self.ref:
            return 'same'
        return 'diff'
