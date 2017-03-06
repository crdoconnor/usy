Example:
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
    - Assert True: |
        repr(parsed) == "USY({'property1': 'value1', 'property2': '2'})"
