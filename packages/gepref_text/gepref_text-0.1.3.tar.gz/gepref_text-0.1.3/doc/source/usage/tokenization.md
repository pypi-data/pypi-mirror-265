# Tokenization

The `tokenization` module allows to split tokens using different tokenization techniques (word, sentence, among others).

Let's see an example with the following text:

```python
example = "This is a text that has commas, this is the comma's example"
```

We can implement a preprocessor to perform the following tasks:

1. Perform word tokenization to separate punctuation.
2. Convert to lowercase.

Let's import the required components:

```python
from gepref_text.base import TextPreprocessor
from gepref_text.tokenization import WordTokenStep
from gepref_text.normalization import LowerStep
```

Let us detail these components:

- `TextPreprocessor`: class that composes several steps and defines the preprocessing pipeline.
- `WordTokenStep`: performs word tokenization.
- `LowerStep`: converts an input text to lowercase.

The preprocessor can be implemented as:

```python
preprocessor = TextPreprocessor(
    steps=[WordTokenStep(), LowerStep()]
)
```

Finally, we can see the clean example:

```python
print(preprocessor(example))
```
