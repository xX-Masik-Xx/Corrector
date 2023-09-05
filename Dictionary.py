import difflib

class Dictionary:
    def __init__(self, file_path: str) -> None:
        self.dictionary_list = dict(zip(list("абвгдеёжзийклмнопрстуфхцчшщъыьэюя"), [[]]*33))
        
        with open(file_path, "r") as dictionary_file:
            for dictionary_word in dictionary_file.readlines():
                self.dictionary_list[dictionary_word[0].lower()].append(dictionary_word.lower().removesuffix("\n"))
            
    def __call__(self):
        return self.dictionary_list
    
    def __repr__(self) -> str:
        return "\n".join(list(map(str, self.dictionary_list)))