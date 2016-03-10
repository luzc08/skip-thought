import skipthoughts
from nlp_modules import *
import cPickle as pickle

model = skipthoughts.load_model()

sentX = test_sentence()

train_sentences = pickle.load( open( "sentences.p", "rb" ))
train_label = pickle.load( open( "labels.p", "rb" ))

print train_sentences
print train_label

train_vectors = skipthoughts.encode(model,train_sentences)
