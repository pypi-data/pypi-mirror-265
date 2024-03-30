from pyggle.boggle import Boggle
from pyggle.functions import time

if __name__ == "__main__":

    with open("data/word_list_3000.txt", "r") as f:
       all_words = [word.strip() for word in f] 

    boggle = Boggle("aqa dsf", None, True)
    boggle2 = Boggle("ea st")

    boggle.print_result()
