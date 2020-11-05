# Problem Set 4C
# Name: <your name here>
# Collaborators:
# Time Spent: x:xx

import string
from ps4a import get_permutations
import random

### HELPER CODE ###
def load_words(file_name):
    print("Loading word list from file...")
    # inFile: file
    inFile = open(file_name, 'r')
    # wordlist: list of strings
    wordlist = []
    for line in inFile:
        wordlist.extend([word.lower() for word in line.split(' ')])
    print("  ", len(wordlist), "words loaded.")
    return wordlist

def is_word(word_list, word):

    word = word.lower()
    word = word.strip(" !@#$%^&*()-_+={}[]|\:;'<>?,./\"")
    return word in word_list


### END HELPER CODE ###

WORDLIST_FILENAME = 'words.txt'

# you may find these constants helpful
VOWELS_LOWER = 'aeiou'
VOWELS_UPPER = 'AEIOU'
CONSONANTS_LOWER = 'bcdfghjklmnpqrstvwxyz'
CONSONANTS_UPPER = 'BCDFGHJKLMNPQRSTVWXYZ'

class SubMessage(object):
    def __init__(self, text):
        self.message_text=text
        self.valid_words=load_words(WORDLIST_FILENAME)
       
    def get_message_text(self):
        return self.message_text
        
    def get_valid_words(self):
        valid_words_list=self.valid_words
        list_copy=valid_words_list.copy()
        return list_copy
                
    def build_transpose_dict(self, vowels_permutation):
        transpose_dict={}
        for i in range (0, len(VOWELS_LOWER)):
            vowel_lower_map={VOWELS_LOWER[i]:vowels_permutation[i]}
            transpose_dict.update(vowel_lower_map)
        vowels_permutation_upper=vowels_permutation.upper()
        for i in range (0, len(VOWELS_UPPER)):
            vowel_upper_map={VOWELS_UPPER[i]:vowels_permutation_upper[i]}
            transpose_dict.update(vowel_upper_map)
        for letter in CONSONANTS_LOWER:
            consonants_lower_map={letter:letter}
            transpose_dict.update(consonants_lower_map)
        for letter in CONSONANTS_UPPER:
            consonants_upper_map={letter:letter}
            transpose_dict.update(consonants_upper_map)
        return transpose_dict
    
    def apply_transpose(self, transpose_dict): 
        text=self.get_message_text()
        encrypted_letter_list=[]
        for letter in text:
            newletter=transpose_dict.get(letter)
            if newletter==None:
                encrypted_letter_list.append(letter)
            else:
                encrypted_letter_list.append(newletter)
        encrypted_message="".join(encrypted_letter_list)
        return encrypted_message

class EncryptedSubMessage(SubMessage):
    def __init__(self, text):
        SubMessage.__init__(self,text)

    def decrypt_message(self):
        permutations_list=get_permutations(VOWELS_LOWER)
        messages=[]
        message_validity=[]
        for permutation in permutations_list:
            number_of_valid_words=0
            transpose_dict=self.build_transpose_dict(permutation)
            decrypted_text=self.apply_transpose(transpose_dict)
            decrypted_text_list=decrypted_text.split()
            for word in decrypted_text_list:
                valid=is_word(self.get_valid_words(), word)
                if valid==True:
                    number_of_valid_words+=1
            messages.append(decrypted_text)
            message_validity.append(number_of_valid_words)
        best_index=message_validity.index(max(message_validity))
        decrypted_message=messages[best_index]
        return decrypted_message
            
#test case 
plain_text="Hello, World!"
permutations_list=get_permutations(VOWELS_LOWER)
index=random.randint(0, len(permutations_list))
permutation=permutations_list[index]
obj1=SubMessage(plain_text)
transpose_dict=obj1.build_transpose_dict(permutation)
encrypted_text=obj1.apply_transpose(transpose_dict)
print(encrypted_text)
obj2=EncryptedSubMessage(encrypted_text)
get_plain_text_back=obj2.decrypt_message()
print(get_plain_text_back)




