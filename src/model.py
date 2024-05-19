import pickle
import logging
from sklearn.feature_extraction.text import TfidfVectorizer

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()


def load_model():
    logger.info("Loading model...")

    with open("./ml/vectorizer.pk", "rb") as openfile:
        vect = pickle.load(openfile)
    vocab = vect.vocabulary_
    with open("./ml/model.pk", "rb") as openfile:
        xgb_cl = pickle.load(openfile)
    vect2 = TfidfVectorizer(vocabulary=vocab)

    return xgb_cl, vect2


def predict(transformer: TfidfVectorizer, model, name: str) -> bool:
    try:
        logger.info("Classifying...")
        data = transformer.fit_transform([name])
        prediction = model.predict(data)
        logger.info(f"Prediction: {prediction[0]}")
        return bool(prediction[0])
    except Exception as e:
        logger.error(f"Failed: {e}")
        return False
