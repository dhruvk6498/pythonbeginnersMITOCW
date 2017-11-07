"""
    
    Author - Dhruv Kakran
    June 2017
    
    """





import random
import string

VOWELS = 'aeiou'
CONSONANTS = 'bcdfghjklmnpqrstvwxyz'
HAND_SIZE = 7

SCRABBLE_LETTER_VALUES = {
    'a': 1, 'b': 3, 'c': 3, 'd': 2, 'e': 1, 'f': 4, 'g': 2, 'h': 4, 'i': 1, 'j': 8, 'k': 5, 'l': 1, 'm': 3, 'n': 1, 'o': 1, 'p': 3, 'q': 10, 'r': 1, 's': 1, 't': 1, 'u': 1, 'v': 4, 'w': 4, 'x': 8, 'y': 4, 'z': 10
}

WORDLIST_FILENAME = "words.txt"

def load_words():
    """
    Returns a list of valid words. Words are strings of lowercase letters.
    
    Depending on the size of the word list, this function may
    take a while to finish.
    """
    print ("Loading word list from file...")
    # inFile: file
    inFile = open(WORDLIST_FILENAME, 'r')
    wordlist = []
    for line in inFile:
        wordlist.append(line.strip().lower())
    print ("  ", len(wordlist), "words loaded.")
    return wordlist

def get_frequency_dict(sequence):
    """
    Returns a dictionary where the keys are elements of the sequence
    and the values are integer counts, for the number of times that
    an element is repeated in the sequence.

    sequence: string or list
    return: dictionary
    """
    # freqs: dictionary (element_type -> int)
    freq = {}
    for x in sequence:
        freq[x] = freq.get(x,0) + 1
    return freq

def get_word_score(word, n):
    """
    Returns the score for a word. Assumes the word is a
    valid word.

    The score for a word is the sum of the points for letters
    in the word, plus 50 points if all n letters are used on
    the first go.

    Letters are scored as in Scrabble; A is worth 1, B is
    worth 3, C is worth 3, D is worth 2, E is worth 1, and so on.

    word: string (lowercase letters)
    returns: int >= 0
    """
    wordlist = load_words()
    wordscore = 0 
    for x in wordlist:
        if x == word:
            for i in word:
                wordscore += int(SCRABBLE_LETTER_VALUES[str(i)])
    if len(word) == n:
        wordscore += 50
    return wordscore

def display_hand(hand):
    """
    Displays the letters currently in the hand.

    For example:
       display_hand({'a':1, 'x':2, 'l':3, 'e':1})
    Should print out something like:
       a x x l l l e
    The order of the letters is unimportant.

    hand: dictionary (string -> int)
    """
    for letter in hand.keys():
        for j in range(hand[letter]):
            print (letter),             # print all on the same line
    print()                              # print an empty line

def deal_hand(n):
    """
    Returns a random hand containing n lowercase letters.
    At least n/3 the letters in the hand should be VOWELS.

    Hands are represented as dictionaries. The keys are
    letters and the values are the number of times the
    particular letter is repeated in that hand.

    n: int >= 0
    returns: dictionary (string -> int)
    """
    hand={}
    num_vowels = n // 3
    
    for i in range(num_vowels):
        x = VOWELS[random.randrange(0,len(VOWELS))]
        hand[x] = hand.get(x, 0) + 1
        
    for i in range(num_vowels, n):    
        x = CONSONANTS[random.randrange(0,len(CONSONANTS))]
        hand[x] = hand.get(x, 0) + 1
        
    return hand

def update_hand(hand, word):
    """
    Assumes that 'hand' has all the letters in word.
    In other words, this assumes that however many times
    a letter appears in 'word', 'hand' has at least as
    many of that letter in it. 

    Updates the hand: uses up the letters in the given word
    and returns the new hand, without those letters in it.

    Has no side effects: does not mutate hand.

    word: string
    hand: dictionary (string -> int)    
    returns: dictionary (string -> int)
    """
    newhand = {}
    for x in hand.keys():
        lettercount = 0
        lettercount = word.count(x)
        newhand[x] = int(hand[x]) - lettercount
    for key in newhand.copy().keys():
        if newhand[key] == 0:
            del newhand[key]
    print(newhand)
    return newhand

def is_valid_word(word, hand, word_list):
    """
    Returns True if word is in the word_list and is entirely
    composed of letters in the hand. Otherwise, returns False.
    Does not mutate hand or word_list.
    
    word: string
    hand: dictionary (string -> int)
    word_list: list of lowercase strings
    """
    isvalid = False
    handkeys = []
    for y in hand.keys():
        handkeys.append(str(y))
    for x in word_list:
        if x == word:
            for i in word:
                if i in handkeys and word.count(i) <= int(hand[i]):
                    isvalid = True
                else:
                    isvalid = False
                    break
    
    return isvalid


def play_hand(hand, word_list):
    """
    Allows the user to play the given hand, as follows:

    * The hand is displayed.
    
    * The user may input a word.

    * An invalid word is rejected, and a message is displayed asking
      the user to choose another word.

    * When a valid word is entered, it uses up letters from the hand.

    * After every valid word: the score for that word and the total
      score so far are displayed, the remaining letters in the hand 
      are displayed, and the user is asked to input another word.

    * The sum of the word scores is displayed when the hand finishes.

    * The hand finishes when there are no more unused letters.
      The user can also finish playing the hand by inputing a single
      period (the string '.') instead of a word.

    * The final score is displayed.

      hand: dictionary (string -> int)
      word_list: list of lowercase strings
    """
    display_hand(hand)
    word = str(input("Enter a word: "))
    is_valid = is_valid_word(word, hand, word_list)
    while is_valid == False:
        word = str(input("Word is invalid, please enter a different word: "))
        if word == ".":
            break
        
    is_valid = is_valid_word(word, hand, word_list)
    hand = update_hand(hand, word)
    n = HAND_SIZE
    totalscore = 0
    totalscore += get_word_score(word, n)
    print("Your score for this word: ", (get_word_score(word, n)))
    print("Your total score: ", totalscore)
    display_hand(hand)
    while bool(hand) != False:
        word = str(input("Enter another word for this hand ?"))
        if word == ".":
            break
        else:
            is_valid = is_valid_word(word, hand, word_list)
        while is_valid == False:
            word = str(input("Word is invalid, please enter a different word: "))
            is_valid = is_valid_word(word, hand, word_list)
            if word == ".":
                break
        if word == ".":
            break
        else:
            hand = update_hand(hand, word)
            totalscore += get_word_score(word, n)
            print("Your score for this word: ", (get_word_score(word, n)))
            print("Your total score: ", totalscore)
            display_hand(hand)


def play_game(word_list):
    """
    Allow the user to play an arbitrary number of hands.

    * Asks the user to input 'n' or 'r' or 'e'.

    * If the user inputs 'n', let the user play a new (random) hand.
      When done playing the hand, ask the 'n' or 'e' question again.

    * If the user inputs 'r', let the user play the last hand again.

    * If the user inputs 'e', exit the game.

    * If the user inputs anything else, ask them again.
    """
    
    hand = deal_hand(HAND_SIZE) # random init
    while True:
        cmd = str(input('Enter n to deal a new hand, r to replay the last hand, or e to end game: '))
        if cmd == 'n':
            hand = deal_hand(HAND_SIZE)
            play_hand(hand.copy(), word_list)
            print()
        elif cmd == 'r':
            play_hand(hand.copy(), word_list)
            print()
        elif cmd == 'e':
            break
        else:
            print ("Invalid command.")


if __name__ == '__main__':
    word_list = load_words()
    play_game(word_list)

        
        
        
        
        
        
    
    
        
    
    
    
              
    



    


            
                
        


            
    
    



