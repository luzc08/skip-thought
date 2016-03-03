import skipthoughts
from nlp_modules import *

model = skipthoughts.load_model()

sentX = test_sentence()

vectors = skipthoughts.encode(model,sentX)

testX = 'We present Myopoint, an EMG and IMU pointing and clicking technique using a consumer Myo arm band device'


testX = 'We thank Min Jeong Kim for her help with the figures used in this paper'
skipthoughts.nn(model,sentX,vectors,testX)
