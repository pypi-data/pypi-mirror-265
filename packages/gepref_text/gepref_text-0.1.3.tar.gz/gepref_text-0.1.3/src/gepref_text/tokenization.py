from nltk.tokenize import word_tokenize, sent_tokenize
from gepref_text.base import AbstractTextStep


class WordTokenStep(AbstractTextStep):
    """
    Performs word tokenization using NLTK.

    :param lang: code language for tokenization.
    :type lang: str
    """
    def __init__(self, lang: str="english"):
        self.lang = lang

    def call(self, data: str) -> str:
        """
        Preprocess an input text element.

        :param data: Input text element.
        :type data: str
        :returns: Preprocessed data.
        :rtype: str
        """
        tokens = word_tokenize(data, language=self.lang)
        return " ".join(tokens)

class SentTokenStep(AbstractTextStep):
    """
    Performs sentence tokenization using NLTK.

    :param lang: code language for tokenization.
    :type lang: str
    """
    def __init__(self, lang: str="english"):
        self.lang = lang

    def call(self, data: str) -> str:
        """
        Preprocess an input text element.

        :param data: Input text element.
        :type data: str
        :returns: Preprocessed data.
        :rtype: str
        """
        tokens = sent_tokenize(data, language=self.lang)
        return " ".join(tokens)
