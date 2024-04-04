# Filtering

The `filtering` module contains several components for text filtering. This includes stopword filtering, length filters, among others.

Let's see an example in which we want to filter the following text:

```python
example = "this is an example text 2"
```

First, we'll import the components to build the pipeline:

```python
from gepref_text.base import TextPreprocessor
from gepref_text.filtering import StopwordFilterStep, TokenLenFilterStep
```

Let us detail these components:

- `TextPreprocessor`: class that composes several steps and defines the preprocessing pipeline.
- `StopwordFilterStep`: filters stopwords for a given language.
- `TokenLenFilterStep`: filters words in a lenght range.

The preprocessor can be implemented as:

```python
preprocessor = TextPreprocessor(
    steps=[StopwordFilterStep(lang="english"), TokenLenFilterStep(min_len=2, max_len=10)]
)
```

Finally, we can see the clean example:

```python
print(preprocessor(example))
```
