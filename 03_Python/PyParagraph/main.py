"Analysis of text file"
import os
import string
import re

#from collectons import Counter

path = os.path.join("..", "Resources", "paragraph_1.txt")
NoWords, NoSent, letters = 0, 0, 0

with open (path, "r") as TextToAnalyze:
    text = TextToAnalyze.read()
    # Split text by "., !, ? followed by space"
    sent_split = re.split("(?<=[.!?]) +", text)
    
    for sent in sent_split:
        if (sent != ""):
            NoSent +=1
    
    # Split text by spaces, calculate number of words and number of letters (isalpha function removes punctuation)
    words = text.split()
    for word in words:
        NoWords +=1
        for char in word:
            if char.isalpha():
                letters +=1

print ("Paragraph Analysis")
print ("-"*30)
print (f'Approximate word count: {NoWords}')
print (f'Approximate sentence count: {NoSent}')
print (f'Approximate letter count: {letters}')
print (f'Average sentence length: {letters/NoWords:.2f}')