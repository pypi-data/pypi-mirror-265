# Custom Components

It's possible to define any custom preprocessing step by extending the `AbstractTextStep` class. Let us import it:

```python
from gepref_text.base import AbstractTextStep
```

Let's see an example in which we want to perform the following operations:

1. Convert text to lowercase.
2. Add the `[sta]` and `[end]` tokens at the start and end of the string (this is a common practice when preparing data for generative models).

We can import the required components:

```python
from gepref_text.base import TextPreprocessor
from gepref_text.normalization import LowerStep
```

Now, we can implement a custom step that adds the new tokens. We have to extend the `AbstractTextStep` and implement the `call` method.


```python
class PadTokensStep(AbstractTextStep):
    def __init__(self, start_token: str="[sta]", end_token: str="[end]"):
        self.start_token = start_token
        self.end_token = end_token

    def call(self, data: str) -> str:
        return f"{self.start_token} {data} {self.end_token}"
```

Finally, we can define the preprocessor:

```python
preprocessor = TextPreprocessor(
    steps=[LowerStep(), PadTokensStep()]
)
```

Let us test it with the following sample text:

```python
example = "This is an Example"
```

The result:

```python
print(preprocessor(example))
```
