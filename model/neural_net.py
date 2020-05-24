import pandas as pd
from tools import nltk_tools
import itertools
import string
import torch
import torch.nn as nn
import torch.optim as optim

df = pd.read_csv("tools/data.csv")
df = df.dropna(subset=["title"])

vector_size = 10000


def process_titles(data):
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
    top_words = tokens.value_counts().index[:vector_size]
    word_table = {word: index for index, word in enumerate(top_words)}
    tokens = tokens[tokens.map(lambda x: x in word_table)]
    tokens = tokens.map(word_table)

    return tokens, word_table


X, word_table = process_titles(df.title)
y = df.score

torch.manual_seed(1)


class Model(nn.Module):
    def __init__(self, input_size):
        super(Model, self).__init__()

        self.input_size = input_size
        self.input_l2_size = 100
        self.hidden_size = 1000

        self.input_to_input_l2 = nn.Linear(self.input_size, self.input_l2_size)
        self.combined_to_hidden = nn.Linear(self.input_l2_size + self.hidden_size, self.hidden_size)
        self.combined_to_out = nn.Linear(self.input_l2_size + self.hidden_size, 1)

    def forward(self, input_word, hidden):
        input_l2 = self.input_to_input_l2(input_word)
        combined = torch.cat((input_l2, hidden))
        hidden = self.combined_to_hidden(combined)

        new_combined = torch.cat((input_l2, hidden))
        out = self.combined_to_out(new_combined)

        return out, hidden

