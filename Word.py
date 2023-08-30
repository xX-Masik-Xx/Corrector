from Dictionary import Dictionary

class Word:
    def __init__(self, text, beginning: int, ending: int) -> None:
        self._text = text
        self._beginning = beginning
        self._ending = ending
        
        self.dictionary_word = self.identify_dictionary_word()
    
    def as_string(self) -> str:
        return self.text.string_text[self.beginning:self.ending]
    
    #TODO: Replace all the instances of "is_uppercase" as an attribute to calling a function
    def is_uppercase(self) -> bool:
        return self.text.string_text[self.beginning].isupper()
    
    def identify_dictionary_word(self) -> str:
        formatted_word = self.as_string().lower()
        
        if self.text.morph_analyzer.word_is_known(formatted_word):
            return self.text.morph_analyzer.normal_forms(formatted_word)
        else:
            self._spelling_mistake = True
            return Dictionary.closest_dictionary_words(formatted_word, self.text.dictionary)
    
    def replace_in_text(self, replacement: str) -> None:
        self.text.string_text = self.text.string_text[:self.beginning] + (replacement.capitalize() if self.is_uppercase() else replacement.lower()) + self.text.string_text[self.ending:]
        
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