######################################
# App that automatically plays Wordle
######################################

# Import necessary modules
from selenium import webdriver
from selenium.webdriver.common.by import By
import tkinter
import time

import WordleGuesser as WG

WordleDoo = WG.WordleGuesser()

guess_number = 1
has_won = False

driver = webdriver.Chrome(executable_path="C:/Users/Jack/Documents/chromedriver_win32/chromedriver.exe")
driver.get("https://www.nytimes.com/games/wordle/index.html")

# Click off popup on first run
driver.find_element(By.CLASS_NAME, "Modal-module_modalOverlay__81ZCi").click()

while guess_number <= 6 and has_won is not True:
    current_guess = WordleDoo.guess()

    for letter in current_guess:
        driver.find_element(By.XPATH, f"//button[@data-key='{letter}']").click()
        time.sleep(.2)

    driver.find_element(By.XPATH, "//button[@data-key='↵']").click()
    time.sleep(2)

    tile_list = driver.find_elements(By.CLASS_NAME, "Tile-module_tile__3ayIZ")

    number_correct = 0

    for tile in tile_list[(guess_number * 5) - 5:guess_number * 5]:

        index = tile_list.index(tile) % 5

        if tile.get_attribute("data-state") == "absent":
            WordleDoo.addEliminatedLetter(current_guess[index])

        if tile.get_attribute("data-state") == "present":
            WordleDoo.addYellowLetter(current_guess[index], index + 1)

        if tile.get_attribute("data-state") == "correct":
            number_correct += 1
            WordleDoo.addGreenLetter(current_guess[index], index + 1)

    if number_correct == 5:
        has_won = True
        time.sleep(5)
    else:
        WordleDoo.addGuessedWord(current_guess)
        guess_number += 1

if has_won is not True:
    print("Did not guess correct word.")
else:
    print(f"Guessed word {current_guess} in {guess_number} guesses.")

    driver.find_element(By.ID, "share-button").click()

    print(tkinter.Tk().clipboard_get())

driver.close()