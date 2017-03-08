"""
Ultra-Strict YAML

Usage::

  import usy

  with open('example.yaml', 'r') as handle:
     contents = handle.read()

  parsed = usy.load(contents)


License::

Copyright (c) 2017, Colm O'Connor
All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:

1. Redistributions of source code must retain the above copyright notice, this
   list of conditions and the following disclaimer.
2. Redistributions in binary form must reproduce the above copyright notice,
   this list of conditions and the following disclaimer in the documentation
   and/or other materials provided with the distribution.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR
ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
(INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
(INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
"""


class USYException(Exception):
    pass


class InvalidYAML(USYException):
    pass


class Line(object):
    def __init__(self, text):
        self._text = text

        if text.startswith(" "):
            raise InvalidYAML((
                "Line '{0}' starts with a space - this may "
                "be valid YAML but it is not valid USYAML."
            ).format(text))

        if not text.startswith("#"):
            if ":" not in text:
                raise InvalidYAML((
                    "Line '{0}'      not contain a ':' indicating "
                    "a property so it is not valid USYAML."
                ).format(text))

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
