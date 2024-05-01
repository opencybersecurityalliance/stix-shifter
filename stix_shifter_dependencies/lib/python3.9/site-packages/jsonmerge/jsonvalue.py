# vim:ts=4 sw=4 expandtab softtabstop=4
import sys

if sys.version_info[0] >= 3:
    text_type = str
else:
    text_type = unicode

class JSONValue(object):
    def __init__(self, val=None, ref='#', undef=False):
        assert not isinstance(val, JSONValue)
        self.val = val
        self.ref = ref
        self.undef = undef

    def is_undef(self):
        return self.undef

    def _ref_escape(self, key):
        return key.replace('~', '~0').replace('/', '~1')

    def _subval(self, key, **kwargs):
        return JSONValue(ref=self.ref+'/'+self._ref_escape(text_type(key)), **kwargs)

    def __setitem__(self, key, item):
        if item.is_undef():
            if isinstance(self.val, list):
                raise ValueError("Can't assign an undefined value to a list")

            # setting a dict element to an undefined value deletes that element
            if key in self.val:
                del self.val[key]
        else:
            self.val[key] = item.val

    def __getitem__(self, key):
        return self._subval(key, val=self.val[key])

    def append(self, item):
        assert isinstance(self.val, list)

        if not item.is_undef():
            self.val.append(item.val)

    def get(self, key, *args):
        r = self.val.get(key, *args)
        if r is None:
            return self._subval(key, undef=True)
        else:
            return self._subval(key, val=r)

    def __repr__(self):
        if self.is_undef():
            return 'JSONValue(undef=True)'
        else:
            return 'JSONValue(%r,%r)' % (self.val, self.ref)

    def items(self):
        for k, v in self.val.items():
            yield (k, self._subval(k, val=v))

    def __iter__(self):
        assert isinstance(self.val, list)

        for i, v in enumerate(self.val):
            yield self._subval(i, val=v)

    def sort(self, *args, **kwargs):
        assert isinstance(self.val, list)

        i = list(self)
        i.sort(*args, **kwargs)
        self.val = [ j.val for j in i ]
