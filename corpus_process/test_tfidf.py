# run tf-idf on preprocessed data

import os.path
import nltk
from nltk.tokenize import word_tokenize
from nltk.stem import *
from nltk.corpus import stopwords
import re
import string
from collections import Counter
from pre_process_para import *
import cPickle as pickle

data_path = '/data2/luzhc/raw_text/'

target_path = '/data2/luzhc/tfidf/'

all_tokens = []

# cnt = 0

def collect_text1(filename):
    f_name = os.path.join(data_path, filename)
    print f_name + ' ? '
    # print 'processing', f_name
    tokens = []
    if not os.path.isfile(f_name):
        return tokens
    for line in open(f_name):
        print line
        sentences = sent_tokenize_text(line)
        for t_sent in sentences:
            # cnt += 1
            sent = re.sub(p, '', t_sent)
            tokens = word_tokenize(sent)
            tokens = [i.lower() for i in tokens if i not in string.punctuation]
            stems = stem_tokens(tokens, stemmer)
            # if cnt%10 == 0:
            #     print stems

    tokens = tokens + stems
    return tokens
            # all_tokens = all_tokens + stems
            # new_line = ' '.join(stems)
            # new_line = ' '.join(tokens)
            # f.write(new_line + '\n')
    # f = open(target_path + conf_name + '.txt', "a+")
# folders = os.listdir(data_path)

# if not os.path.exists(target_path):
#     os.makedirs(target_path)

# t_folders = os.listdir(target_path)
all_tokens = collect_text1('CHI2015')


# for filename in folders:
#     tmp = collect_text(filename)
#     if tmp:
#         all_tokens = all_tokens + tmp

pickle.dump( all_tokens, open( target_path+"tokens.p", "wb" ) )
count = Counter(all_tokens)
print count.most_common(100)