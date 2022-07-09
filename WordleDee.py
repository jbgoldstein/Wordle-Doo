##################################
# App that manually plays Wordle
##################################

# Import necessary modules
import WordleGuesser as WG
from WDFunctions import evaluateLetters, eliminateLetters

# Instructions and Input
print("Instructions: Enter all guessed words separated by a space.")
print("Mark yellow letters with a question mark (?) following the letter.")
print("Mark green letters with an exclamation point (!) following the letter.")
print("For a starting word, input the word 'none'.")
word_input = input("Enter guessed words here:").lower()

guessed_words = word_input.lower().translate({ord("?"): None, ord("!"): None}).split(" ")

# Logic for when determining potential next guesses
if guessed_words[0] != "none":

    WordleDee = WG.WordleGuesser(word_input)

    # If letters are green or yellow, keep them in mind for later
    green_letters, yellow_letters = evaluateLetters(word_input)

    for letter in yellow_letters:
        WordleDee.addYellowLetter(letter[0], letter[1])

    for key in green_letters:
        index = int(key)
        if green_letters[index] != '.':
            WordleDee.addGreenLetter(green_letters[index], index)

    # If letter isn't green or yellow, then it shouldn't been in the word
    eliminated_letters = eliminateLetters(word_input, green_letters, yellow_letters)
    for letter in eliminated_letters:
            WordleDee.addEliminatedLetter(letter)

else:

    WordleDee = WG.WordleGuesser()

selected_word = WordleDee.guess()

# Input word and see results
print("Suggested Next Word: " + selected_word)