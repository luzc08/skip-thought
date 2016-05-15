from gensim.models import word2vec
import logging
import os

corpus_dir = '/data2/luzhc/pre_processed_text/'

class HCISentences(object):
    def __init__(self, dirname):
        self.dirname = dirname

    def __iter__(self):
        for fname in os.listdir(self.dirname):
            for line in open(os.path.join(self.dirname, fname)):
                yield line.split()


logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

#model = word2vec.Word2Vec.load_word2vec_format('/data2/luzhc/GoogleNews-vectors-negative300.bin', binary=True)
sentences = HCISentences(corpus_dir)

model = word2vec.Word2Vec(sentences, size = 200)

model.save('/data2/luzhc/w2v_data/test.model')

print model.most_similar(['girl', 'father'], ['boy'], topn=3)

print model.doesnt_match("breakfast cereal dinner lunch".split())