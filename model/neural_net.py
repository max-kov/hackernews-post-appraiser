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


class RNNModel(nn.Module):
    def __init__(self, input_size):
        super(RNNModel, self).__init__()

        self.input_size = input_size
        self.hidden_size = 1000
        self.embedding_size = 1000

        self.embedding = nn.Embedding(self.input_size, self.embedding_size)
        self.hidden = nn.RNN(self.embedding_size, self.hidden_size, batch_first=True)
        self.hidden_to_out = nn.Linear(self.hidden_size, 1)

    def forward(self, input_sentence):
        embeddings = self.embedding(input_sentence)
        _, hidden = self.hidden(embeddings.unsqueeze(0))
        out = self.hidden_to_out(hidden[0][0])

        return out



        out = self.hidden_to_out(hidden)

        return out


data_point_count = df.shape[0]
model = RNNModel(vector_size)

criterion = nn.SmoothL1Loss()
optimizer = optim.SGD(model.parameters(), lr=0.001)

print("Starting training - word vector length = {}, data points = {}".format(vector_size, data_point_count))

total_loss = torch.autograd.Variable(torch.zeros(1), requires_grad=True)
sentances = X.groupby(level=0).apply(lambda x: torch.tensor(x.values))

for i, sample in sentances.items():
    out = model(sample)
    loss = criterion(out, torch.tensor([y[i]]))
    total_loss = total_loss + loss

    if i % 50 == 0:
        optimizer.zero_grad()
        total_loss.backward()
        optimizer.step()
        total_loss = torch.autograd.Variable(torch.zeros(1), requires_grad=True)

    if i % 100 == 1:
        print("{} out of {}, Sample \"{}\", score = {}, predicted score {},  loss = {}"
              .format(i, data_point_count, df.title[i], df.score[i], out[0], loss))
