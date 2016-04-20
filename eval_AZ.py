'''
Evaluation code for the AZ dataset
'''
import numpy as np
import skipthoughts
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import MultinomialNB
from sklearn.linear_model import SGDClassifier
from sklearn import svm
from sklearn.cross_validation import KFold
from sklearn.utils import shuffle
import cPickle as pickle

#Classifiers: LG, NB, SVM?

def evaluate(model, k=10, seed=1234, evalcv=True, evaltest=False, classifier='LG'):
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
        interval = [2**t for t in range(0,9,1)]     # coarse-grained
        #interval = [t for t in range(1,20,1)]
        C = eval_kfold(trainF, train_labels, k=k, scan=interval, seed=seed, classifier=classifier)

    if evaltest:
        if not evalcv:
            C = 8     # Best parameter found from CV
            #C = 1e-3

        print 'Computing testing skipthoughts...'
        testF = skipthoughts.encode(model, test, verbose=False, use_eos=False)

        print 'Evaluating...'
        if classifier=='LG':
            clf = LogisticRegression(C=C, solver='newton-cg', multi_class='multinomial', n_jobs=-1)
            clf.fit(trainF, train_labels)
            yhat = clf.predict(testF)
            pickle.dump(yhat, open("LR_test_labels.p", "wb"))
            pickle.dump(clf, open("LRModel.p", "wb"))

        if classifier=='SVM':
            clf = svm.SVC(decision_function_shape='ovo')
            clf.fit(trainF, train_labels)
            yhat = clf.predict(testF)
            pickle.dump(yhat, open("SVM_test_labels.p", "wb"))
            pickle.dump(clf, open("SVM_Model.p", "wb"))
        #clf = MultinomialNB().fit(trainF, train_labels)
        # clf = SGDClassifier(loss='hinge', penalty='l2', alpha=C, n_iter=5, random_state=seed)
        # clf.fit(trainF, train_labels)

        print 'Test accuracy: ' + str(clf.score(testF, test_labels))


def load_data():
    """
    Load the TREC question-type dataset
    """
    train_sentences = pickle.load(open("sentences.p", "rb"))
    train_label = np.array(pickle.load(open("labels.p", "rb")))

    train = train_sentences[0:7500]
    train_labels = train_label[0:7500]
    test = train_sentences[7501:]
    test_labels = train_label[7501:]

    return train, train_labels, test, test_labels

def eval_kfold(features, labels, k=10, scan=[2**t for t in range(0,9,1)], seed=1234, classifier='LG'):
    """
    Perform k-fold cross validation
    """
    npts = len(features)
    kf = KFold(npts, n_folds=k, random_state=seed)
    scores = []

    #scan = [1e-2, 1e-3]

    if classifier == 'LG':
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
                # clf = MultinomialNB().fit(X_train, y_train)
                    # clf = SGDClassifier(loss='hinge', penalty='l2', alpha=s, n_iter=5, random_state=seed)
                    # clf.fit(X_train, y_train)

                score = clf.score(X_test, y_test)
                scanscores.append(score)
                print (s, score)
            # Append mean score
            scores.append(np.mean(scanscores))
            print scores
        s_ind = np.argmax(scores)
        s = scan[s_ind]
        print (s_ind, s)
        return s

    if classifier == 'SVM':
        scanscores = []

        for train, test in kf:
            # Split data
            X_train = features[train]
            y_train = labels[train]
            X_test = features[test]
            y_test = labels[test]

            clf = svm.SVC(decision_function_shape='ovo')
            clf.fit(X_train, y_train)
            score = clf.score(X_test, y_test)
            scanscores.append(score)
            #print (s, score)

        #scores.append(np.mean(scanscores))
        print np.mean(scanscores)
        return 0
    # Get the index of the best score

