import skipthoughts
from nlp_modules import *
import cPickle as pickle
import sys
sys.path.insert(0, 'libsvm/python/')
#from libsvm.python.svmutil import *
from svmutil import *

model = skipthoughts.load_model()

sentX = test_sentence()

train_sentences = pickle.load( open( "sentences.p", "rb" ))
train_label = pickle.load( open( "labels.p", "rb" ))

print train_sentences
print train_label

train_vectors = skipthoughts.encode(model,train_sentences)

AZmodel = svm_train(train_label,train_sentences)
svm_save_model('AZ.model', AZmodel)
