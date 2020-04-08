import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression

import nltk_tools
import model_to_file

df = pd.read_csv("data.csv")
df = df.dropna(subset=["title"])

vectorizer = TfidfVectorizer(stop_words=nltk_tools.get_stopwords(),
                             tokenizer=nltk_tools.get_tokenizer().tokenize,
                             preprocessor=nltk_tools.get_stemmer().stem)
X = vectorizer.fit_transform(df.title)

scaler = StandardScaler()
y = scaler.fit_transform(df[["score"]])

model = LinearRegression().fit(X, y.ravel())

model_to_file.save_model(model, "model")
model_to_file.save_model(scaler, "scaler")
model_to_file.save_model(vectorizer, "vectorizer")
