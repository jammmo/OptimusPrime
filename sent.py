
# coding: utf-8

# 1. determine if sentence is negative (d)
#     - use POS Tagging for each word
#     - get POS tag
#     - check the negative sentiment score based off the pos
#     - return the relevant words to be cross referenced in the database
# 2. find relevant quotes
#     - find quotes that are similiar to sentence
#         - find synonyms of the sentence (d)
#         - find quotes that have synonyms or words from sentence
#         - return the quotes
# 3. Use the TDIDF to find the most meaningful words in a sentence.
#4. Discouraging quotes
#    - If "I" in sentence and negative word in sentence and negative word is a verb

import nltk
#nltk.download('sentiwordnet')
from nltk.corpus import sentiwordnet as swn
from nltk.corpus import wordnet
import nltk
from nltk.corpus import stopwords
import random
import speakmywords
import sys

def get_negs(sentence):
    """Gets the negative words in a sentence.
    
    Parameters
    ----------
    sentence    string: String of words.
    
    Returns
    -------
    neg_list    list: List of negative words.
    """

    barred = ['fuck','fucking']
    stop_words = set(stopwords.words('english'))
    sent_list = sentence.split(' ')
    
    neg_list = []
    
    #load negative word data
    f = open('negative_words.txt')
    neg_db = f.readlines()
    neg_db = [w.strip() for w in neg_db]
    f.close()

    #check if any words are in 
    for word in sent_list:
        if (word not in barred) and (word not in stop_words) and (word in neg_db):
            neg_list.append(word)

    return list(set(neg_list))

def is_discourage(sentence):
    """Checks if a sentence should be discouraged.
    
    Parameters
    ----------  
    sentence    list: Sentence that will be analyzed.
    
    Returns
    -------
    discourage   bool: Wether it should be discouraged.
    """
    print(sentence)        
    sent_list = [s.lower() for s in sentence]
    negs = get_negs(' '.join(sentence))
    discourage = False          #initialize discourage to false
    tags = nltk.pos_tag(sentence)
    print(tags)
    
    #If "I" in sentence and negative word in 
    #sentence and negative word is a verb
    #Possibly swap this functin out for Jaime's
    if 'i' in sent_list and len(negs) > 0:
        for t in tags:
            pos_tag = t[1]
            if 'v' in pos_tag.lower():
                discourage = True
        
    return discourage

def load_quotes(file_name):
    """Loads quotes from a given file.
    
    Parameters
    ----------
    file_name    string: Name of file.
    
    Returns
    -------
    quotes       list: List of quotes.
    """
    
    f = open(file_name, 'r')
    quotes = f.readlines()
    quotes = [s.strip() for s in quotes]
    f.close()
    
    return quotes

def get_quote(sentence):
    """Gets a quote that is relevant to an input sentence.
    
    Parameters
    ----------
    sentence    string: Sentence to be analyzed.
    
    Returns
    -------
    quote       string: A single quote.
    """
       
    #list of negative words
    #neg_words = get_negs(sentence)
    
    #find out what type of quote to choose
    discourage = is_discourage(nltk.word_tokenize(sentence))
    
    if discourage is True:
        disc = load_quotes('discouraging file.txt')
        rand = random.randrange(len(disc))
        quote = disc[rand]
    else:
        #get quote info
        encourage = load_quotes('encouraging file.txt')
        rand = random.randrange(len(encourage))
        quote = encourage[rand]

    print(discourage)
    print(quote)
    speakmywords.main(quote)

if __name__ == "__main__":
    get_quote(sys.argv[1])
