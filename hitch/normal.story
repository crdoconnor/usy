Base story:
  params:
    python version: 3.5.0
  preconditions:
    python version: (( python version ))

Example:
  based on: Base story
  preconditions:
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

Invalid YAML:
  based on: Base story
  preconditions:
    variables:
      example_indented: |
        # YAML file with indent
        property1: value1
          property2: 2
      example_not_property: |
        # YAML file without :
        just a line of text
  scenario:
    - Assert Exception:
        command: |
          import usy

          parsed = usy.load(example_indented)
        exception: InvalidYAML
    - Assert Exception:
        command: |
          import usy

          parsed = usy.load(example_not_property)
        exception: InvalidYAML

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

