# 6.00 Problem Set 3
# 
# Hangman
#


# -----------------------------------
# Helper code
# (you don't need to understand this helper code)
import random
import string

WORDLIST_FILENAME = "words.txt"

def load_words():
    """
    Returns a list of valid words. Words are strings of lowercase letters.
    
    Depending on the size of the word list, this function may
    take a while to finish.
    """
    print "Loading word list from file..."
    # inFile: file
    inFile = open(WORDLIST_FILENAME, 'r', 0)
    # line: string
    line = inFile.readline()
    # wordlist: list of strings
    wordlist = string.split(line)
    print "  ", len(wordlist), "words loaded."
    return wordlist

def choose_word(wordlist):
    """
    wordlist (list): list of words (strings)

    Returns a word from wordlist at random
    """
    return random.choice(wordlist)

# end of helper code
# -----------------------------------

# actually load the dictionary of words and point to it with 
# the wordlist variable so that it can be accessed from anywhere
# in the program
wordlist = load_words()

# your code begins here!

word = list(choose_word(wordlist))
guesses = len(word) + 5
unfilled = list("_" * len(word))
letters = list("abcdefghijklmnopqrstuvwxyz")
print "Welcome to the game, Hangman!\n"\
      "I am thinking of a word that is {} letters long.\n".format(len(word))
def hangman():
    global word
    global guesses
    global unfilled
    if '_' in unfilled and guesses == 0:
        print "Sorry, you lose! The word was '{}'\n".format(''.join(word))
        return unfilled
    if '_' not in unfilled and guesses >= 0:
        print "Congrats, you won! The word is '{}'\n".format(''.join(word))
        return unfilled
    else:
        print "You have {} guesses left.\n"\
              "Available letters: {}\n".format(guesses, ''.join(letters))
        choice = raw_input("Please guess a letter: ")
        if len(choice) != 1:
            print "Only one character at a time! Try again!"
            return hangman()
        if choice not in letters:
            print "{} already guessed, try again.".format(choice)
            return hangman()
        if choice.lower() in word:
            letters.remove(choice)
            for spot, item in enumerate(word):
                if item == choice:
                    unfilled[spot] = choice.lower()
            print "Good guess: {}".format(' '.join(unfilled))
            return hangman()
        elif choice.lower() not in word:
            guesses -= 1
            letters.remove(choice)
            print "{} not in this word: {}".format(choice, ' '.join(unfilled))
            return hangman()   
    return "Finished!"    
hangman()
