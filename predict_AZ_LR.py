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

tags=['Background','Conclusion', 'Problem', 'Result', 'Connection', 'Method', 'Difference','Future']

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
        # result = ''
        # for s in sents:
        #     tokens = word_tokenize(s)
        #     result += ' ' + ' '.join(tokens)
        X += sents
    return X

if __name__ == "__main__":
    test0 = ["Percussion is a musical practice more defined by the methods of interacting with instruments rather than the instruments themselves. Percussionists perform by ?striking, scraping, brushing, rubbing, whacking, or crashing any... available object? [11]. These percussive gestures are used to coax wide varieties of timbres and musical gestures from simple instruments. For percussionists, free improvisation is often a process of gestural exploration, discovering new sounds from traditional and non-traditional instruments and responding to other sounds in an ensemble. Like some percussion instruments, touch-screen computing devices can be rubbed, scraped, and struck with fingers and hands. While it is well established that popular touch-screen devices can be used to make music, mainstream creative frameworks for their use (tapping virtual piano keys, for instance) are limited. The percussive affordances of these devices motivates an exploration of their use in a modern percussion ensemble to establish more varied modes of interaction that could be used in app-design, for musical composition, and other applications.",
             "HCI studies of gestures on touch screens have been conducted for tasks such as activating a shortcut in a smartphone [10, 1], manipulating virtual objects on a table-based interface [7] and controlling a video performance [9]. Many of these studies have characterised gestures that emerged as part of users' interactions with a touch interface. In a similar way, the work described in this paper examines touch-screen gestures that emerge when iPads are introduced into a modern, freeimprovisation percussion ensemble. Qualitative analysis of a series of the group's rehearsals and discussions reveals a vocabulary of new gestures invented by the musicians. These gestures were used by the musicians to creatively interactwith, and expand the power of, two specially-designed iPad percussion apps. Unlike other studies such as Wobbrock et al [12], the gestures we observed are generally two-handed and combine many touches over a number of seconds to express sustained musical ideas. Our study also yields a refined concept of how iPad based instruments fit into a percussive artistic practice and how these instruments can contribute to the musical structure of a free-improvisation."]
    sent = preprocess(test0)
    #print sent
    model = skipthoughts.load_model()
    k = predict_AZ(model, sent)
    annotations = [tags[x] for x in k]
    for idx, s in enumerate(sent):
        print annotations[idx],s
