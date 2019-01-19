import textblob as tb
import sentiment_analysis

text = tb.TextBlob("I want to kill someone.")
if 'I' in text.tokenize():
    allpos = text.pos_tags
    verbphrase = []
    for x in allpos:
        if x[1] in ['VB', 'VBZ', 'VBP', 'VBD', 'VBN', 'VBG', 'RB', 'RBR', 'RBS']:
            verbphrase.append(x[0])

print(sentiment_analysis.get_negs(' '.join(verbphrase)))
