import nltk


def install_deps():
    nltk.download('stopwords')
    nltk.download('udhr')
    nltk.download('udhr')


def get_stopwords():
    from nltk.corpus import stopwords
    return stopwords.words("english")


def get_tokenizer():
    from nltk.tokenize import TweetTokenizer
    return TweetTokenizer(preserve_case=False)


def get_stemmer():
    from nltk.stem import SnowballStemmer
    return SnowballStemmer("english", ignore_stopwords=True)
