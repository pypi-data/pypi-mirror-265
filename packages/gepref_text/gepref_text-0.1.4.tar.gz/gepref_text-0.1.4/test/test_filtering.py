import nltk
import pytest
from gepref_text.filtering import StopwordFilterStep, TokenLenFilterStep
nltk.download("stopwords")

@pytest.mark.parametrize("text, answer", [
    ("this is a first example of something great", "first example something great"),
    ("i am the man who sold the world", "man sold world"),
    ])
def test_stopword_filter(text: str, answer: str):
    filter_text = StopwordFilterStep()(text)
    assert answer == filter_text

@pytest.mark.parametrize("text, answer, min_len, max_len", [
    ("a bb ccc dddd eeeee ffffff", "ccc dddd eeeee", 3, 5),
    ("a bb ccc dddd eeeee ffffff", "bb ccc dddd", 2, 4),
    ("a bb ccc dddd eeeee ffffff", "a bb ccc dddd eeeee ffffff", 1, 6),
    ])
def test_tokenlen_filter(text: str, answer: str, min_len: int, max_len: int):
    filter_text = TokenLenFilterStep(min_len=min_len, max_len=max_len)(text)
    assert answer == filter_text
