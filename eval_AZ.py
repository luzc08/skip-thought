'''
Evaluation code for the AZ dataset
'''
import numpy as np
import skipthoughts
from sklearn.linear_model import LogisticRegression
from sklearn.cross_validation import KFold
from sklearn.utils import shuffle
import cPickle as pickle


def evaluate(model, k=10, seed=1234, evalcv=True, evaltest=False):
    """
    Run experiment
    k: number of CV folds
    test: whether to evaluate on test set
    """
    print 'Preparing data...'

    [train, train_labels, test, test_labels] = load_data()
    #train_labels = prepare_labels(train_labels)
    #test_labels = prepare_labels(test_labels)
    train, train_labels = shuffle(train, train_labels, random_state=seed)

    print 'Computing training skipthoughts...'
    trainF = skipthoughts.encode(model, train, verbose=False, use_eos=False)
    
    if evalcv:
        print 'Running cross-validation...'
        #interval = [2**t for t in range(0,9,1)]     # coarse-grained
        interval = [t for t in range(1,20,1)]
        C = eval_kfold(trainF, train_labels, k=k, scan=interval, seed=seed)

    if evaltest:
        if not evalcv:
            C = 16     # Best parameter found from CV

        print 'Computing testing skipthoughts...'
        testF = skipthoughts.encode(model, test, verbose=False, use_eos=False)

        print 'Evaluating...'
        clf = LogisticRegression(C=C, solver='newton-cg', multi_class='multinomial', n_jobs=-1)
        clf.fit(trainF, train_labels)
        yhat = clf.predict(testF)
        pickle.dump( yhat, open("test_labels.p", "wb"))
        print 'Test accuracy: ' + str(clf.score(testF, test_labels))


def load_data():
    """
    Load the TREC question-type dataset
    """
    train_sentences = pickle.load(open("sentences.p", "rb"))
    train_label = np.array(pickle.load(open("labels.p", "rb")))

    train = train_sentences[0:9000]
    train_labels = train_label[0:9000]
    test = train_sentences[9001:]
    test_labels = train_label[9001:]

    return train, train_labels, test, test_labels

def eval_kfold(features, labels, k=10, scan=[2**t for t in range(0,9,1)], seed=1234):
    """
    Perform k-fold cross validation
    """
    npts = len(features)
    kf = KFold(npts, n_folds=k, random_state=seed)
    scores = []

    for s in scan:

        scanscores = []

        for train, test in kf:

            # Split data
            X_train = features[train]
            y_train = labels[train]
            X_test = features[test]
            y_test = labels[test]

            # Train classifier
            clf = LogisticRegression(C=s, solver='newton-cg', multi_class='multinomial', n_jobs=-1)
            clf.fit(X_train, y_train)
            score = clf.score(X_test, y_test)
            scanscores.append(score)
            print (s, score)

        # Append mean score
        scores.append(np.mean(scanscores))
        print scores

    # Get the index of the best score
    s_ind = np.argmax(scores)
    s = scan[s_ind]
    print (s_ind, s)
    return s

