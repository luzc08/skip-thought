import skipthoughts
from nlp_modules import *
import cPickle as pickle
import sys
sys.path.insert(0, 'libsvm/python/')
#from libsvm.python.svmutil import *
from svmutil import *

if sys.argv[1]=='load':
    model = skipthoughts.load_model()

    #sentX = test_sentence()

    train_sentences = pickle.load( open( "sentences.p", "rb" ))
    train_label = pickle.load( open( "labels.p", "rb" ))

#print train_sentences
#print train_label

    train_vectors = skipthoughts.encode(model,train_sentences)

    pickle.dump( train_vectors, open("vectors.p", "wb"))

if sys.argv[1]=='train':
    model = skipthoughts.load_model()

    train_vectors = pickle.load( open( "vectors.p", "rb" )).tolist()
    train_label = pickle.load( open( "labels.p", "rb" ))
    #train_vectors = skipthoughts.encode(model,train_sentences)
    AZmodel = svm_train(train_label,train_vectors)
    svm_save_model('AZ.model', AZmodel)

if sys.argv[1]=='predict':
    #model = skipthoughts.load_model()
    AZmodel = svm_load_model('AZ.model')
    train_vectors = pickle.load( open( "vectors.p", "rb" )).tolist()
    train_label = pickle.load( open( "labels.p", "rb" ))
    p_labels, p_acc, p_vals = svm_predict(train_label[0:1000], train_vectors[0:1000], AZmodel)
    for idx in range(0,1000):
        print train_label[idx],p_labels[idx]
    (ACC, MSE, SCC) = evaluations(train_label[0:1000], p_labels)
