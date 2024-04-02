# Normalization

The `normalization` module contains several components for text normalization. This includes writing modification, unicode normalization, and trimming.

Let's see an example in which we want to clean the following text:

```python
example = "---ThIs is ThE eXample----"
```

First, we'll import the components to build the pipeline:

```python
from gepref_text.base import TextPreprocessor
from gepref_text.normalization import LowerStep, TrimStep
```

Let us detail these components:

- `TextPreprocessor`: class that composes several steps and defines the preprocessing pipeline.
- `LowerStep`: converts an input text to lowercase.
- `TrimStep`: performs text trimming using a given set of characters to exclude.

The preprocessor can be implemented as:

```python
preprocessor = TextPreprocessor(
    steps=[LowerStep(), TrimStep(chars="-")]
)
```

Finally, we can see the clean example:

```python
print(preprocessor(example))
```
