import itertools


class Config(object):
    def __init__(self, target=None):
        self._target = target

    def __getattribute__(self, name):
        value = object.__getattribute__(self, name)
        if name == '_target':
            return value
        if isinstance(value, str):
            target = object.__getattribute__(self, '_target')
            if target is not None:
                return value.format(target=target)
            else:
                return value
        else:
            return value

    def load(self, fpath):
        with open(fpath, 'r') as f:
            self.rawdata = f.read()
        exec(self.rawdata)
        params = locals()
        for key in ('self', 'fpath', 'rawdata', 'f', 'OrderedDict',
                    'os', 'sys', '_target'):
            if key in params:
                params.pop(key)
        for key in params:
            value = params[key]
            setattr(self, key, value)

    def todict(self):
        d = dict(self.__dict__)
        return d

    def param_products(self, keys, restrictions=None):
        if hasattr(restrictions, '__dict__'):
            restrictions = vars(restrictions)
        attrs = []
        for key in keys:
            attr = getattr(self, key)
            if restrictions and key in restrictions and restrictions[key]:
                attr = restrictions[key]
            if isinstance(attr, list) or isinstance(attr, tuple):
                pass
            elif isinstance(attr, dict):
                attr = list(attr.keys())
            else:
                attr = [attr]
            attrs.append(attr)
        params = itertools.product(*attrs)
        return params
