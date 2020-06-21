import pandas as pd
from tools import model_to_file
import torch
import torch.nn as nn
import torch.optim as optim

from word_level_torch_vectorizer import process_titles

from torch_models.rnn import RNNModel

torch.manual_seed(0)


def resample_dataset(data):
    cutoff_score = 3
    rescale_size = data[data.score == cutoff_score].count().iloc[0]
    resampled_dataset = data[data.score >= cutoff_score]

    for i in range(1, cutoff_score):
        data_for_score = data[data.score == i]
        resampled_dataset = pd.concat([resampled_dataset, data_for_score.sample(rescale_size)])

    return resampled_dataset


df = pd.read_csv("tools/data.csv")
df = df.dropna(subset=["title"])

vector_size = 10000

X, indeces, word_table = process_titles(df.title, vector_size)
y = df.score[indeces].reset_index(drop=True)
data = pd.concat([X, y], 1)
data = resample_dataset(data)

data_point_count = data.shape[0]
model = RNNModel(vector_size)

criterion = nn.SmoothL1Loss()
optimizer = optim.Adam(model.parameters())

print("Starting training - word vector length = {}, data points = {}".format(vector_size, data_point_count))


def pad_f(batch):
    X = [x[0] for x in batch]
    y = torch.tensor([x[1] for x in batch]).double().unsqueeze(1)
    lengths = [len(x) for x in X]
    return torch.nn.utils.rnn.pad_sequence(X, batch_first=True), lengths, y


batch_size = 64
n_of_epochs = 20
sentances = torch.utils.data.DataLoader(data.values, batch_size=batch_size, collate_fn=pad_f, shuffle=True)
model_to_file.save_model(word_table, "model_files/rnn_word_table")

for epoch in range(n_of_epochs):
    print("epoch {}:".format(epoch))
    i = 0
    for sample, lengths, ys in sentances:
        optimizer.zero_grad()

        out = model(sample, lengths)
        loss = criterion(out, ys)

        loss.backward()
        optimizer.step()

        if i%100==0:
            print("Iter = {}, score = {}, predicted score {},  loss = {}".format(i, ys[0][0], out[0][0],loss))

        i+=1

    torch.save(model, "model_files/rnn_model.sav".format(epoch))
