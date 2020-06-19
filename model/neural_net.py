import pandas as pd
from tools import model_to_file
import torch
import torch.nn as nn
import torch.optim as optim

from word_level_torch_vectorizer import process_titles

from model.torch_models.rnn import RNNModel

torch.manual_seed(0)

df = pd.read_csv("tools/data.csv")[:500]
df = df.dropna(subset=["title"])

vector_size = 10000

X, indeces, word_table = process_titles(df.title, vector_size)
y = df.score[indeces].reset_index(drop=True)
data = pd.concat([X, y], 1)

data_point_count = df.shape[0]
model = RNNModel(vector_size)

criterion = nn.SmoothL1Loss()
optimizer = optim.Adam(model.parameters())

print("Starting training - word vector length = {}, data points = {}".format(vector_size, data_point_count))


def pad_f(batch):
    X = [x[0] for x in batch]
    y = torch.Tensor([x[1] for x in batch]).double().unsqueeze(1)
    lengths = [len(x) for x in X]
    return torch.nn.utils.rnn.pad_sequence(X, batch_first=True), lengths, y


batch_size = 128
sentances = torch.utils.data.DataLoader(data.values, batch_size=batch_size, collate_fn=pad_f, shuffle=True)

for i, (sample, lengths, ys) in enumerate(sentances):
    optimizer.zero_grad()

    out = model(sample, lengths)
    loss = criterion(out, ys)

    loss.backward()
    optimizer.step()

    print("{} out of {}, Sample \"{}\", score = {}, predicted score {},  loss = {}"
          .format(i, data_point_count // batch_size, df.title[indeces[i * batch_size]], y[i * batch_size], out[0][0],
                  loss))

torch.save(model, "model_files/rnn_model.sav")
model_to_file.save_model(word_table, "model_files/rnn_word_table")
