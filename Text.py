#imports
from WordFromText import WordFromText
import string

class Text:
    def __init__(self, string_text: str) -> None:
        self._string_text = string_text
        self._contained_words = self.__split_words()
        self.corrected_text = None

    def __split_words(self) -> list[WordFromText]:
        delimiters = {" ", "!","\"","#","$","%","&","\'","(",")","*","+","-",".",",","/",":",";","<","=",">","?","@","[","]","^","_","`","{","|","}","~"}
        ignore = {"	"}
        current_string = self._string_text + " "
        result_list = []
        if not current_string:
            return [WordFromText(self, 0, len(self.string_text))]
        start = 0
        for index, char in enumerate(current_string):
            if char in delimiters:
                if not (set(current_string[start:index+1]).issubset(delimiters)):
                    result_list.append(WordFromText(self, start, index))
                    start = index + 1
                else:
                    start += 1
            elif char in ignore:
                start += 1
        if start == 0:
            return [WordFromText(self, 0, len(self.string_text))]
        
        return result_list
    
    def resplit_words(self) -> None:
        self._contained_words = self.__split_words()

    def apply_correction(self, corrected_text: str) -> None:
        self._string_text = corrected_text

    def __str__(self) -> str:
        return self._string_text

    @property
    def contained_words(self) -> list[WordFromText]:
        return self._contained_words

    def get_highlight(self, colour_code: str, begin: int, end: int) -> str:
        return self._string_text[:begin] + "\033[" + colour_code + self._string_text[begin:end] + "\033[0m" + self._string_text[end:]

    def get_play_down(self, begin: int, end: int) -> str:
        return self._string_text[:begin] + self._string_text[end:]

    @property
    def string_text(self) -> str:
        return self._string_text

    @string_text.setter
    def string_text(self, new_text) -> None:
        self._string_text = new_text
        self.__split_words()