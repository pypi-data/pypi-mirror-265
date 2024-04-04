from abc import ABC, abstractmethod
from typing import Callable, List
from gepref_text.base import AbstractTextStep
from nltk.corpus import stopwords
from pydantic import PositiveInt

class AbstractTokenFilterStep(AbstractTextStep, ABC):
    """
    Interface that defines any regex substitution preprocessing step.
    The `get_pattern` method must be implemented.

    :param pattern: Regex pattern to match.
    :type pattern: re.Pattern
    :param replace_str: String to replace.
    :type replace_str: str
    """
    def call(self, data: str) -> str:
        """
        Preprocess an input text element.

        :param data: Input text element.
        :type data: str
        :returns: Preprocessed data.
        :rtype: str
        """
        tokens = data.split(" ")
        filtered_tokens = filter(self.get_condition(), tokens)
        return " ".join(filtered_tokens)

    @abstractmethod
    def get_condition(self) -> Callable[[str], bool]:
        ...

class StopwordFilterStep(AbstractTokenFilterStep):
    """
    Removes stopwords for a given language, uses NLTK list of stopwords.

    :param lang: Language for stopwords
    :type lang: str
    """
    def __init__(self, lang: str="english"):
        self.sw = stopwords.words(lang)

    def get_condition(self) -> Callable[[str], bool]:
        """
        Creates a function with the filter condition.

        :returns: Filter condition.
        :rtype: Callable[[str], bool]
        """
        return lambda token: token not in self.sw

class TokenLenFilterStep(AbstractTokenFilterStep):
    """
    Filters tokens based on a minimum and maximum number of characters.

    :param min_len: Minimum token length.
    :type min_len: PositiveInt
    :param max_len: Maximum token length.
    :type max_len: PositiveInt
    """
    def __init__(self, min_len: PositiveInt, max_len: PositiveInt):
        self.min_len = min_len
        self.max_len = max_len

    def get_condition(self) -> Callable[[str], bool]:
        """
        Creates a function with the filter condition.

        :returns: Filter condition.
        :rtype: Callable[[str], bool]
        """
        return lambda token: (
                len(token) >= self.min_len and len(token) <= self.max_len
                )

class CustomWordFilterStep(AbstractTokenFilterStep):
    """
    Excludes words from a custom list.

    :param exclude: Words to exclude.
    :type exclude: List[str]
    """

    def __init__(self, exclude: List[str]):
        self.exclude = exclude

    def get_condition(self) -> Callable[[str], bool]:
        """
        Creates a function with the filter condition.

        :returns: Filter condition.
        :rtype: Callable[[str], bool]
        """
        return lambda token: token not in self.exclude
