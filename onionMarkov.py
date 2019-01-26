# -*- coding: utf-8 -*-
"""
Created on Tue Jan 22 13:45:07 2019

DATA PRE-PROCESSING AND MARKOV MODEL

@author: Murphy
"""
import nltk as tk
from numpy.random import choice

# read in all text files to a string
unique_words = []
all_words = []
sentences = []

def loadText(filename):
    clean = ""
    with open(filename, "r",encoding='utf-8-sig') as f:
        for line in f:
            sentence = ""
            words = line.split()
            
            #pop off the date at the end of each line
            words.pop()
            words.pop()
            words.pop()
            
            #remove the links in each tweet
            for word in words:
                if "http" in word:
                    pass
                else:
                    sentence = sentence + word + " "
                    clean = clean + word + " "
            sentences.append(sentence)
    all_words.extend(clean.split())
    return clean

# LOAD AND PREPROCESS A DATA SET
loadText("economisttweets.txt")

#scan words to find number of distinct words
for word in all_words:
    if word in unique_words:
        n = 0
    else:
        unique_words.append(word)
        
p_start = [0.0] * len(unique_words)
num_unique_words = len(unique_words)

p_start_sum = 0
        
# find the start of each sentence and increase the count in p_start index
for sentence in sentences:
    words = sentence.split()
    start_word = words[0]
    start_word_index = unique_words.index(start_word)
    p_start[start_word_index] += 1
    p_start_sum += 1


# turn p_start into probabilities by dividing value by sum
index = 0
while (index < len(p_start)):
    p_start[index] /= p_start_sum
    index += 1
      
#calculate probabilities that each word is before another word
# for each row, count each time every word(column) appears after it in all words
# divide each column by the sum of each row
first_order_matrix = [[0.0 for x in range(num_unique_words)] for y in range(num_unique_words)] 
curr_word_index = 0

for word in all_words:
    row_index = unique_words.index(word)
    following_word_position = curr_word_index + 1
    if following_word_position < len(all_words):
        following_word = all_words[following_word_position]
    col_index = unique_words.index(following_word)
    first_order_matrix[row_index][col_index] += 1
    curr_word_index +=1 
 
for row in range(num_unique_words):
    row_sum = sum(first_order_matrix[row])
    for column in range(num_unique_words):
        first_order_matrix[row][column] /= row_sum
        
def get_first_word():
    return choice(unique_words, 1,
              p=p_start)
    
def choose_word(current_word):
    return (choice(unique_words, 1, p=first_order_matrix[unique_words.index(current_word)]))
    
def write_sentence(num_words):
    sentence = get_first_word()[0]
    curr_word = sentence
    for i in range(num_words - 1):
        new_word = choose_word(curr_word)[0]
        sentence = sentence + " " + new_word
        curr_word = new_word
    return sentence

def write_sentence_with(start_word, length):
    sentence = start_word
    curr_word = sentence
    for i in range(length - 1):
        new_word = choose_word(curr_word)[0]
        sentence = sentence + " " + new_word
        curr_word = new_word
    return sentence

def saveClean(filename):
    with open(filename, "w", encoding='utf-8-sig') as f:
        for line in sentences:
            f.write("%s\n" % line)

# GENERATE A HEADLINE
write_sentence(10)