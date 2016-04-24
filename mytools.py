import cPickle as pickle
from collections import Counter
import numpy as np

train_label = np.array(pickle.load(open("labels.p", "rb")))
p = Counter(train_label)
print train_label
print p
