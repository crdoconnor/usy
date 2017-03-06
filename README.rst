Ultra Simple YAML
=================

Ultra Simple YAML is a tiny module designed to parse a *very*
restricted subset of YAML. It is a sister project of StrictYAML
which parses a larger (albeit still restricted) subset of YAML.

It is designed to be includeable in larger projects where
including an entire additional module would be a problem.

Usage
-----

Given the following file example.yaml:

.. code-block:: yaml

  # Simple YAML file
  property1: value1
  property2: 2


Copy the file usy.py into your project and use:

.. code-block:: python

  >>> with open('example.yaml', 'r') as handle:
  >>>     contents = handle.read()
  >>> parsed = usy.load(contents)
  >>> parsed
  USY({"property1": "value1", "property2": "2"})

  >>> parsed["property1"]
  value1

  >>> parsed["property2"] == "2"
  True

  >>> parsed["property3"] = "3"

  >>> parsed.dump()
  # Simple YAML file
  property1: value1
  property2: 2
  property3: 3


What can and cannot be parsed?
------------------------------

* Only key/value pairs and comments will be parsed.
* No nested key/value pairs will be parsed or saved.
* No lists will be parsed.
* All values will be parsed as strings.

