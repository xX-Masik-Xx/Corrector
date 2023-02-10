#imports
from Text import Text
#from nltk.corpus import brown

class CorrectionHandler:
    def __init__(self, text: Text) -> None:
        self.text = text
        self.mistakes_count = 0
        self.found_mistakes = []
        self.check_for_mistakes()

    def check_for_mistakes(self, edited = False) -> bool:
        from CorrectAdvices.CorrectAdvice import CorrectAdvice
        from CorrectAdvices.SpellingCorrectionAdvice import SpellingCorrectionAdvice
        for subclass in CorrectAdvice.__subclasses__():
            if subclass.check_for_presence(self):
                return True

        if self.mistakes_count == 0:
            print("Похоже, ошибок больше нет! Итоговый текст:" if edited else "Похоже, ошибок нет!")
            return False

    def push_mistake(self, mistake) -> None:
        self.mistakes_count += 1
        self.found_mistakes.append(mistake)
        mistake_type = mistake.mistake_type.lower()
        text_to_print = self.text.get_highlight("1;31m" if mistake_type == "spelling" else "", mistake.beginning, mistake.ending)

        #Спросить разрешения на исправление:
        answer = input(mistake.throw().format(text_to_print) + "  ").lower()
        if answer == "да":
            mistake.correct()
        if not self.check_for_mistakes(edited=True):
            print(self.get_text)

    @property
    def get_text(self) -> Text:
        return self.text