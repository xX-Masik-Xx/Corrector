from Text import Text
from CorrectionHandler import CorrectionHandler

if __name__ == "__main__":
    #input
    print("Введите текст:")
    input_text = Text(input())
    
    #Экземпляр CorrectionHandler:
    CorrectionHandler(input_text)