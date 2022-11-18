import os
import time

HANGMAN_ASCII_ART = ("""  _    _                                         
 | |  | |                                        
 | |__| | __ _ _ __   __ _ _ __ ___   __ _ _ __  
 |  __  |/ _` | '_ \ / _` | '_ ` _ \ / _` | '_ \ 
 | |  | | (_| | | | | (_| | | | | | | (_| | | | |
 |_|  |_|\__,_|_| |_|\__, |_| |_| |_|\__,_|_| |_|
                      __/ |                      
                     |___/\n""")

MAX_TRIES = 6  

HANGMAN_PHOTOS = {1 : """    x-------x\n""",2 : """    x-------x
    |
    |
    |
    |
    |
\n""",3 : """    x-------x
    |
    |
    |
    |
    |

\n""",4 : """    x-------x
    |       |
    |       0
    |       |
    |
    |\n""",5 : """    x-------x
    |       |
    |       0
    |      /|\\
    |
    |\n""",6 : """    x-------x
    |       |
    |       0
    |      /|\\
    |      /
    |\n""",7 : """    x-------x
    |       |
    |       0
    |      /|\\
    |      / \\
    |\n"""}

# check if the path exist
def is_valid_path(path_from_user):
    return os.path.exists(path_from_user)

# check if the index is int and in range
def is_valid_index(index, words):
    if index.isalpha() == True:
        print("Please enter a number")
        return False
    else:
        return check_index_range(int(index), words)


def check_index_range(index, words):
    if index > len(words):
        print("Out og range")
        return False
    else:
        return True
    
# make a list from the text in the file   
def read_words_from_file(file_path):
    words = []
    with open (file_path,"r") as f:
        words = f.read().split()
    
    return words                


def print_hangman(num_of_tries):
    print(HANGMAN_PHOTOS[num_of_tries])


def clear_screen():
    time.sleep(1)
    os.system('cls')


def choose_secret_word(words, index):
    secret_word = words[index - 1]

    return secret_word

# check if the input from the user is a single letter
def is_valid_guessed_word(letter_guessed, old_letters_guessed):
    if (len(letter_guessed) > 1 or not letter_guessed.isalpha()):
        print("Invalid input")
        return False
    elif letter_guessed in old_letters_guessed:
        print("Letter already exist")
        print(*old_letters_guessed, sep=' -> ')
        clear_screen()
        return False        
    else:
        return True

# print the hidden word that the player needs to guess 
def show_hidden_word(secret_word, old_letters_guessed, secret_word_list):
    if not old_letters_guessed:
        print('\n')
        print("_ " * len(secret_word))
    else:    
        index_list = ([i for i, ltr in enumerate(secret_word) if ltr == old_letters_guessed[-1]])
        for i in range(len(index_list)):
            secret_word_list[index_list[i]] = old_letters_guessed[-1]

        print('\n')
        print(*secret_word_list) 

    return secret_word_list 
        

# add the last guess to the old guess list
def try_update_letter_guessed(letter_guessed, old_letters_guessed, secret_word, count_round, secret_word_list):   
    if letter_guessed not in secret_word:
        print("\nLetter not in word :(")
        print_hangman(count_round)
        old_letters_guessed.append(letter_guessed)
        clear_screen() 
        show_hidden_word(secret_word, old_letters_guessed, secret_word_list)
    else:    
        old_letters_guessed.append(letter_guessed)
        clear_screen()
        show_hidden_word(secret_word, old_letters_guessed, secret_word_list)    

    return old_letters_guessed 


# check if the player guess the whole word
def check_win(secret_word, old_letters_guessed):
    secret_word_list = [*secret_word]
    is_in_list = set(secret_word_list).issubset(old_letters_guessed)
    
    return is_in_list           
        

def run_game(letter_guessed_list):
    is_valid_path_check = False
    is_valid_index_check = False

    while is_valid_path_check == False:
        path_from_user = input("\nEnter file path: ")
        is_valid_path_check = is_valid_path(path_from_user)
    
    words_from_file = read_words_from_file(path_from_user)    

    while is_valid_index_check == False:   
        index_from_user = input("\nEnter index: ")
        is_valid_index_check = is_valid_index(index_from_user, words_from_file)

    clear_screen()
    # define the secret word to guess
    secret_word = choose_secret_word(words_from_file, int(index_from_user))
    secret_word_list = ['_'] * len(secret_word)
    print(*secret_word_list)
    count_round = 1
    is_winning = False
    # start to guess
    while count_round < 7 and is_winning == False:
        letter_from_user = input("\nGuess a letter: ")
        is_valid_guess = is_valid_guessed_word(letter_from_user, letter_guessed_list)   
        while is_valid_guess == False:
            letter_from_user = input("\nGuess a letter: ")
            is_valid_guess = is_valid_guessed_word(letter_from_user, letter_guessed_list)
            show_hidden_word(secret_word, letter_guessed_list, secret_word_list)   

        letter_guessed_list = try_update_letter_guessed(letter_from_user,letter_guessed_list, secret_word, count_round, secret_word_list)
        is_winning = check_win(secret_word, letter_guessed_list)
        count_round += 1
        
    
    clear_screen()
    if is_winning == True:
        print("\nYOU WON!!")
    else:
        print("\nLOSER!!")          


    
def main():
    letter_guessed_list = []
    print("WELCOME TO HANGMAN")
    print('\n')
    print(HANGMAN_ASCII_ART)
    print('\n')
    print("YOU HAVE", MAX_TRIES, "ROUNDS")
    clear_screen()
    run_game(letter_guessed_list)
    


if __name__ == "__main__":
    main()        