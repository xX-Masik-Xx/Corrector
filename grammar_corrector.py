#imports
from difflib import SequenceMatcher
import string
#from nltk.corpus import brown

class WordFromText:
    def __init__(self, text, beginning: int, ending: int) -> None:
        self._text = text
        self._beginning = beginning
        self._ending = ending
        
    def as_string(self) -> str:
        return self.text.string_text[self.beginning:self.ending]
    
    def replace_in_text(self, replacement: str) -> None:
        self.text = self.text.string_text[:self.beginning] + replacement + self.text.string_text[self.ending:]
        
    def __str__(self) -> str:
        return self.as_string()
    
    def __repr__(self) -> str:
        return self.as_string()

    @property
    def text(self):
        return self._text

    @text.setter
    def text(self, new_text):
        self._text = new_text

    @property
    def beginning(self) -> int:
        return self._beginning
    
    @property
    def ending(self) -> int:
        return self._ending

    @beginning.setter
    def beginning(self, new_beginning):
        self._beginning = new_beginning

    @ending.setter
    def ending(self, new_ending):
        self._ending = new_ending

#Класс текста
class Text:
    def __init__(self, string_text: str) -> None:
        self._string_text = string_text
        self._contained_words = self.__split_words()
        self.corrected_text = None

    def __split_words(self) -> list[WordFromText]:
        delimiter = " "
        current_string = self._string_text.translate(str.maketrans('', '', string.punctuation)).replace("	", "")
        result_list = []
        if not current_string:
            print [WordFromText(self, 0, len(self.string_text))]
            return [WordFromText(self, 0, len(self.string_text))]
        start = 0
        for index, char in enumerate(current_string):
            if char == delimiter:
                result_list.append(current_string[start:index])
                start = index + 1
        if start == 0:
            return [WordFromText(self, 0, len(self.string_text))]
        result_list.append(WordFromText(self, start, index + 1))
        
        print(result_list)
        return result_list

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

#Класс для управления советами по исправлению
class CorrectionHandler:
    def __init__(self, text: Text) -> None:
        self.text = text
        self.mistakes_count = 0
        self.found_mistakes = []
        self.check_for_mistakes()

    def check_for_mistakes(self) -> None:
        for subclass in CorrectAdvice.__subclasses__():
            subclass.check_for_presence(self)

        if self.mistakes_count == 0:
            print("Похоже, ошибок нет!")

    def push_mistake(self, mistake) -> None:
        self.mistakes_count += 1
        self.found_mistakes.append(mistake)
        mistake_type = mistake.mistake_type.lower()
        self.text.string_text = self.text.get_highlight("1;31m" if mistake_type == "spelling" else "", mistake.beginning, mistake.ending)

        #Спросить разрешения на исправление:
        answer = input(mistake.throw() + "  ").lower()
        if answer == "да":
            mistake.correct()
            print(self.get_text)

    @property
    def get_text(self) -> Text:
        return self.text

#Базовый класс для советов по исправлению
class CorrectAdvice:
    def __init__(self, handler: CorrectionHandler, message: str, mistake_type: str, beginning: int, ending: int) -> None:
        self.message = message
        self._mistake_type = mistake_type
        self._handler = handler
        self._beginning = beginning
        self._ending = ending

    def throw(self, **kwargs) -> str:
        if kwargs.keys:
            return "\"{}\" — ".format(self._handler.get_text) + self.message.format(**kwargs) + "?"
        else: 
            return f"\"{self._handler.get_text}\" — {self.message}?"

    def correct(self) -> None:
        pass

    @staticmethod
    def check_for_presence(self, handler: CorrectionHandler):
        pass

    @property
    def mistake_type(self) -> str:
        return self._mistake_type

    @mistake_type.setter
    def mistake_type(self, mistake_type: str) -> None:
        self._mistake_type = mistake_type

    @property
    def beginning(self) -> int:
        return self._beginning
    
    @property
    def ending(self) -> int:
        return self._ending

#Список слов
words_list = ["яблоко", "груша", "апельсин"]

#Класс для советов по орфографии
class SpellingCorrectionAdvice(CorrectAdvice):
    def __init__(self, handler: CorrectionHandler, beginning: int, ending: int, incorrect_word: WordFromText, corrected_word: str) -> None:
        super().__init__(handler, "возможно вы имели в виду \033[1;32m{true_word}\033[0m, а не \033[1;9m\"{word}\"\033[0m", "Spelling", beginning, ending)
        self._incorrect_word = incorrect_word
        self._corrected_word = corrected_word
        self._handler.push_mistake(self)

    def throw(self) -> str:
        return super().throw(true_word=self.corrected_word, word=self.incorrect_word.as_string())

    @staticmethod
    def check_for_presence(handler: CorrectionHandler)-> tuple[bool, CorrectAdvice]:
        for word in handler.get_text.contained_words:
            for true_word in words_list:
                if SequenceMatcher(None, word.as_string().lower(), true_word).ratio() > 0.75 and word.as_string().lower() not in words_list:
                    mistake = SpellingCorrectionAdvice(handler, word.beginning, word.ending, word, true_word)
                    mistake.corrected_word = true_word
                    return True, mistake

    def correct(self) -> None:
        self.incorrect_word.replace_in_text(self.corrected_word)

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

if __name__ == "__main__":
    #input
    print("Введите текст:")
    input_text = Text(input())
    
    #Экземпляр CorrectionHandler:
    CorrectionHandler(input_text)