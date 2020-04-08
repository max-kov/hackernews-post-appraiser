import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression
import joblib


def get_stopwords():
    import nltk
    nltk.download('stopwords')
    from nltk.corpus import stopwords
    return stopwords.words("english")


def get_tokenizer():
    import nltk
    nltk.download('udhr')
    from nltk.tokenize import TweetTokenizer

    return TweetTokenizer(preserve_case=False)


def get_stemmer():
    import nltk
    nltk.download('udhr')
    from nltk.stem import SnowballStemmer
    return SnowballStemmer("english", ignore_stopwords=True)


df = pd.read_csv("data.csv")
df = df.dropna(subset=["title"])

vectorizer = TfidfVectorizer(stop_words=get_stopwords(), tokenizer=tokenizer.tokenize, preprocessor=stemmer.stem)
X = vectorizer.fit_transform(df.title)

scaler = StandardScaler()
y = scaler.fit_transform(df[["score"]])

model = LinearRegression().fit(X, y.ravel())

joblib.dump(model, "model.sav")
joblib.dump(scaler, "scaler.sav")
joblib.dump(vectorizer, "vectorizer.sav")
