import typing as t
from abc import abstractmethod
from dataclasses import dataclass

from nltk.tokenize import word_tokenize


class TokenizerWrapper:
    @abstractmethod
    def __call__(self, text: str) -> str:
        pass


class NLTKWordTokenizer(TokenizerWrapper):
    def __call__(self, text: str) -> str:
        return word_tokenize(text)

@dataclass
class TextTokenizer:
    tokenizer: TokenizerWrapper

    def __call__(self, text: str) -> str:
        return self.tokenizer(text=text)
