from torch import nn as nn


class RNNModel(nn.Module):
    def __init__(self, input_size):
        super(RNNModel, self).__init__()

        self.input_size = input_size
        self.hidden_size = 1000
        self.embedding_size = 1000
        self.l2_size = 100

        self.embedding = nn.Embedding(self.input_size, self.embedding_size)
        self.hidden = nn.GRU(self.embedding_size, self.hidden_size, batch_first=True)
        self.hidden_to_l2 = nn.Linear(self.hidden_size, self.l2_size)
        self.hidden_to_out = nn.Linear(self.l2_size, 1)

    def forward(self, input_sentence, lengths):
        embeddings = self.embedding(input_sentence)
        packed = nn.utils.rnn.pack_padded_sequence(embeddings, lengths, batch_first=True, enforce_sorted=False)
        _, hidden = self.hidden(packed)
        l2 = self.hidden_to_l2(hidden[0])
        out = self.hidden_to_out(l2).double()

        return out