#coding=utf8

from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer

vectorizer = CountVectorizer()
transformer = TfidfTransformer()

corpus = [
'This is the first document.',
'This is the second second document.',
'And the third one.',
'Is this the first document?',
]
X = vectorizer.fit_transform(corpus)
print(X.toarray())

print(vectorizer.get_feature_names())

tfidf = transformer.fit_transform(X.toarray())
print(tfidf.toarray())