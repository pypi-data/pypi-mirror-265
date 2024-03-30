import json

#dictionary of words by dwyl at https://github.com/dwyl/english-words/tree/master
# open file and load words into a list
with open('words\words_alpha.txt', 'r') as words_file:
        words_list = words_file.readlines()
        words_list = [word.strip() for word in words_list]

# each word in the list has letters put in alphabetical order and is placed in a list in the dict
words_dict = {}
for word in words_list:
    alphabetical = ''.join(sorted(word.lower()))
    if alphabetical not in words_dict:
        words_dict[alphabetical] = [word]
    else:
         words_dict[alphabetical].append(word)

# export to .json
with open('words\words_dict.json', 'w') as dict_file:
     json.dump(words_dict, dict_file)