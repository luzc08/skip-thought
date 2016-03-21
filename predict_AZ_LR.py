import numpy as np
import skipthoughts
from sklearn.linear_model import LogisticRegression
#from sklearn.naive_bayes import MultinomialNB
#from sklearn.linear_model import SGDClassifier
#from sklearn.cross_validation import KFold
#from sklearn.utils import shuffle
import cPickle as pickle
import nltk
from nltk.tokenize import word_tokenize

def predict_AZ(model,sentences):
    clf = pickle.load(open("LRModel.p", "rb"))
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
        result = ''
        for s in sents:
            tokens = word_tokenize(s)
            result += ' ' + ' '.join(tokens)
        X.append(result)
    return X

if __name__ == "__main__":
    test0 = "New information technologies are changing the way we do science. One promising new development in empirical research methodology is the emergence of online experimentation. Compared to their offline equivalents, online experiments are more customizable, more scalable, and allow for much wider and more diverse participation beyond traditionally WEIRD samples. They allow for designs that minimize experimenter effects, promote replicable methods, and lower the cost of conducting rigorous empirical research at a large scale. Modifying or repurposing existing experimental settings is much easier online, as is the open sharing of technologies, standards, and protocols. "
    sent = preprocess(test0)
    print sent
    #model = skipthoughts.load_model()
    #k = predict_AZ(model, sent)
