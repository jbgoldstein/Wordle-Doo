# Import necessary modules
import pandas as pd
import re
from wordfreq import zipf_frequency


def loadWordList():
    # Get list of potential words
    word_list = pd.read_csv("https://raw.githubusercontent.com/tabatkins/wordle-list/main/words", header=0,
                            names=["Potential Words"])

    # Check vowel count of each word
    word_list["Vowel Count"] = word_list["Potential Words"].apply(
        lambda word: len(set(re.findall(r'[aeiouy]', word.lower()))))

    # Get common use frequency of each word
    word_list["Usage Frequency"] = word_list["Potential Words"].apply(lambda word: zipf_frequency(word, 'en'))

    # Get number of unique letters in the word
    word_list["Unique Letters"] = word_list["Potential Words"].apply(lambda word: len(set(word)))

    return word_list


def evaluateLetters(word_input):
    green_letters = {1: '.', 2: '.', 3: '.', 4: '.', 5: '.'}
    yellow_letters = []

    # Set iterators to mark position in overall word input string
    pos_iter = 0
    # Set iterator to mark position in individual word
    word_iter = 0

    for letter in word_input:
        # If first letter in word, to prevent possibility of array out of bound error
        if pos_iter == 0:
            pos_iter += 1
            word_iter += 1
            continue
        # If a question mark is input, check the letter before it for a yellow letter
        if (letter == "?"):
            if (word_input[pos_iter - 1], word_iter) not in yellow_letters:
                yellow_letters.append((word_input[pos_iter - 1], word_iter))
        # If a exclaimation point is input, check the letter before it for a green letter and log position in word
        elif (letter == "!"):
            green_letters[word_iter] = word_input[pos_iter - 1]
        # Reset green letter position iterator when there is a new word
        elif letter == " ":
            word_iter = 0
        else:
            word_iter += 1
        pos_iter += 1

    return green_letters, yellow_letters


def eliminateLetters(word_input, green_letters, yellow_letters):
    eliminated_letters = []

    iter = 0

    # Loop through input words and find any letters that are not green or yellow so that they can be eliminated
    for letter in word_input:
        if letter not in green_letters.values() and letter not in ''.join(
                map(lambda letterTuple: letterTuple[0], yellow_letters)) and letter not in ['?', '!', ' ']:
            eliminated_letters.append(letter)

    return eliminated_letters
