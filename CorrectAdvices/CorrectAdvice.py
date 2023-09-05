class CorrectAdvice:
    def __init__(self, handler, message: str, mistake_type: str, beginning: int, ending: int, answer_input_type = None, message_input_modifiers = None) -> None:
        self.message = message
        self._mistake_type = mistake_type
        self._handler = handler
        self._beginning = beginning
        self._ending = ending
        self.answer_input_type = answer_input_type
        self.message_input_modifiers = message_input_modifiers

    def throw(self, **kwargs) -> str:
        data = kwargs if self.message_input_modifiers == None else {key:self.message_input_modifiers[key](value) for (key,value) in kwargs.items()}
        if kwargs.keys:
            return "\"{}\" — " + self.message.format(**data) + "?"
        else: 
            return f"\"{self._handler.get_text}\" — {self.message}?"

    def correct(self, answer = None) -> None:
        self._handler.mistakes_count -= 1
        self._handler.edited = True
        
    def correction_rejected(self) -> None:
        self._handler.mistakes_count -= 1

    @staticmethod
    def check_for_presence(self, handler):
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