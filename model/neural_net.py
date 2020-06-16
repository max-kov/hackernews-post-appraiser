import pandas as pd
from tools import nltk_tools, model_to_file
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
    tokens = tokens.map(word_table).groupby(level=0).apply(lambda x: torch.tensor(x.values))
    indeces = tokens.index
    tokens = tokens.reset_index(drop=True)

    return tokens, indeces, word_table


X, indeces, word_table = process_titles(df.title)
y = df.score[indeces].reset_index(drop=True)

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

    def forward(self, input_sentence, lengths):
        embeddings = self.embedding(input_sentence)
        packed = nn.utils.rnn.pack_padded_sequence(embeddings, lengths, batch_first=True, enforce_sorted=False)
        _, hidden = self.hidden(packed)
        out = self.hidden_to_out(hidden[0]).double()

        return out


class LSTMModel(nn.Module):
    def __init__(self, input_size):
        super(LSTMModel, self).__init__()

        self.input_size = input_size
        self.hidden_size = 1000
        self.embedding_size = 1000

        self.embedding = nn.Embedding(self.input_size, self.embedding_size)
        self.hidden_layer = nn.LSTM(self.embedding_size, self.hidden_size, batch_first=True)
        self.hidden_to_out = nn.Linear(self.hidden_size, 1)

    def forward(self, input_sentence):
        embeddings = self.embedding(input_sentence)
        _, (hidden, _) = self.hidden_layer(embeddings.unsqueeze(0))
        out = self.hidden_to_out(hidden[0][0])

        return out


data_point_count = df.shape[0]
model = RNNModel(vector_size)

criterion = nn.SmoothL1Loss()
optimizer = optim.Adam(model.parameters())

print("Starting training - word vector length = {}, data points = {}".format(vector_size, data_point_count))


def pad_f(batch):
    return torch.nn.utils.rnn.pad_sequence(batch, batch_first=True), [len(x) for x in batch]


batch_size = 10
sentances = torch.utils.data.DataLoader(X, batch_size=batch_size, collate_fn=pad_f)

for i, (sample, lengths) in enumerate(sentances):
    optimizer.zero_grad()

    out = model(sample, lengths)
    values = y[i * batch_size: (i + 1) * batch_size].values
    loss = criterion(out, torch.tensor(values).unsqueeze(1))

    loss.backward()
    optimizer.step()

    if i % 20 == 1:
        print("{} out of {}, Sample \"{}\", score = {}, predicted score {},  loss = {}"
              .format(i, data_point_count // batch_size, df.title[indeces[i * batch_size]], y[i * batch_size], out[0][0],
                      loss))

model_to_file.save_model(model, "model_files/rnn_model")
model_to_file.save_model(word_table, "model_files/rnn_word_table")
