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

    @property
    def text(self):
        return self._text

    @value.setter
    def value(self, value):
        self._text = "{0}: {1}".format(self.key, value)


class USY(object):
    """
    Ultra-simple YAML
    """
    def __init__(self, contents):
        self._contents = contents
        self._lines = [
            Line(line) for line in self._contents.strip().split('\n')
        ]

    @property
    def lines(self):
        return self._lines

    def __getitem__(self, key):
        for line in self.lines:
            if line.is_key_value:
                if line.key == key:
                    return line.value
        raise KeyError(key)

    def __setitem__(self, key, value):
        for line in self.lines:
            if line.is_key_value:
                if line.key == key:
                    line.value = value
                    return
        self._lines.append(Line("{0}: {1}".format(key, value)))

    def items(self):
        _vals = []
        for line in self.lines:
            if line.is_key_value:
                _vals.append((line.key, line.value))
        return _vals

    def as_yaml(self):
        return "\n".join([line.text for line in self.lines]) + '\n'

    def __repr__(self):
        return u"USY({{{0}}})".format(
            ", ".join([
                "'{0}': '{1}'".format(key, value)
                for key, value in self.items()
            ])
        )


def load(contents):
    return USY(contents)
