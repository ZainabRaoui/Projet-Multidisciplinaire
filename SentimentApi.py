from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import pandas as pd
import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.text import tokenizer_from_json
import json
import tensorflow as tf
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
import pickle


# Charger le modèle et le tokenizer
MODEL_PATH = "lstmAnalyseSentiment.h5"
TOKENIZER_PATH = "tokenizer_config.json"

def load_tokenizer():
    with open(TOKENIZER_PATH, "r") as f:
        tokenizer_data = json.load(f)
    return tokenizer_from_json(tokenizer_data)

# Initialize FastAPI app
app = FastAPI()

# Add CORS middleware to allow requests from your Angular app
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4200"],  # Allow Angular frontend to make requests
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)

# Global variables for model and tokenizer
model = None
tokenizer = None
max_sequence_length = 100

# Pydantic model for predictions
class TextInput(BaseModel):
    text: str

@app.post("/load-data/")
async def load_data(file: UploadFile = File(...)):
    """Endpoint to load CSV data."""
    try:
        # Read the uploaded CSV file
        data = pd.read_csv(file.file)
        if 'text' not in data.columns or 'label' not in data.columns:
            raise HTTPException(status_code=400, detail="CSV must contain 'text' and 'label' columns.")
        return {"message": "Data loaded successfully.", "columns": data.columns.tolist()}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error loading data: {str(e)}")

@app.post("/preprocess/")
async def preprocess_data(file: UploadFile = File(...)):
    """Endpoint to preprocess text data."""
    try:
        data = pd.read_csv(file.file)
        texts = data['text'].astype(str).tolist()
        global tokenizer
        tokenizer = Tokenizer()
        tokenizer.fit_on_texts(texts)
        sequences = tokenizer.texts_to_sequences(texts)
        padded_sequences = pad_sequences(sequences, maxlen=max_sequence_length)
        return {"message": "Data preprocessed successfully.", "num_samples": len(padded_sequences)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error during preprocessing: {str(e)}")

@app.post("/train/")
async def train_model(file: UploadFile):
    try:
        # Charger les données CSV
        df = pd.read_csv(file.file)
        print("CSV loaded successfully")
        
        # Vérification des colonnes nécessaires
        if "text" not in df.columns or "sentiment" not in df.columns:
            raise HTTPException(
                status_code=400, detail="Le fichier CSV doit contenir les colonnes 'text' et 'sentiment'."
            )

        # Conversion des sentiments en valeurs numériques
        sentiment_map = {
            "positive": 1,
            "negative": 0,
            "neutral": 2
        }
        df["sentiment"] = df["sentiment"].map(sentiment_map)

        texts = df["text"].tolist()
        labels = df["sentiment"].tolist()

        # Charger le modèle et le tokenizer
        print("Loading model and tokenizer")
        tokenizer = load_tokenizer()
        model = load_model(MODEL_PATH)

        # Prétraitement des textes
        sequences = tokenizer.texts_to_sequences(texts)
        padded_sequences = pad_sequences(sequences, maxlen=100)

        # Réentraîner le modèle
        print("Training model")
        model.fit(padded_sequences, labels, epochs=5, batch_size=32)

        # Sauvegarder le modèle mis à jour
        model.save(MODEL_PATH)
        print("Model saved successfully")

        return JSONResponse(content={"message": "Modèle réentraîné avec succès."})
    except Exception as e:
        print(f"Error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error during training: {str(e)}")

@app.post("/predict/")
async def predict_sentiment(input: TextInput):
    """Endpoint to predict sentiment of a given text."""
    try:
        global model, tokenizer
        if model is None or tokenizer is None:
            raise HTTPException(status_code=400, detail="Model and tokenizer are not loaded.")

        sequence = tokenizer.texts_to_sequences([input.text])
        padded_sequence = pad_sequences(sequence, maxlen=max_sequence_length)
        prediction = model.predict(padded_sequence)
        sentiment = np.argmax(prediction, axis=1)[0]

        return {"text": input.text, "sentiment": int(sentiment)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error during prediction: {str(e)}")

@app.get("/download-model/")
async def download_model():
    """Endpoint to download the trained model and tokenizer."""
    try:
        return {"model_path": "sentiment_model.h5", "tokenizer_path": "tokenizer.pkl"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error during model download: {str(e)}")
