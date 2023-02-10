class WordFromText:
    def __init__(self, text, beginning: int, ending: int) -> None:
        self._text = text
        self._beginning = beginning
        self._ending = ending
        self.is_uppercase = self.text.string_text[beginning].isupper()
        
    def as_string(self) -> str:
        return self.text.string_text[self.beginning:self.ending]
    
    def replace_in_text(self, replacement: str) -> None:
        self.text.string_text = self.text.string_text[:self.beginning] + (replacement.capitalize() if self.is_uppercase else replacement) + self.text.string_text[self.ending:]
        
    def __str__(self) -> str:
        return self.as_string()
    
    def __repr__(self) -> str:
        return self.as_string()

    @property
    def text(self):
        return self._text

    @text.setter
    def text(self, new_text) -> None:
        self._text = new_text

    @property
    def beginning(self) -> int:
        return self._beginning
    
    @property
    def ending(self) -> int:
        return self._ending

    @beginning.setter
    def beginning(self, new_beginning) -> None:
        self._beginning = new_beginning

    @ending.setter
    def ending(self, new_ending) -> None:
        self._ending = new_ending