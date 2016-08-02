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

data_path = '/data2/luzhc/raw_text/'

target_path = '/data2/luzhc/tfidf/'

all_tokens = []

def collect_text(filename):
    f_name = os.path.join(data_path, filename)
    print 'processing', f_name
    if not os.path.isfile(f_name):
        return []
    for line in open(f_name):
        sentences = sent_tokenize_text(line)
        for t_sent in sentences:
            sent = re.sub(p, '', t_sent)
            tokens = word_tokenize(sent)
            tokens = [i.lower() for i in tokens if i not in string.punctuation and i not in stopwords.words('english')]
            stems = stem_tokens(tokens, stemmer)
            return stems
            # all_tokens = all_tokens + stems
            # new_line = ' '.join(stems)
            # new_line = ' '.join(tokens)
            # f.write(new_line + '\n')
    # f = open(target_path + conf_name + '.txt', "a+")
folders = os.listdir(data_path)

if not os.path.exists(target_path):
    os.makedirs(target_path)

t_folders = os.listdir(target_path)

for filename in folders:
    all_tokens = all_tokens + collect_text(filename)

count = Counter(all_tokens)
print count.most_common(100)



