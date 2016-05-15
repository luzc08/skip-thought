from gensim.models import word2vec
import logging

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

model = word2vec.Word2Vec.load_word2vec_format('/tmp/vectors.bin', binary=True)

model.most_similar(['girl', 'father'], ['boy'], topn=3)

model.doesnt_match("breakfast cereal dinner lunch".split())