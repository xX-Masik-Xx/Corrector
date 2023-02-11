#imports
from CorrectAdvices.CorrectAdvice import CorrectAdvice
from CorrectionHandler import CorrectionHandler
from WordFromText import WordFromText

import difflib
from collections import defaultdict

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
        words_list = SpellingCorrectionAdvice.get_words_list()
        
        for word in handler.get_text.contained_words:
            first_letter_dicts = words_list[word.as_string().lower()[0]] + words_list[word.as_string().upper()[0]]
            if word.as_string().lower() not in first_letter_dicts:
                true_word = difflib.get_close_matches(word.as_string().lower(), first_letter_dicts, n=1)[0]
                mistake = SpellingCorrectionAdvice(handler, word.beginning, word.ending, word, true_word)
                mistake.corrected_word = true_word
                return True, mistake
        return False
    
    
    @staticmethod
    def get_words_list() -> list[str]:
        file = open('russian.txt','r')

        inpt = file.read().splitlines()
        result = defaultdict(list)
        for word in inpt:
            result[word[0]].append(word)
        return result

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