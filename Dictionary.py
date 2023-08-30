import difflib

class Dictionary:
    def __init__(self, file_path: str) -> None:
        self.dictionary_list = dict(zip(list("абвгдеёжзийклмнопрстуфхцчшщъыьэюя"), [[]]*33))
        
        with open(file_path, "r") as dictionary_file:
            for dictionary_word in dictionary_file.readlines():
                self.dictionary_list[dictionary_word[0].lower()].append(dictionary_word.lower().removesuffix("\n"))
    
    @staticmethod
    def closest_dictionary_words(word: str, dictionary) -> list[str]:
        first_letter_dict = dictionary.dictionary_list[word[0]]
        cutoff = 0.6
        result = []
        s = difflib.SequenceMatcher()
        s.set_seq2(word)
        for x in first_letter_dict:
            s.set_seq1(x)
            if s.real_quick_ratio() >= cutoff and \
            s.quick_ratio() >= cutoff and \
            s.ratio() >= cutoff:
                result.append((s.ratio(), x))
        return [i[1] for i in sorted(result, key=lambda s: s[0], reverse=True)][0:4]
            
    def __call__(self):
        return self.dictionary_list
    
    def __repr__(self) -> str:
        return "\n".join(list(map(str, self.dictionary_list)))