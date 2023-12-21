r"""
FastText Model
==============

Introduces Gensim's fastText model and demonstrates its use on the Lee Corpus.
"""

import logging
# logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

from gensim.models import FastText
from gensim.models.fasttext import load_facebook_vectors
from gensim.test.utils import common_texts  # some example sentences

print(common_texts[0])

print(len(common_texts))

model2 = FastText(vector_size=4, window=3, min_count=1, sentences=common_texts, epochs=10)

prediction = model2.predict_output_word(['Hello my name is Mike'])

print(prediction)

from gensim.test.utils import datapath

cap_path = datapath("crime-and-punishment.bin")
wv = load_facebook_vectors(cap_path)



