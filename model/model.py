import pathlib

import joblib
import pandas as pd
import torch

from tools import nltk_tools
from torch_models.rnn import RNNModel
from word_level_torch_vectorizer import process_titles


class ModelRunner:

    def __init__(self):
        self.model_folder = pathlib.Path(__file__).parent / "model_files"
        self.model_type = "rnn"
        self.model_func = {"rnn": self.run_RNN,
                           "linreg": self.run_linear_reg}

        nltk_tools.install_deps()
        if self.model_type == "rnn":
            model_state = torch.load(self.model_folder / "rnn_model.sav", map_location=torch.device('cpu'))
            self.model = RNNModel(10000)
            self.model.load_state_dict(model_state)

            self.word_list = joblib.load(self.model_folder / "rnn_word_table.sav")
        else:
            self.model = joblib.load(self.model_folder / "model.sav")
            self.vectorizer = joblib.load(self.model_folder / "vectorizer.sav")
            self.scaler = joblib.load(self.model_folder / "scaler.sav")

    def predict(self, title: str):
        return self.model_func.get(self.model_type)(title)

    def run_linear_reg(self, title: str):
        return self.scaler.inverse_transform(self.model.predict(self.vectorizer.transform([title])))[0]

    def run_RNN(self, title):
        vector_length = len(self.word_list)
        X, _, _ = process_titles(pd.Series([title]), vector_length, word_table=self.word_list)
        title_lengths = [len(X[0])]
        title_vectors = X[0].unsqueeze(0)
        return self.model(title_vectors, title_lengths)[0][0].item()
