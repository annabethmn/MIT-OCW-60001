# Problem Set 2, hangman.py
# Name: 
# Collaborators:
# Time spent:

# Hangman Game
# -----------------------------------
# Helper code
# You don't need to understand this helper code,
# but you will have to know how to use the functions
# (so be sure to read the docstrings!)
import random
import string

WORDLIST_FILENAME = "words.txt"


def load_words():
    """
    Returns a list of valid words. Words are strings of lowercase letters.
    
    Depending on the size of the word list, this function may
    take a while to finish.
    """
    print("Loading word list from file...")
    # inFile: file
    inFile = open(WORDLIST_FILENAME, 'r')
    # line: string
    line = inFile.readline()
    # wordlist: list of strings
    wordlist = line.split()
    print("  ", len(wordlist), "words loaded.")
    return wordlist



def choose_word(wordlist):
    """
    wordlist (list): list of words (strings)
    
    Returns a word from wordlist at random
    """
    return random.choice(wordlist)

# end of helper code

# -----------------------------------

# Load the list of words into the variable wordlist
# so that it can be accessed from anywhere in the program
wordlist = load_words()

def get_man_drawing(remaining_guesses):
    """
    Returns a string drawing of hangman based on number of wrong guesses
    This function was not included in the original problem set- I added it for fun
    """
    guess_1= "----------------" + "\n" + " | " + "\n" + " O "
    guess_2= guess_1 + "\n" + "\| "
    guess_3= guess_1 + "\n" + "\|/ "
    guess_4= guess_3 + "\n" + " | "
    guess_5= guess_4 + "\n" + "/ "
    guess_6=guess_4 + "\n" + "/ \ " 
    if remaining_guesses==5:
        man=guess_1
    elif remaining_guesses==4:
        man=guess_2
    elif remaining_guesses==3:
        man=guess_3
    elif remaining_guesses==2:
        man=guess_4
    elif remaining_guesses==1:
        man=guess_5
    else:
        man=guess_6
    return man

def is_word_guessed(secret_word, letters_guessed):
    '''
    secret_word: string, the word the user is guessing; assumes all letters are
      lowercase
    letters_guessed: list (of letters), which letters have been guessed so far;
      assumes that all letters are lowercase
    returns: boolean, True if all the letters of secret_word are in letters_guessed;
      False otherwise
    '''
    #check each letter of the secret word against guessed letters
    for char in secret_word:
        num=letters_guessed.count(char) 
        if num==0:
            return False #if any of the letters haven't been guessed
    return True



def get_guessed_word(secret_word, letters_guessed):
    '''
    secret_word: string, the word the user is guessing
    letters_guessed: list (of letters), which letters have been guessed so far
    returns: string, comprised of letters, underscores (_), and spaces that represents
      which letters in secret_word have been guessed so far.
    '''
    current_guess= ""
    for char in secret_word:
        num=letters_guessed.count(char)
        if num!=0:
            current_guess+=char #fill in the character if it has been guessed
        else:
            current_guess+="_ "
    return current_guess



def get_available_letters(letters_guessed):
    '''
    letters_guessed: list (of letters), which letters have been guessed so far
    returns: string (of letters), comprised of letters that represents which letters have not
      yet been guessed.
    '''
    abc=string.ascii_lowercase
    for s in letters_guessed:
        for char in s:
            abc=abc.replace(char, "") #remove letters from the alphabet that have already been guessed
    return abc
    
    
def check_warnings(guess, letters_guessed):
    '''
    Helper function I added to check if the guess counts against warnings
    Guess: character inputted by user
    returns: True if the guess gets a warning, False if it counts against number of guesses
    '''
    available_letters=get_available_letters(letters_guessed)
    #if guess is not in the alphabet, deduct a warning
    if not str.isalpha(guess): 
        return True
    #if guess is in letters already guessed, deduct a warning
    for char in guess: 
        is_guessed=available_letters.count(char)
        if is_guessed==0:
            return True
    return False

def is_guess_correct(guess, secret_word):
    '''
    Helper function I wrote that checks if the letter guessed is in the secret word
    Returns: True if guess is in the secret word, False otherwise
    '''
    for char in guess:
        number=secret_word.count(char)
        if number==0:
            return False
    return True

def hangman(secret_word):
    '''
    secret_word: string, the secret word to guess.
    
    Starts up an interactive game of Hangman.
    
    * At the start of the game, let the user know how many 
      letters the secret_word contains and how many guesses s/he starts with.
      
    * The user should start with 6 guesses

    * Before each round, you should display to the user how many guesses
      s/he has left and the letters that the user has not yet guessed.
    
    * Ask the user to supply one guess per round. Remember to make
      sure that the user puts in a letter!
    
    * The user should receive feedback immediately after each guess 
      about whether their guess appears in the computer's word.

    * After each guess, you should display to the user the 
      partially guessed word so far.
    
    Follows the other limitations detailed in the problem write-up.
    '''
    print("Welcome to the game hangman! \n I am thinking of a word that is", len(secret_word), "letters long. \n You have 3 warnings and 6 guesses left. \n Available letters:", string.ascii_lowercase )
    remaining_guesses=6
    remaining_warnings=3
    letters_guessed=[]
    while remaining_guesses>0: #end game after running out of guesses
        guess=input("Guess a letter...")
        guess=str.lower(guess)
        if check_warnings(guess, letters_guessed):
            print("Oops!Guesses must be letters that you have not already guessed.")
            if remaining_warnings>0:
                remaining_warnings-=1
            else:
                remaining_guesses-=1
            print("Warnings:",remaining_warnings)
            print("Guesses:", remaining_guesses)
            continue
        else:
            letters_guessed+=guess
        if is_guess_correct(guess,secret_word):
            print("Good guess")
        else: 
            remaining_guesses-=1
            print(get_man_drawing(remaining_guesses))
        print (get_guessed_word(secret_word,letters_guessed))
        print ("Available letters:",get_available_letters(letters_guessed))
        print ("Guesses:",remaining_guesses, "\n Warnings:", remaining_warnings)
        if is_word_guessed(secret_word,letters_guessed)==True:
            msg=print("Congratulations! You guessed the word.The word is", secret_word)
            break
    if is_word_guessed(secret_word, letters_guessed)==False:
            msg=print("Sorry!You lost. The word is", secret_word)
    return msg    
    



# When you've completed your hangman function, scroll down to the bottom
# of the file and uncomment the first two lines to test
#(hint: you might want to pick your own
# secret_word while you're doing your own testing)


# -----------------------------------



def match_with_gaps(my_word, other_word):
    '''
    my_word: string with _ characters, current guess of secret word
    other_word: string, regular English word
    returns: boolean, True if all the actual letters of my_word match the 
        corresponding letters of other_word, or the letter is the special symbol
        _ , and my_word and other_word are of the same length;
        False otherwise: 
    '''
    #remove whitespace
    my_word= my_word.replace(" ", "")
    other_word=other_word.strip()
    if len(my_word)!=len(other_word): 
        return False
    #check equality letter by letter
    for i in range(len(my_word)):
        char1=my_word[i]
        char2=other_word[i]
        if char1!=char2 and char1!="_": 
            return False #if any 2 letters at same index don't match
        if char2 in my_word and char1 == "_":
            return False #if a letter has already been guessed, it cannot be one of the hidden letters
    return True


def show_possible_matches(my_word):
    '''
    my_word: string with _ characters, current guess of secret word
    returns: nothing, but should print out every word in wordlist that matches my_word
             Keep in mind that in hangman when a letter is guessed, all the positions
             at which that letter occurs in the secret word are revealed.
             Therefore, the hidden letter(_ ) cannot be one of the letters in the word
             that has already been revealed.

    '''
    myword=my_word.replace(" ", "") #remove whitespace
    match=[]
    for word in wordlist: #check entire word list for matches
        if match_with_gaps(myword,word)==True:
            match.append(word)
    if len(match)==0:
        print("No matches found")
    else:
        matches = " ".join(match)#build a string of all matches separated by spaces
        print(matches)
    
def check_warnings_hints(guess, letters_guessed):
    '''
    Modification of check_warnings helper function that allows wildcard
    See docstring for check_warnings
    '''
    available_letters=get_available_letters(letters_guessed)
    if guess=="*":
        return False
    if str.isalpha(guess)==False:
        return True
    is_guessed=available_letters.count(guess)
    if is_guessed==0:
        return True
    return False
    
def hangman_with_hints(secret_word):
    '''
    secret_word: string, the secret word to guess.
    
    Starts up an interactive game of Hangman.
    
    * At the start of the game, let the user know how many 
      letters the secret_word contains and how many guesses s/he starts with.
      
    * The user should start with 6 guesses
    
    * Before each round, you should display to the user how many guesses
      s/he has left and the letters that the user has not yet guessed.
    
    * Ask the user to supply one guess per round. Make sure to check that the user guesses a letter
      
    * The user should receive feedback immediately after each guess 
      about whether their guess appears in the computer's word.

    * After each guess, you should display to the user the 
      partially guessed word so far.
      
    * If the guess is the symbol *, print out all words in wordlist that
      matches the current guessed word. 
    
    Follows the other limitations detailed in the problem write-up.
    '''
    print("Welcome to the game hangman! \n I am thinking of a word that is", len(secret_word), "letters long. \n You have 3 warnings and 6 guesses left. \n Available letters:", string.ascii_lowercase, "\n If you would like a hint, type * for guess")
    remaining_guesses=6
    remaining_warnings=3
    letters_guessed=[]
    while remaining_guesses>0:
        guess=input("Guess a letter...")
        guess=str.lower(guess)
        if check_warnings_hints(guess, letters_guessed):
            print("Oops!Guesses must be letters that you have not already guessed.")
            if remaining_warnings>0:
                remaining_warnings-=1
            else:
                remaining_guesses-=1
            print("Warnings:",remaining_warnings)
            print("Guesses:", remaining_guesses)
            continue
        elif guess=="*":
            #when user inputs a wildcard, show matches to their current guesses
            guessedword=get_guessed_word(secret_word,letters_guessed)
            show_possible_matches(guessedword)
        else:
            letters_guessed+=guess
        vowels="aeiou"
        is_vowel=vowels.count(guess)
        if is_guess_correct(guess,secret_word):
            print("Good guess")
        elif not is_guess_correct(guess,secret_word) and is_vowel>0:
            remaining_guesses-=2
            print(get_man_drawing(remaining_guesses))
        elif guess=="*":
            remaining_guesses-=0
        else: 
            remaining_guesses-=1
            print(get_man_drawing(remaining_guesses))
        print (get_guessed_word(secret_word,letters_guessed))
        print ("Available letters:",get_available_letters(letters_guessed))
        print ("Guesses:",remaining_guesses, "\n Warnings:", remaining_warnings)
        if is_word_guessed(secret_word,letters_guessed)==True:
            msg=print("Congratulations! You guessed the word.The word is", secret_word)
            break
    if is_word_guessed(secret_word, letters_guessed)==False:
            msg=print("Sorry!You lost. The word is", secret_word)
    return msg        



# When you've completed your hangman_with_hint function, comment the two similar
# lines above that were used to run the hangman function, and then uncomment
# these two lines and run this file to test!
# Hint: You might want to pick your own secret_word while you're testing.


if __name__ == "__main__":
    # pass

    # To test part 2, comment out the pass line above and
    # uncomment the following two lines.
    
##    secret_word = choose_word(wordlist)
##    hangman(secret_word)

###############
    
    # To test part 3 re-comment out the above lines and 
    # uncomment the following two lines. 
    
    secret_word = choose_word(wordlist)
    hangman_with_hints(secret_word)
