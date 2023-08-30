#imports
from CorrectAdvices.CorrectAdvice import CorrectAdvice
from Word import Word

class SpellingCorrectionAdvice(CorrectAdvice):
    def __init__(self, handler, beginning: int, ending: int, incorrect_word: Word, corrected_word: str) -> None:
        super().__init__(handler,
            "возможно вы имели в виду \033[1;32m{true_word}\033[0m вместо \033[1;9m\"{word}\"\033[0m",
            "Spelling", beginning, ending,
            answer_input_type = int,
            message_input_modifiers = {"true_word": (lambda x: " | ".join([f"{s} ({i+1})" for i, s in enumerate(x)])),
                                       "word": lambda x: x}
        )
        self._incorrect_word = incorrect_word
        self._corrected_word = corrected_word
        self._handler.push_mistake(self)

    def throw(self) -> str:
        return super().throw(true_word=self.corrected_word, word=self.incorrect_word.as_string())

    @staticmethod
    def check_for_presence(handler) -> None:
        for word in handler.get_text.contained_words:
            if getattr(word, "_spelling_mistake", False):
                SpellingCorrectionAdvice(handler, word.beginning, word.ending, word, word.dictionary_word)

    def correct(self, answer = None) -> None:
        super().correct(answer)
        self.incorrect_word.replace_in_text(self.corrected_word[answer - 1])
        self._handler.get_text.resplit_words()

    @property
    def incorrect_word(self) -> Word:
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