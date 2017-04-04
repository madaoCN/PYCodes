#coding=utf8

from __future__ import unicode_literals
from nltk.stem.lancaster import LancasterStemmer
import nltk


if __name__ == "__main__":
    # st = LancasterStemmer()
    # print(st.stem('你 到底 在 说 什么'))

    # wnl = nltk.WordNetLemmatizer()
    # print(wnl.lemmatize(st.stem('你 到底 在 说 什么')))

    fd = nltk.FreqDist('你 到底 在 说 什么')
    print(fd.tabulate())
