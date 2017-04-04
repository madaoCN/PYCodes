#_*_coding=utf8_*_
import nltk
from nltk.corpus import brown


def search_most_100():
    fd = nltk.FreqDist(
        brown.words(categories='news')
    )
    cfd = nltk.ConditionalFreqDist(
        brown.tagged_words(categories='news')
    )
    most_freq_words = fd.keys()[:100]

    likely_tags = dict((word, cfd[word].max()) for word in most_freq_words)

    baseline_tagger = nltk.UnigramTagger(model=likely_tags)

    baseline_tagger.evaluate(brown_tagged_sents)

if __name__ == "__main__":
    search_most_100()