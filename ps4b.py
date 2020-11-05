# Problem Set 4B
# Name: <your name here>
# Collaborators:
# Time Spent: x:xx

import string

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

def get_story_string():
   
    f = open("story.txt", "r")
    story = str(f.read())
    f.close()
    return story

### END HELPER CODE ###

WORDLIST_FILENAME = 'words_ps4.txt'
word_list=load_words(WORDLIST_FILENAME)

class Message(object):
    def __init__(self, text):
    
        self.message_text=text
    def get_message_text(self):
        return self.message_text

    def get_valid_words(self):
        wordlist=self.valid_words
        list_copy=wordlist.copy()
        return list_copy
        
    def build_shift_dict(self, shift):
        uppercase_letters=2*string.ascii_uppercase 
        lowercase_letters=2*string.ascii_lowercase
        dict={}
        for i in range (0, 26):
            letter_pair_upper={uppercase_letters[i]:uppercase_letters[i+shift]}
            letter_pair_lower={lowercase_letters[i]:lowercase_letters[i+shift]}
            dict.update(letter_pair_upper)
            dict.update (letter_pair_lower)
        return dict          
    def apply_shift(self,shift):
        text=self.get_message_text()
        shiftdict=self.build_shift_dict(shift)
        encrypted_letter_list=[]
        for char in text:
            if char.isalpha()==True:
                newchar=shiftdict.get(char)
                encrypted_letter_list.append(newchar)
            else:
                encrypted_letter_list.append(char)
        emptystring=""
        encrypted_text=emptystring.join(encrypted_letter_list)
        return encrypted_text
class PlaintextMessage(Message):
    def __init__(self, text, shift):
        Message.__init__(self,text)
        self.shift=shift
        self.encryption_dict=self.build_shift_dict(shift)
        self.message_text_encrypted=self.apply_shift(shift)

    def get_shift(self):
        return self.shift

    def get_encryption_dict(self):
        dict=self.encryption_dict.copy()
        return dict
    def get_message_text_encrypted(self):
        return self.message_text_encrypted

    def change_shift(self, shift):
        self.shift=shift
        self.encryption_dict=self.build_shift_dict(shift)
        self.message_text_encrypted=self.apply_shift(shift)
        
class CiphertextMessage(Message):
    def __init__(self, text):
        Message.__init__(self,text)
        
    def decrypt_message(self):
        message_validity=[]
        messages=[]
        for i in range (0,26):
            shift_message=self.apply_shift(i)
            valid_words=0
            shift_message_list=shift_message.split()
            for word in shift_message_list:
                if (is_word(word_list,word)==True):
                    valid_words+=1
            message_validity.append(valid_words)
            messages.append(shift_message)
        best_index=message_validity.index(max(message_validity))
        decrypted_message=messages[best_index]
        tup=(decrypted_message, 26-best_index)
        return tup

#begin test case 
plain_text="my pet rat is a very good boy"
obj1=PlaintextMessage(plain_text, 1)
encrypted_text=obj1.get_message_text_encrypted()
obj2=CiphertextMessage(encrypted_text)
get_plain_text_back=obj2.decrypt_message()
print(encrypted_text)
print(get_plain_text_back)




