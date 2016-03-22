import numpy as np
import skipthoughts
from sklearn.linear_model import LogisticRegression
#from sklearn.naive_bayes import MultinomialNB
#from sklearn.linear_model import SGDClassifier
#from sklearn.cross_validation import KFold
#from sklearn.utils import shuffle
import cPickle as pickle
import nltk
from nltk.tokenize import word_tokenize

tags=['Background','Conclusion', 'Problem', 'Result', 'Connection', 'Method', 'Difference','Future']

def predict_AZ(model,sentences):
    clf = pickle.load(open("LRModel.p", "rb"))
    vectors = skipthoughts.encode(model, sentences, verbose=False, use_eos=False)
    yhat = clf.predict(vectors)
    return yhat

def preprocess(text):
    """
    Preprocess text for encoder
    """
    X = []
    sent_detector = nltk.data.load('tokenizers/punkt/english.pickle')
    for t in text:
        sents = sent_detector.tokenize(t)
        # result = ''
        # for s in sents:
        #     tokens = word_tokenize(s)
        #     result += ' ' + ' '.join(tokens)
        X += sents
    return X

if __name__ == "__main__":
    test0 = ["Nature has engineered its own actuators, as well as the efficient material composition, geometry and structure to utilize its actuators and achieve functional transformation. Based on the natural phenomenon of cells' hygromorphic transformation, we introduce the living Bacillus Subtilis natto cell as a humidity sensitive nanoactuator. In this paper, we unfold the process of exploring and comparing cell types that are proper for HCI use, the development of the composite biofilm, the development of the responsive structures, the control setup for actuating biofilms, and a simulation and fabrication platform. Finally, we provide a variety of application designs, with and without computer control to demonstrate the potential of our bio actuators. Through this paper, we intend to enable the use of natto cells and our platform technologies for HCI researchers, designers and bio-hackers. More generally, we try to encourage the research and use of biological responsive materials and interdisciplinary research in HCI.",
             "Looking into nature, from the wilting of flowers to the opening of fallen pinecones, biological sensors as well as actuators are omnipresent. Utilizing such mechanisms from nature through the integration of living organisms into design and engineering has gained increasing interest amongst scientists and engineers [3][16]. On the other hand, in the field of Human-Computer Interaction (HCI), material-based interface design and shape-change interfaces are emerging topics[24]. Ishii describes 'Radical Atom' and suggests the dynamic manifestation of digital information in the physical world [9]. To add one more type of smart material for such research, we introduce a biological cell actuator, Bacilus Subtilis natto that responds to moisture changes to design interactive objects.",
             "Using living cells as an actuator has several distinctive advantages: electronic free, safe and edible, the lack of wires or tubes, quiet transformation, potential biological synthesis, self-reproduction and flexibility of deposition as a liquid form. However, there are still challenges when we seek to use living cell actuators in the HCI context. For example: how to gain access and use the material in a common prototyping environment while reducing biosafety level concerns? How to synthesize material on a macro scale with nano scale actuators? How to integrate digital fabrication for more precise manufacturing in order to embed a certain level of programmability to achieve desired transformation? How to integrate the human factor and digital controllability into a hydromorphic actuator that responds to the change of relative humidity? Through this work, we hope to address those challenges."]
    sent = preprocess(test0)
    #print sent
    model = skipthoughts.load_model()
    k = predict_AZ(model, sent)
    annotations = [tags[x] for x in k]
    for idx, s in enumerate(sent):
        print annotations[idx],s
