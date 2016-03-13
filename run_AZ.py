import skipthoughts
import eval_AZ

model = skipthoughts.load_model()
eval_AZ.evaluate(model, evalcv=True, evaltest=False)
