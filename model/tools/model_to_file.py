def save_model(object, obj_name):
    import joblib
    joblib.dump(object, "{}.sav".format(obj_name))