from gensim.models import word2vec
import logging

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

model = word2vec.Word2Vec.load_word2vec_format('/data2/luzhc/GoogleNews-vectors-negative300.bin', binary=True)

print model.most_similar(['girl', 'father'], ['boy'], topn=3)

print model.doesnt_match("breakfast cereal dinner lunch".split())