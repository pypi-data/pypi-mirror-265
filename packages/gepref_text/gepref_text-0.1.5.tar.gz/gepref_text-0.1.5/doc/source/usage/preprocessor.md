# Preprocessor

The `TextPreprocessor` is the principal component to build a text preprocessing pipeline, it takes several `AbstractTextStep` to create an end-to-end preprocessing solution.

We can import the `TextPreprocessor` as:

```python
from gepref_text.base import TextPreprocessor
```

Let's see an example for the following pipeline:

<img src="../_static/preprocessor.svg">

We need to import the steps:

```python
from gepref_text.normalization import LowerStep, UnidecodeStep
```

Now, the pipeline can be defined as:

```python
preprocessor = TextPreprocessor(
    steps=[LowerStep(), UnidecodeStep()]
)
```

The preprocessor can be used to generate the same result as in the figure:

```python
print(preprocessor("Canción"))
```
