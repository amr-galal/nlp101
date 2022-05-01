import typing as t
from abc import abstractmethod, abstractproperty
from dataclasses import dataclass

import re


class TextPreprocessor:
    @abstractmethod
    def __call__(self, text: str) -> str:
        pass


class ToLower(TextPreprocessor):
    def __call__(self, text: str) -> str:
        return text.lower()
    

@dataclass
class StopwordsRemover(TextPreprocessor):
    list_stopwords: t.List[str]

    def __call__(self, text: str) -> str:
        return ' '.join([ word for word in text.split() if (not word in self.list_stopwords) ])


@dataclass
class RegexMapper:
    regex: str
    sub: str
    flag: t.Union[re.RegexFlag, int] = 0


@dataclass
class RegexSubstituter(TextPreprocessor):
    regex_mapper: RegexMapper

    def __call__(self, text: str) -> str:
        regex = self.regex_mapper.regex
        sub = self.regex_mapper.sub
        flag = self.regex_mapper.flag

        return re.sub(pattern=regex, repl=sub, string=text, flags=flag)


@dataclass
class SequentialRegexSubstituter(TextPreprocessor):
    list_regex_mappers: t.List[RegexMapper]

    def __call__(self, text: str) -> str:
        for mapper in self.list_regex_mappers:
            text = RegexSubstituter(regex_mapper=mapper)(text)

        return text



@dataclass
class CompositeTextPreprocessors(TextPreprocessor):
    list_preprocessors: t.List[TextPreprocessor]

    def __call__(self, text: str) -> str:
        for preprocessor in self.list_preprocessors:
            text = preprocessor(text)
        return text