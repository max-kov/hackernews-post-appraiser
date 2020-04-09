import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression

from tools import nltk_tools, model_to_file

df = pd.read_csv("tools/data.csv")
df = df.dropna(subset=["title"])

vectorizer = TfidfVectorizer(stop_words=nltk_tools.get_stopwords(),
                             tokenizer=nltk_tools.get_tokenizer().tokenize,
                             preprocessor=nltk_tools.get_stemmer().stem)
X = vectorizer.fit_transform(df.title)

scaler = StandardScaler()
y = scaler.fit_transform(df[["score"]])

model = LinearRegression().fit(X, y.ravel())

model_to_file.save_model(model, "model_files/model")
model_to_file.save_model(scaler, "model_files/scaler")
model_to_file.save_model(vectorizer, "model_files/vectorizer")
