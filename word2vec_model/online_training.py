from gensim.models import word2vec
import logging
import nltk
from nltk.tokenize import word_tokenize
import string
import cPickle as pickle

target_dir = '/data2/luzhc/w2v_data/'

class BioSentences(object):
    def __init__(self, filename):
        self.filename = filename

    def __iter__(self):
        for sent in pickle.load(open(self.filename, "rb")):
            tokens = word_tokenize(sent)
            tokens = [i.lower() for i in tokens if i not in string.punctuation]
            yield tokens


# def prepare_biotext():
#     train_sentences = pickle.load(open("sentences.p", "rb"))
#     result = []
#     for sent in train_sentences:
#         #sent = re.sub(p, '', t_sent)
#         tokens = word_tokenize(sent)
#         tokens = [i.lower() for i in tokens if i not in string.punctuation]
#         result.append(tokens)
#     return result

model = word2vec.Word2Vec.load('/data2/luzhc/w2v_data/test.model')

sentences = BioSentences("sentences.p")

model.train(sentences)

model.save(target_dir+'mixed.model')

print model.most_similar(['girl', 'father'], ['boy'], topn=3)

print model.doesnt_match("breakfast cereal dinner lunch".split())





