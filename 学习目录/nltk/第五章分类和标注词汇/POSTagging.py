#_*_coding=utf8_*_
import nltk

text = nltk.word_tokenize("what the fox say?")
print(nltk.pos_tag(text))#对词汇进行标注

text = nltk.Text("what the fox say?")
print(text.similar('w'))