import pandas as pd
import string

import nltk
nltk.download('stopwords')
nltk.download('udhr')

from nltk.corpus import stopwords 
from nltk.tokenize import TweetTokenizer
from nltk.stem import SnowballStemmer 

stop_words = stopwords.words("english")
df = pd.read_csv("data.csv")

translator = str.maketrans("", "", string.punctuation) 
tokenizer = TweetTokenizer(preserve_case=False)
stemmer = SnowballStemmer("english", ignore_stopwords=True)

df = df.dropna(subset=["title"])

from sklearn.feature_extraction.text import TfidfVectorizer

vectorizer = TfidfVectorizer(stop_words=stop_words, tokenizer=tokenizer.tokenize, preprocessor=stemmer.stem)
X = vectorizer.fit_transform(df.title)

from sklearn.preprocessing import StandardScaler

scaler = StandardScaler()
y = scaler.fit_transform(df[["score"]])

from sklearn.linear_model import LinearRegression

model = LinearRegression().fit(X,y.ravel())

import joblib

joblib.dump(model, "model.sav")
