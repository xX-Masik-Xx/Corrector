#imports
from Text import Text
from CorrectionHandler import CorrectionHandler

if __name__ == "__main__":
    #input
    print("Введите текст:")
    input_text = Text(input())
    
    #Instance of CorrectionHandler:
    CorrectionHandler(input_text)