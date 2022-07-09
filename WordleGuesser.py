# Import necessary modules
import pandas as pd
import re
from wordfreq import zipf_frequency
from random import choices


class WordleGuesser:

    def __init__(self, initial_guess=''):

        self.word_input = initial_guess
        self.guessed_words = initial_guess.lower().translate({ord("?"): None, ord("!"): None}).split(" ")

        self.word_list = self.loadWordList()
        self.word_list = self.word_list[~self.word_list["Potential Words"].isin(self.guessed_words)]

        self.green_letters = {1: '.', 2: '.', 3: '.', 4: '.', 5: '.'}
        self.yellow_letters = []
        self.eliminated_letters = []

    def loadWordList(self):

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

    def addGuessedWord(self, guessed_word):

        self.guessed_words.append(guessed_word)

        # If a word has already been guessed, eliminate the possibility
        self.word_list = self.word_list[~self.word_list["Potential Words"].isin(self.guessed_words)]

    def addEliminatedLetter(self, elim_letter):

        self.eliminated_letters.append(elim_letter)

        self.word_list = self.word_list[self.word_list["Potential Words"].apply(
            lambda word: 1 not in [letter in word for letter in self.eliminated_letters])]

    def addYellowLetter(self, yellow_letter, pos):

        self.yellow_letters.append((yellow_letter, pos))

        self.word_list = self.word_list[self.word_list["Potential Words"].apply(
            lambda word: 0 not in [letterTuple[0] in word for letterTuple in self.yellow_letters] and 1 not in [
                letterTuple[0] in word[letterTuple[1] - 1] for letterTuple in self.yellow_letters])]

    def addGreenLetter(self, green_letter, pos):

        self.green_letters[pos] = green_letter

        self.word_list = self.word_list[self.word_list["Potential Words"].apply(
            lambda word: re.match(''.join(self.green_letters.values()), word) is not None)]

    def guess(self):

        # Prioritize common words. If stumped, use any word that comes to mind
        if self.word_list["Potential Words"].size > 10:
            most_common_words = self.word_list.sort_values(by=["Usage Frequency", "Vowel Count"],
                                                                    ascending=False).head(
                round(self.word_list["Potential Words"].size * .10))
        # Eliminate any completely unused words
        else:
            most_common_words = self.word_list[
                self.word_list["Usage Frequency"].apply(
                    lambda frequency_value: frequency_value != 0.00)].sort_values(
                by=["Usage Frequency", "Vowel Count"], ascending=False)

        # Prioritize unique letters in early guesses
        if self.guessed_words[0] == "none" or len(self.guessed_words) < 3:
            unique_letters = most_common_words[most_common_words["Unique Letters"].apply(
                lambda unique_letter_value: unique_letter_value == most_common_words["Unique Letters"].max())]
        else:
            unique_letters = most_common_words

        # Prioritize using more vowels in early guesses
        if self.guessed_words[0] == "none" or len(self.guessed_words) < 3:
            final_list = unique_letters[unique_letters["Vowel Count"].apply(
                lambda vowel_count_value: vowel_count_value == unique_letters["Vowel Count"].max()
                                          or vowel_count_value == unique_letters["Vowel Count"].max() - 1)]
        else:
            final_list = unique_letters

        # With list of potential options in mind, randomly pick from options to take your guess
        # Adjusted random select to prioritize common words
        selected_word = choices(list(final_list["Potential Words"]), weights=list(final_list["Usage Frequency"]), k=1)[
            0]

        return selected_word
