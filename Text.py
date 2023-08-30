#imports
from Word import Word
from Dictionary import Dictionary
from pymorphy2 import MorphAnalyzer

class Text:
    def __init__(self, string_text: str) -> None:
        self._string_text = string_text
        self.dictionary = Dictionary("russian.txt")
        self._morph_analyzer = MorphAnalyzer()
        self._contained_words = self.__split_words()

    def __split_words(self) -> list[Word]:
        alphabet = set("абвгдеёжзийклмнопрстуфхцчшщъыьэюяАБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ-")
        current_string = self._string_text + " "
        result_list = []
        if not current_string:
            return [Word(self, 0, len(self.string_text))]
        start = 0
        for index, char in enumerate(current_string):
            if len(set(current_string[start:index+1]).intersection(alphabet)) == 0:
                start += 1
            elif char not in alphabet:
                result_list.append(Word(self, start, index))
                start = index + 1
        if start == 0:
            return [Word(self, 0, len(self.string_text))]
        return result_list
    
    def resplit_words(self) -> None:
        self._contained_words = self.__split_words()

    def apply_correction(self, corrected_text: str) -> None:
        self._string_text = corrected_text

    def __str__(self) -> str:
        return self._string_text

    @property
    def contained_words(self) -> list[Word]:
        return self._contained_words

    def get_highlight(self, colour_code: str, begin: int, end: int) -> str:
        return self._string_text[:begin] + "\033[" + colour_code + self._string_text[begin:end] + "\033[0m" + self._string_text[end:]

    def get_play_down(self, begin: int, end: int) -> str:
        return self._string_text[:begin] + self._string_text[end:]

    @property
    def morph_analyzer(self) -> MorphAnalyzer:
        return self._morph_analyzer

    @property
    def string_text(self) -> str:
        return self._string_text

    @string_text.setter
    def string_text(self, new_text) -> None:
        self._string_text = new_text
        self.__split_words()