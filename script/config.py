import copy
import itertools
import types


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

    def __getattr__(self, name):
        if name.startswith('value_'):
            attrkey = name[len('value_'):]
            if not hasattr(self, attrkey):
                raise AttributeError
            attr = getattr(self, attrkey)
            target_attr = getattr(self._target, attrkey)
            return attr[target_attr]
        raise AttributeError

    def load(self, fpath):
        with open(fpath, 'r') as f:
            self.rawdata = f.read()
        exec(self.rawdata)
        params = locals()
        for param in params.keys():
            if isinstance((params[param]), type):
                params.pop(param)
            elif isinstance((params[param]), types.ModuleType):
                params.pop(param)
        for key in ('self', 'fpath', 'rawdata', 'f', '_target'):
            if key in params:
                params.pop(key)
        for key in params:
            value = params[key]
            setattr(self, key, value)

    def copy(self):
        return copy.copy(self)

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

    def param_restricts(self, keys, values, restrictions):
        if hasattr(restrictions, '__dict__'):
            restrictions = vars(restrictions)
        optvalues = list()
        for option in values:
            match = True
            for i, key in enumerate(keys):
                if restrictions.get(key):
                    if option[i] != restrictions[key]:
                        match = False
            if match:
                optvalues.append(option)
        return optvalues

    def options(self, args):
        if hasattr(self, 'optvalues'):
            for option in self.param_restricts(self.optkeys, self.optvalues, args):
                yield option
        else:
            for option in self.param_products(self.optkeys, args):
                yield option
