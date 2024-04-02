# universal_common
Library that extends the base class library functionality.

### Dictionary
Drop in replacement for the built-in dict that supports either attribute access or indexing.
```python
dictionary: Dictionary = Dictionary({ "a": 1 })

assert dictionary.a == 1
assert dictionary["a"] == 1
assert dictionary.b is None # Does not raise errors.
```