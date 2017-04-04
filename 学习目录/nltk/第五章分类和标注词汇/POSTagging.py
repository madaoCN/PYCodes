import nltk

text = nltk.word_tokenize("what the fox say?")

print(text)
nltk.pos_tag(text)