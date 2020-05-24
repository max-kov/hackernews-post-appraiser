import joblib
import pathlib

model_folder = pathlib.Path(__file__).parent / "model_files"
model = joblib.load(model_folder / "model.sav")
vectorizer = joblib.load(model_folder / "vectorizer.sav")
scaler = joblib.load(model_folder / "scaler.sav")


def predict(title):
    return scaler.inverse_transform(model.predict(vectorizer.transform([title])))[0]