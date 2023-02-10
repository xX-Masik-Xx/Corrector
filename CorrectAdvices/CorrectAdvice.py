from CorrectionHandler import CorrectionHandler

class CorrectAdvice:
    def __init__(self, handler: CorrectionHandler, message: str, mistake_type: str, beginning: int, ending: int) -> None:
        self.message = message
        self._mistake_type = mistake_type
        self._handler = handler
        self._beginning = beginning
        self._ending = ending

    def throw(self, **kwargs) -> str:
        if kwargs.keys:
            return "\"{}\" — " + self.message.format(**kwargs) + "?"
        else: 
            return f"\"{self._handler.get_text}\" — {self.message}?"

    def correct(self) -> None:
        self._handler.mistakes_count -= 1

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