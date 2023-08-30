from enum import Enum

class DictionaryWord:
    def __init__(self, string: str|list[str], definition) -> None:
        self.string = string
        self.definition = definition
        
    def __repr__(self) -> str:
        return self.dictionary_format()
    
    def __str__(self) -> str:
        return self.string
        
    def dictionary_format(self) -> str:
        if type(self.definition) == list:
            return f"\033[1m«{self.string.capitalize()}»\033[0m" + "\n" + '\n'.join([f'{index + 1}. {define}' for index, define in enumerate(self.definition)])
        else:
            return self.string + " — " + self.definition
        
    @staticmethod
    def instantiate(string: str|list[str], meaning, part_of_speech: str, **morphology):
        return globals()[part_of_speech](string, meaning, **morphology)
    
    @staticmethod
    def from_string(string:str, dictionary):
        return next((word for word in dictionary.dictionary[string[0]] if word.string == string), None)
        
class Gender(Enum):
    masculine = 0
    feminine = 1
    neuter = 2
    
class Term(Enum):
    singular = 0
    plural = 1
    
class Case(Enum):
    Nominative = 1
    Genitive = 2
    Dative = 3
    Accusative = 4
    Instrumental = 5
    Prepositional = 6
        
class Noun(DictionaryWord):
    def __init__(self, string: str, definition: str | list[str], stem: int | list[tuple[int, int]], animate: bool, gender: Gender, proper: bool, declination: int) -> None:
        super().__init__(string, definition)
        self._stem = stem
        self.animate = animate
        self.gender = gender
        self.proper = proper
        self.declination = declination
        
    @property
    def stem(self):
        if type(self._stem) == int:
            return self.string[:self._stem]
        else:
            #TODO: add support to the words with multiple endings
            raise(NotImplementedError)