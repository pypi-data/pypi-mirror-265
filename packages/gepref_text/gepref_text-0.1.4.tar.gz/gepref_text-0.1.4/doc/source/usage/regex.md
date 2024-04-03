# Regex

The `regex_sub` module includes components for regex-based text substitution, allowing to replace special characters, numbers, duplicated spaces, URLs, among others.

Let's see an example in which we want to perform the following preprocessing operations:

1. Remove URLs.
2. Remove special characters.
3. Remove duplicated spaces.
4. Replace the pattern `"Peter Parker"` with `"[author]"`

To this end, we can import the relevant components:

```python
from gepref_text.base import TextPreprocessor
from gepref_text.regex_sub import UrlRemovalStep, SpRemovalStep, DupSpacesStep, RegexRemovalStep
```

Let us detail these components:

- `TextPreprocessor`: class that composes several steps and defines the preprocessing pipeline.
- `UrlRemovalStep`: removes a _http_ or _https_ URL.
- `SpRemovalStep`: removes special characters.
- `DupSpacesStep`: removes duplicated spaces.
- `RegexRemovalStep`: uses the `set_pattern` and `set_replace_str` to respectively set a matching pattern and the string to substitute.

The preprocessor can be implemented as:

```python
import re
preprocessor = TextPreprocessor(
    steps=[
        UrlRemovalStep(), SpRemovalStep(), DupSpacesStep(),
        RegexRemovalStep().set_pattern(re.compile(r"Peter Parker")).set_replace_str("[author]")
        ]
)
```

Finally, let us define a sample text:

```python
example = "My name is Peter Parker (https://peterparker.com)   and I am not spiderman"
```

If we use the preprocessor:

```python
print(preprocessor(example))
```
