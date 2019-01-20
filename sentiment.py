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
import sys
import speakmywords


def get_negs(sentence):
    """Gets the negative words in a sentence.
    
    Parameters
    ----------
    sentence    string: String of words.
    
    Returns
    -------
    neg_list    list: List of negative words.
    """

    barred = ['fucking']
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

def load_quotes(file_name):
    """Loads quotes from a given file.
    
    Parameters
    ----------
    file_name    string: Name of file.
    
    Returns
    -------
    (quotes_list, quotes_str)
    
    quotes_list       list: List of quotes.
    quotes_str       string: List of quotes.
    """
    
    f = open(file_name, 'r')
    quotes_list = f.readlines()
    quotes_list = [s.strip() for s in quotes_list]
    f.close()
    
    f = open(file_name, 'r')
    quotes_str = f.read()
    f.close()
    
    return quotes_list, quotes_str

def find_synonyms(my_list):
    """Create a list of synonyms for a given word.

    Parameters
    ----------

    my_list    list: List containing strings.

    Returns
    -------
    d:         dictionary: {original_word: [synonyms]}
    """
    
    assert type(my_list) == list, "Passed object is not of type list."
    
    s = []        #synonym list
    d = dict()
    count = 0
    
    for word in my_list:
        for syn in wordnet.synsets(word): 
            for l in syn.lemmas():
                #name of synonym
                s.append(l.name()) 
        d[word] = list((set(s)))
        
    #replace underscores
    for syn in d:
        for s in d[syn]:
            #reassign list item vals
            d[syn][count] = s.replace('_', ' ')
            count +=1
        #reset counter
        count = 0
    return d


def select_best_quote(file_name, neg_list, sentence):
    
    # print('Negative words: {}'.format(neg_list))
    quotes_list, quotes_str = load_quotes(file_name)
    quotes_relevant = []
    best_quote = ''
    word_list = []
    
    #if there are any negative words
    if len(neg_list) > 0:
        word_list == neg_list
    else:
        word_list == sentence
        
    for word in word_list:

        #if in any quotes, search quotes
        if word in quotes_str:
            #print('Yes {} is in at least 1 quote.'.format(word))
            for q in quotes_list:

                #if in a quote, return the quote
                if word in q:
                    quotes_relevant.append(q)

        #if there are negatives, but no quotes with 
        #the same words, check synonyms.

        #find synonyms
        syn_dict = find_synonyms(word_list)

        #print('Syonym Dictionary: {}'.format(syn_dict))

        #{'negative_word':[syn1, syn2, syn3...]}
        for key in syn_dict:

            #for [syn1, syn2, syn3...]
            for synonym in syn_dict[key]:
                if synonym in quotes_list:
                    #loop through all quotes
                    for qt in quotes_list:
                        if synonym in qt:
                            quotes_relevant.append(q)
                                    
        #print('Length Relevant Quotes: {}'.format(len(quotes_relevant)))
        
        if len(quotes_relevant) > 0:
            rand = random.randrange(len(quotes_relevant))
            best_quote = quotes_relevant[rand]
        else:
            rand = random.randrange(len(quotes_list))
            best_quote = quotes_list[rand]
        
    #precaution if there are no relevant quotes
    if best_quote == '':
        rand = random.randrange(len(quotes_list))
        best_quote = quotes_list[rand]
        
    return best_quote


def get_quote(sentence_str):
    """Gets a quote that is relevant to an input sentence.
    
    Parameters
    ----------
    sentence_str    string: Sentence to be analyzed.
    
    Returns
    -------
    quote       string: A single quote.
    """
    sentence = nltk.word_tokenize(sentence_str)
    sent_list = [s.lower() for s in sentence]
    #print(sent_list)
    negs = get_negs(' '.join(sentence))

    if len(negs) == 0 and 'not' not in sent_list:
        #print('Nothing negative. Restarting')
        return

    if len(negs) == 1 and 'not' in sent_list:
        #print('Nothing negative (Double Negative). Restarting')
        return

    discourage = False          #initialize discourage to false
    tags = nltk.pos_tag(sentence)
    #print('POS Tags: {}'.format(tags))
    
    #If "I" in sentence and negative word in 
    #sentence and negative word is a verb
    #Possibly swap this functin out for Jamie's
    if 'i' in sent_list and len(negs) > 0:
        for t in tags:
            pos_tag = t[1]
            if 'v' in pos_tag.lower():
                neg_verbs = get_negs(t[0])
                
                if len(neg_verbs) > 0:
                    discourage = True
                    #print('It evaluated to true')
                
    #print('Discourage result: {}'.format(discourage))           
                
    if discourage is True:
        quote = select_best_quote('discouraging file2.txt', negs, sentence)
    else:
        quote = select_best_quote('encouraging file2.txt', negs, sentence)
    print(quote)
    speakmywords.main(quote)


if __name__ == '__main__': 
    get_quote('Today is annoying as fuck.')