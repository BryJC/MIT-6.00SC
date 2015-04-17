from ps3a import *
import time
from perm import *


#
#
# Problem #6A: Computer chooses a word
#
#
def comp_choose_word(hand, word_list):
    chosen = [None, 0]
    length = sum(hand.values())
    for n in xrange(length, 0, -1):
        #print 'cycle {}'.format(n)
        possibilities = get_perms(hand, n)
        #print possibilities
        for word in possibilities:
            if word in word_list:
                score = get_word_score(word, n)
                if score > chosen[1]:
                    chosen = [word, score]
    return chosen[0]
    
    """
	Given a hand and a word_dict, find the word that gives the maximum value score, and return it.
   	This word should be calculated by considering all possible permutations of lengths 1 to HAND_SIZE.

    hand: dictionary (string -> int)
    word_list: list (string)
    """
    # TO DO...

#
# Problem #6B: Computer plays a hand
#
def comp_play_hand(hand, word_list):    
    hand_total = 0
    orig_len = calculate_handlen(hand)
    while calculate_handlen(hand) > 0:        
        print "Current hand: "
        display_hand(hand)
        #print hand
        word = comp_choose_word(hand, word_list)
        print word
        if word == None:
            print "Final score is {}\n".format(hand_total)
            return
        else:
            hand_total += get_word_score(word, orig_len)
            print "'{}' earned {} points. Total = {} points\n".format(
                    word, get_word_score(word, orig_len), hand_total)
            hand = update_hand(hand, word)
    print "Out of letters. Final score is {}\n".format(hand_total)
    """
     Allows the computer to play the given hand, as follows:

     * The hand is displayed.

     * The computer chooses a word using comp_choose_words(hand, word_dict).

     * After every valid word: the score for that word is displayed, 
       the remaining letters in the hand are displayed, and the computer 
       chooses another word.

     * The sum of the word scores is displayed when the hand finishes.

     * The hand finishes when the computer has exhausted its possible choices (i.e. comp_play_hand returns None).

     hand: dictionary (string -> int)
     word_list: list (string)
    """
    # TO DO ...    
    
#
# Problem #6C: Playing a game
#
#
def play_game(word_list, n=HAND_SIZE):
    while True:
        ask = raw_input("Time to play a word game!\n"\
                        "Would you like to play a (n)ew hand, (r)edo, or (e)xit? ")
        if ask.lower() == 'n':
            hand = deal_hand(n)
            who_plays = raw_input("(u)ser or (p)rogram to play the hand? ")
            if who_plays == 'u':
                play_hand(hand.copy(), word_list)
            elif who_plays == 'p':
                comp_play_hand(hand.copy(), word_list)
        elif ask.lower() == 'r':
            who_plays = raw_input("(u)ser or (p)rogram to play the hand? ")
            if who_plays == 'u':
                play_hand(hand.copy(), word_list)
            elif who_plays == 'p':
                comp_play_hand(hand.copy(), word_list)            
        elif ask.lower() == 'e':
            break
        else:
            return play_game(word_list)
    """Allow the user to play an arbitrary number of hands.

    1) Asks the user to input 'n' or 'r' or 'e'.
    * If the user inputs 'n', play a new (random) hand.
    * If the user inputs 'r', play the last hand again.
    * If the user inputs 'e', exit the game.
    * If the user inputs anything else, ask them again.

    2) Ask the user to input a 'u' or a 'c'.
    * If the user inputs 'u', let the user play the game as before using play_hand.
    * If the user inputs 'c', let the computer play the game using comp_play_hand (created above).
    * If the user inputs anything else, ask them again.

    3) After the computer or user has played the hand, repeat from step 1

    word_list: list (string)
    """
    # TO DO...
        
#
# Build data structures used for entire session and play game
#
if __name__ == '__main__':
    word_list = load_words()
    play_game(word_list)

    
