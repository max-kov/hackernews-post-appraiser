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
