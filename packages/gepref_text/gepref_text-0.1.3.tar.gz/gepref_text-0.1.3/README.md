# GEneral PREprocessing Framework for TEXT (gepref_text)
---

<div align="center">
    <img src="./doc/source/_static/gepref_text.svg" alt="logo" width="60%"></img>
</div>

The `gepref_text` library is an implementation of the [gepref framework](https://github.com/juselara1/gepref/tree/main) for text preprocessing. It allows to easily build preprocessing pipelines from ready-to-use or custom components.

## Installation
---

You can install `gepref_text` with `pip`:

```sh
pip install gepref_text
```

## Usage
---

You can create preprocessing pipelines using `gepref_text`'s components. For instance, the following code creates a preprocessor that performs the following operations:

1. Removes URLs.
2. Converts to lowercase.
3. Removes special characters.
4. Removes numbers.
5. Removes duplicated spaces.
6. Trim the text.

Let's see the example code:

```python
from gepref_text.base import TextPreprocessor
from gepref_text.normalization import LowerStep, TrimStep
from gepref_text.regex import UrlRemovalStep, SpRemovalStep, NumRemovalStep, DupSpacesStep

text = "1. The main goal of this [project](https://myproject.com) is to do something.    Thanks."

preprocessor = TextPreprocessor(
    steps=[
        UrlRemovalStep(), LowerStep(), SpRemovalStep(),
        NumRemovalStep(), DupSpacesStep(), TrimStep()
    ]
)
print(preprocessor(text))
```

This will generate something like:

```
the main goal of this project is to do something thanks
```

You can check the [official documentation](https://juselara1.github.io/gepref_text/)
