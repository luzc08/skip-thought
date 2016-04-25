import skipthoughts
import eval_AZ
import sys

if sys.argv[1]=='train':
    model = skipthoughts.load_model()
    eval_AZ.evaluate(model, evalcv=True, evaltest=False)

elif sys.argv[1]=='eval':
    model = skipthoughts.load_model()
    eval_AZ.evaluate(model, evalcv=False, evaltest=True)

elif sys.argv[1]=='eval_nb':
    model = skipthoughts.load_model()
    eval_AZ.evaluate(model, evalcv=False, evaltest=True, nb_feature=True)

elif sys.argv[1]=='train_eval':
    #default: logistic regression
    model = skipthoughts.load_model()
    eval_AZ.evaluate(model, evalcv=True, evaltest=True)

elif sys.argv[1]=='train_eval_nb':
    #default: logistic regression
    model = skipthoughts.load_model()
    for i in range(0, 4):
        eval_AZ.evaluate(model, evalcv=True, evaltest=True, nb_feature=True, nb_tag=i)

elif sys.argv[1] == 'train_eval_SVM':
    model = skipthoughts.load_model()
    eval_AZ.evaluate(model, evalcv=True, evaltest=True, classifier='SVM')
