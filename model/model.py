import joblib

model = joblib.load("tools/model.sav")
vectorizer = joblib.load("tools/vectorizer.sav")
scaler = joblib.load("tools/scaler.sav")

def predict(title):
    return scaler.inverse_transform(model.predict(vectorizer.transform([title])))[0]

