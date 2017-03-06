class Line(object):
    def __init__(self, text):
        self._text = text

    @property
    def is_key_value(self):
        return ":" in self._text
    
    @property
    def key(self):
        return self._text.split(":")[0]
    
    @property
    def value(self):
        return self._text.split(":")[1].lstrip()


class USY(object):
    """
    Ultra-simple YAML
    """
    def __init__(self, contents):
        self._contents = contents
    
    
    @property
    def lines(self):
        return [Line(line) for line in self._contents.split('\n')]

    def __getitem__(self, key):
        for line in self.lines:
            if line.is_key_value:
                if line.key == key:
                    return line.value
    
    def items(self):
        _vals = []
        for line in self.lines:
            if line.is_key_value:
                _vals.append((line.key, line.value))
        return _vals
    
    def __repr__(self):
        return u"USY({{{0}}})".format(
            ", ".join([
                "'{0}': '{1}'".format(key, value)
                for key, value in self.items()
            ])
        )


def load(contents):
    return USY(contents)
