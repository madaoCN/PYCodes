#_*_coding=utf8_*_
import nltk
from nltk.corpus import brown
tagged_token = nltk.tag.str2tuple('fly/NN')#针对已经标记好的字符串转换
print(tagged_token)


#读取已标注的语料库
print(nltk.corpus.brown.tagged_words())
#简化标记
# print(nltk.corpus.brown.tagged_words(simplify_tags=True))


#布朗语料库新闻类中最常见的
brown_news_taged = brown.tagged_words(categories='news')
# tag_fd = nltk.FreqDist(brown_news_taged)
# print(tag_fd.keys())

#名词
word_tag_pairs = nltk.bigrams(brown_news_taged)
n_list = list(nltk.FreqDist(a[1] for (a,b) in word_tag_pairs if b[1] == 'N'))