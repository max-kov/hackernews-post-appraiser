import itertools
import string

import pandas as pd
import torch

from tools import nltk_tools

reserved_tokens = 1


def process_titles(data, vector_size, word_table=None):
    tokenizer = nltk_tools.get_tokenizer().tokenize
    token_arrs = [tokenizer(title) for title in data.values]
    index = pd.MultiIndex.from_tuples(
        [(data.index[i], ii) for i, tokens in enumerate(token_arrs) for ii, _ in enumerate(tokens)],
        names=["sentance", "word"]
    )
    tokens = pd.Series(itertools.chain.from_iterable(token_arrs), index=index)

    # Remove stopwords
    stopwords = nltk_tools.get_stopwords()
    tokens = tokens[tokens.map(lambda x: x not in stopwords)]
    # Remove non-ascii
    tokens = tokens.map(lambda word: ''.join(filter(lambda char: char in string.ascii_letters, word)))
    # Remove empty
    tokens = tokens[tokens != ""]
    # Stem
    stemmer = nltk_tools.get_stemmer().stem
    tokens = tokens.map(lambda word: stemmer(word))
    # only take first top n words
    top_words = tokens.value_counts().index[:(vector_size - reserved_tokens)]
    if word_table is None:
        word_table = {word: reserved_tokens + index for index, word in enumerate(top_words)}
    tokens = tokens.map(lambda x: word_table.get(x, 0))
    tokens = tokens.groupby(level=0).apply(lambda x: torch.tensor(x.values)).rename("sentance_vector")
    indeces = tokens.index
    tokens = tokens.reset_index(drop=True)

    return tokens, indeces, word_table
