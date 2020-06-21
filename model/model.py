import joblib
import pathlib
from torch_models.rnn import RNNModel
import torch
import pandas as pd
from word_level_torch_vectorizer import process_titles
from tools import nltk_tools

model_folder = pathlib.Path(__file__).parent / "model_files"
nltk_tools.install_deps()

model = torch.load(model_folder / "rnn_model.sav")
word_list = joblib.load(model_folder / "rnn_word_table.sav")


def predict(title):
    return run_RNN(title)


def run_linear_reg(title):
    model = joblib.load(model_folder / "model.sav")
    vectorizer = joblib.load(model_folder / "vectorizer.sav")
    scaler = joblib.load(model_folder / "scaler.sav")
    return scaler.inverse_transform(model.predict(vectorizer.transform([title])))[0]


def run_RNN(title):
    X, _, _ = process_titles(pd.Series([title]), len(word_list), word_table=word_list)
    return model(X[0].unsqueeze(0), [len(X[0])])[0][0].item()
