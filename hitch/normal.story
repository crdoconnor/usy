Example:
  params:
    python version: 3.5.0
  preconditions:
    python version: (( python version ))
    files:
      example.yaml: |
        # Simple YAML file
        property1: value1
        property2: 2
  scenario:
    - Run: |
        import usy

        with open('example.yaml', 'r') as handle:
          contents = handle.read()

        parsed = usy.load(contents)

Repr:
  based on: Example
  scenario:
    - Assert True: |
        repr(parsed) == "USY({'property1': 'value1', 'property2': '2'})"

Getters:
  based on: Example
  scenario:
    - Assert True: |
        parsed['property1'] == "value1"

    - Assert True: |
        parsed['property2'] == '2'

Getter nonexistent key:
  based on: Example
  scenario:
    - Assert Exception:
        command: |
          parsed['nonexistent'] == "value1"
        exception: KeyError

Setter on existing key:
  based on: Example
  preconditions:
    variables:
      changed_yaml: |
        # Simple YAML file
        property1: value1
        property2: value2
  scenario:
    - Run: |
        parsed['property2'] = "value2"

    - Assert True: |
        parsed['property2'] == "value2"

    - Assert True: |
        parsed.as_yaml() == changed_yaml

Setter on new key:
  based on: Example
  preconditions:
    variables:
      changed_yaml: |
        # Simple YAML file
        property1: value1
        property2: 2
        property3: value3
  scenario:
    - Run: |
        parsed['property3'] = "value3"

    - Assert True: |
        parsed['property3'] == "value3"

    - Assert True: |
        parsed.as_yaml() == changed_yaml

