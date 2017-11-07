
"""
    
    Author - Dhruv Kakran
    June 2017
    
    """


import random
import string
import time 

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
    wordscore = 0 
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
            print (letter,end = " ")            # print all on the same line
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

def is_valid_word(word, hand, points_dict):
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
    if word != ".":
        if points_dict[word]:
            for i in word:
                if i in handkeys and word.count(i) <= int(hand[i]):
                    isvalid = True
                else:
                    isvalid = False
                    break
    else:
        isvalid = False
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
    #limit = int(input("Enter time limit (in seconds) for players : "))
    points_dict = get_words_to_points(word_list)
    limit = get_time_limit(points_dict, 1)
    print("The hand is: ")
    hand = deal_hand(HAND_SIZE)
    display_hand(hand)
    total_hand_time = 0 
    start_time = time.time()
    #word = str(input("Enter a word: "))
    word = pick_best_word(hand, points_dict)
    print(word)
    is_valid = is_valid_word(word, hand, points_dict)
    while is_valid == False and word != ".":
        word = str(input("Word is invalid, please enter a different word: "))
        is_valid = is_valid_word(word, hand, points_dict)
    if word == ".":
        return
    end_time = time.time()
    hand = update_hand(hand, word)
    n = HAND_SIZE
    word_time = end_time - start_time 
    total_hand_time += end_time - start_time
    timer = round(limit - total_hand_time, 2)
    if timer < 0:
        print("Sorry, your time is up.")
        return
    print("It took %0.2f seconds to provide an answer" % word_time)
    print("You have %0.2f seconds left" % timer)
    totalscore = 0
    totalscore += float(get_word_score(word, n) / word_time) 
    print("Your score for this word: ", round((get_word_score(word, n) / word_time),2))
    print("Your total score: ", round(totalscore,2))
    print("The hand is: ")
    display_hand(hand)
    while bool(hand) != False:
        start_time = time.time()
        """word = str(input("Enter another word for this hand ? "))"""
        word = pick_best_word(hand, points_dict)
        is_valid = is_valid_word(word, hand, points_dict)
        if word == ".":
            return
        while is_valid == False:
            word = str(input("Word is invalid, please enter a different word: "))
            is_valid = is_valid_word(word, hand, points_dict)
            if word == ".":
                return
        end_time = time.time()
        word_time = end_time - start_time 
        total_hand_time += end_time - start_time 
        timer = round(limit - total_hand_time, 2)
        if timer < 0:
            print("Sorry, your time is up. Your final score is : ", totalscore)
            return
        else:
            print("It took %0.2f seconds to provide an answer" % word_time)
            print("You have %0.2f seconds left" % timer)
            hand = update_hand(hand, word)
            totalscore += float(get_word_score(word, n) / word_time)
            print("Your score for this word: ", round((get_word_score(word, n) / word_time),2))
            print("Your total score: ", round(totalscore,2))
            if len(hand) != 0:
                print("The hand is: ")
                display_hand(hand)
            else:
                print("All done!")
    print("FINAL SCORE: ", round(totalscore,2)) 


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

def pick_best_word(hand , points_dict):
    """Return the
       highest scoring word from points_dict that can be made with the
       given hand.
       Return '.' if no words can be made with the given hand."""
    hand_words = {}
    for x in points_dict.keys():
        if is_valid_word(x,hand,points_dict):
            hand_words[x] = int(points_dict[x])
    if bool(hand_words):
        return max(hand_words, key = hand_words.get)
    else:
        return "."

#def get_word_rearrangements(word_list, hand):
    
    
    

#def pick_best_word_faster(hand, rearrange_dict):

        
    




def get_words_to_points(word_list):
    points_dict = {}
    wordscore = 0 
    for word in word_list:
        wordscore = get_word_score(word, 7)
        points_dict[word] = wordscore
    return points_dict

def get_time_limit(points_dict, k):
    start_time = time.time()
    for word in points_dict:
        get_frequency_dict(word)
        get_word_score(word, HAND_SIZE)
    end_time = time.time()
    return (end_time - start_time) * k 
    


if __name__ == '__main__':
    word_list = load_words()
    play_game(word_list)

        
        
        
        
        
        
    
    
        
    
    
    
              
    



    


            
                
        


            
    
    



