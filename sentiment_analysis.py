
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

def get_negs(sentence):
    """Gets the negative words in a sentence.
    
    Parameters
    ----------
    sentence    string: String of words.
    
    Returns
    -------
    neg_list    list: List of negative words.
    """
    
    text = nltk.word_tokenize(sentence)
    tags = nltk.pos_tag(text)
    neg_list = []
    barred = ['fuck','fucking']
    
    #load negative word data
    f = open('negative_words.txt')
    neg_db = f.readlines()
    neg_db = [w.strip() for w in neg_db]
    f.close()
    
    for t in tags:
        #list of sentiment sets e.g <breakdown.n.03: PosScore=0.0 NegScore=0.25>
        neg = list(swn.senti_synsets(t[0]))
        word = t[0]
        
        #filter words with 50% negative rating     
        check_negativity = [word for n in neg if n.neg_score()>=0.5]
        neg = list(swn.senti_synsets(t[0]))
        word = t[0]
            
        if ((word in check_negativity) and (word not in barred)) or (word in neg_db):
            neg_list.append(word)

    return list(set(neg_list))

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

def find_quotes(neg_words, sentence, q_file):
    """Finds relevant quotes that corelate to the 
    sentence and negative words.
    
    Function is incomplete.
    
    Parameters
    ----------
    neg_list    list: List of negative words.
    sentence    string: String of words.
    q_file      string: Name of file with extension.
    
    Returns
    -------
    quotes    list: List of quotes.
    """
    
    f = open(q_file, 'r')
    quotes = f.readlines()
    quotes = [q.strip() for q in quotes]
    f.close()
    
def get_quotes(syns, quotes):
    """Finds relevant quotes that corelate to the 
    sentence and negative words.
    
    Parameters
    ----------
    syns      dict: Dictionary of {'word': [list, of, synonyms]}.
    quotes    list: List of quotes
    
    Returns
    -------
    q    generator: Quotes relevant to the sy.
    """
    assert type(syns) == dict, "Sysnonyms is not type dictionary."
    assert type(quotes) == list, "Quotes is not type list."
    
    all_syns = []
    relevant = []

    #combine lists and add key to list
    for k in syns:
        all_syns.append(k)
        all_syns = syns[k] + all_syns

    for q in quotes:
        for s in syns:
            if s in q:
                    yield q
                    
def verbs_and_negs(text):
    v = []
    neg_list = []
    tags = nltk.pos_tag(text)
    
    #find verb POS tags
    for t in tags:
        if 'v' in t[1].lower():
            v.append(t)

    #find negative words
    for t in tags:
        #list of sentiment sets e.g <breakdown.n.03: PosScore=0.0 NegScore=0.25>
        neg = list(swn.senti_synsets(t[0]))

        #filter words with 50% negative rating
        check_negativity = [t[0] for n in neg if n.neg_score()>=0.25]
        if t[0] in check_negativity:
            neg_list.append(t[0])

    return (v, list(set(neg_list)))

def is_discourage(sentence):
    """Checks if a sentence should be discouraged.
    
    Parameters
    ----------  
    sentence    string: Sentence that will be analyzed.
    
    Returns
    -------
    discourage   bool: Wether it should be discouraged.
    """
    
    sent_list = sentence.split(' ')
    sent_list = [s.lower() for s in sent_list]
    negs = get_negs(sentence)
    discourage = False          #initialize discourage to false
    print(negs)
    text = nltk.word_tokenize(sentence)
    tags = nltk.pos_tag(text)
    
    #If "I" in sentence and negative word in 
    #sentence and negative word is a verb
    if 'i' in sent_list and len(negs) > 0:
        for t in tags:
            pos_tag = t[1]
            if 'v' in pos_tag.lower():
                discourage = True
        
    return discourage
