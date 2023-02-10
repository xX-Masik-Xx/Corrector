#imports
from CorrectAdvices.CorrectAdvice import CorrectAdvice
from CorrectionHandler import CorrectionHandler
from WordFromText import WordFromText
from Text import Text

from fuzzywuzzy import fuzz

class SpellingCorrectionAdvice(CorrectAdvice):
    def __init__(self, handler: CorrectionHandler, beginning: int, ending: int, incorrect_word: WordFromText, corrected_word: str) -> None:
        super().__init__(handler, "возможно вы имели в виду \033[1;32m{true_word}\033[0m, а не \033[1;9m\"{word}\"\033[0m", "Spelling", beginning, ending)
        self._incorrect_word = incorrect_word
        self._corrected_word = corrected_word
        self._handler.push_mistake(self)

    def throw(self) -> str:
        return super().throw(true_word=self.corrected_word, word=self.incorrect_word.as_string())

    @staticmethod
    def check_for_presence(handler: CorrectionHandler)-> bool:
        #Список слов
        words_list = ["яблоко", "груша", "апельсин"]

        for word in handler.get_text.contained_words:
            for true_word in words_list:
                if fuzz.ratio(word.as_string().lower(), true_word) > 65 and word.as_string().lower() not in words_list:
                    mistake = SpellingCorrectionAdvice(handler, word.beginning, word.ending, word, true_word)
                    mistake.corrected_word = true_word
                    return True, mistake
        return False

    def correct(self) -> None:
        super().correct()
        self.incorrect_word.replace_in_text(self.corrected_word)
        self._handler.get_text.resplit_words()

    @property
    def incorrect_word(self) -> WordFromText:
        return self._incorrect_word
    
    @property
    def corrected_word(self) -> str:
        return self._corrected_word
    
    @incorrect_word.setter
    def incorrect_word(self, incorrect_word: str) -> None:
        self._incorrect_word = incorrect_word

    @corrected_word.setter
    def corrected_word(self, corrected_word: str) -> None:
        self._corrected_word = corrected_word