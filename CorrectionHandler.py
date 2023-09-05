#imports
from Text import Text
from CorrectAdvices.CorrectAdvice import CorrectAdvice
from CorrectAdvices.SpellingCorrectionAdvice import SpellingCorrectionAdvice

class CorrectionHandler:
    def __init__(self, text: Text) -> None:
        self.text = text
        self.mistakes_count = 0
        self.found_mistakes = []
        self.edited = False
        self.check_for_mistakes()

    def check_for_mistakes(self) -> bool:
        for subclass in CorrectAdvice.__subclasses__():
            subclass.check_for_presence(self)

        if self.mistakes_count == 0:
            print("Похоже, ошибок больше нет! Итоговый текст:" if self.edited else "Похоже, ошибок нет!")
            print(self.text.string_text)
            return False

    def push_mistake(self, mistake) -> None:
        self.mistakes_count += 1
        self.found_mistakes.append(mistake)
        mistake_type = mistake.mistake_type.lower()
        text_to_print = self.text.get_highlight("1;31m" if mistake_type == "spelling" else "", mistake.beginning, mistake.ending)

        #Спросить разрешения на исправление:
        answer = input(mistake.throw().format(text_to_print) + "  ").lower()
        valid_input_type = mistake.answer_input_type
        if answer == "нет":
            mistake.correction_rejected()
        elif valid_input_type != None:
            try:
                if valid_input_type == int:
                    mistake.correct(int(answer))
            except ValueError:
                print("\033[1;9mНевозможный ответ\033[0m")
        else:
            mistake.correct()

    @property
    def get_text(self) -> Text:
        return self.text