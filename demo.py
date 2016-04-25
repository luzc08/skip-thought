import numpy as np
import skipthoughts
from sklearn.linear_model import LogisticRegression
import cPickle as pickle
import nltk
from nltk.tokenize import word_tokenize

tags=['Background','Conclusion', 'Problem', 'Result', 'Connection', 'Method', 'Difference','Future']


def predict_AZ(model,sentences,clf):

    vectors = skipthoughts.encode(model, sentences, verbose=False, use_eos=False)
    yhat = clf.predict(vectors)
    return yhat


def preprocess(text):
    """
    Preprocess text for encoder
    """
    X = []
    sent_detector = nltk.data.load('tokenizers/punkt/english.pickle')
    for t in text:
        sents = sent_detector.tokenize(t)
        # result = ''
        # for s in sents:
        #     tokens = word_tokenize(s)
        #     result += ' ' + ' '.join(tokens)
        X += sents
    return X

if __name__ == "__main__":
    model = skipthoughts.load_model()
    clf = pickle.load(open("LRModel.p", "rb"))
    while True:
        sent = raw_input('Please enter text to test:')

        #print x.split()
        #sent = preprocess(test0)
        #print sent

        k = predict_AZ(model, sent, clf)
        annotations = [tags[x] for x in k]
        for idx, s in enumerate(sent):
            print s
            print annotations[idx]