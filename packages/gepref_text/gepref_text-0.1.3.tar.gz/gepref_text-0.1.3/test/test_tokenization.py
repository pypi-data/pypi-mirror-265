import nltk
import pytest
from gepref_text.tokenization import (
        WordTokenStep, SentTokenStep
        )

nltk.download("punkt")

@pytest.mark.parametrize("text, answer", [
    ("this is a text, let's try this", "this is a text , let 's try this"),
    ("simple, but effective", "simple , but effective"),
    ])
def test_word_token(text: str, answer: str):
    token_text = WordTokenStep()(text)
    assert answer == token_text

@pytest.mark.parametrize("text, answer", [
    ("This is good. This is really good", "This is good. This is really good"),
    ("My name is brian and I'm 20 years old, nice to meet you. How are you and what is your name?", "My name is brian and I'm 20 years old, nice to meet you. How are you and what is your name?"),
    ])
def test_sent_token(text: str, answer: str):
    token_text = SentTokenStep()(text)
    assert answer == token_text
