class TestCase():
    __id_count = 0

    def __init__(self):
        TestCase.__id_count += 1
        self.id = TestCase.__id_count
        self.name = 'unknown'
        self._result = 'unknown'
        self.message = None

    @property
    def result(self):
        return self._result

    @result.setter
    def result(self, value):
        kind = ('pass', 'fail', 'xpass', 'xfail', 'skip', 'miss', 'ignore')
        if value in kind:
            self._result = value
        else:
            self._result = 'unknown'


class LogAnalyzer():
    def __init__(self):
        pass

    def walk_log(self):
        pass
