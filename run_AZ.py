import skipthoughts
import eval_AZ
import sys

if sys.argv[1]=='train':
    model = skipthoughts.load_model()
    eval_AZ.evaluate(model, evalcv=True, evaltest=False)

elif sys.argv[1]=='eval':
    model = skipthoughts.load_model()
    eval_AZ.evaluate(model, evalcv=False, evaltest=True)

elif sys.argv[1]=='train_eval':
    model = skipthoughts.load_model()
    eval_AZ.evaluate(model, evalcv=True, evaltest=True)
