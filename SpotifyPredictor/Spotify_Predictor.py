# spotify_predictor.py

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.pipeline import make_pipeline
from sklearn.metrics import accuracy_score, ConfusionMatrixDisplay
import matplotlib.pyplot as plt


# ─── 1. Load Data ────────────────────────────────────────────────────────────

def load_data(filepath: str) -> (pd.DataFrame, pd.Series):
    """
    • Read CSV from `filepath` using the columns:
        ["popularity","danceability","energy","loudness","speechiness",
         "acousticness","instrumentalness","liveness","valence","tempo"]
    • Drop missing values
    • Create `banger` = (popularity >= 70)
    • Return X (drop popularity & banger) and y (banger)
    """
    # TODO: implement loading, cleaning, and label creation
    
    df = pd.read_csv(filepath, usecols=[
        "popularity", "danceability", "energy", "loudness", "speechiness",
        "acousticness", "instrumentalness", "liveness", "valence", "tempo"
    ])
    df.dropna(inplace=True)
    df['banger'] = df['popularity'] >= 70
    X = df.drop(columns=['popularity', 'banger'])
    y = df['banger']
    return X, y


# ─── 2. Build Pipeline ───────────────────────────────────────────────────────

def build_pipeline() -> make_pipeline:
    """
    • Standardize features
    • RandomForestClassifier(n_estimators=200,
                             class_weight="balanced",
                             random_state=42)
    • Return the assembled pipeline
    """
    # TODO: construct and return the sklearn Pipeline
    
    scaler = StandardScaler()
    rf = RandomForestClassifier(n_estimators=200, class_weight="balanced", random_state=42)
    pipe = make_pipeline(scaler, rf)
    return pipe


# ─── 3. Train & Evaluate ────────────────────────────────────────────────────

def train_and_evaluate(pipe, X_train, X_test, y_train, y_test) -> None:
    """
    • Fit `pipe` on X_train, y_train
    • Predict on X_test
    • Print accuracy
    • Display confusion matrix (Greens colormap)
    """
    # TODO: fit, predict, print accuracy, plot confusion matrix
    pipe.fit(X_train, y_train)
    y_pred = pipe.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    print(f"Accuracy: {accuracy:.2f}")


# ─── 4. Live Demo ────────────────────────────────────────────────────────────

def live_demo(pipe, feature_names: list[str]) -> None:
    """
    • Loop:
      – Read a line of 9 numeric feature values (danceability…tempo)
      – If blank, break
      – Validate input length
      – Build DataFrame with `feature_names`
      – Compute proba = pipe.predict_proba(df_live)[0,1]
      – Label = "BANGER" if proba > threshold else "Meh"
      – Print label and probability
    """
    # TODO: implement user prompts and live prediction
    input_data = input("Enter 9 feature values separated by commas: ")
    if not input_data.strip():
        return
    feature_values = list(map(float, input_data.split(' ')))
    if len(feature_values) != 9:
        print("Invalid input length. Please enter exactly 9 values.")
        return
    df_live = pd.DataFrame([feature_values], columns=feature_names)
    proba = pipe.predict_proba(df_live)[0, 1]
    label = "BANGER" if proba > 0.5 else "Meh"
    print(f"Label: {label}, Probability: {proba:.2f}")


# ─── 5. Main ────────────────────────────────────────────────────────────────

def main() -> None:
    """Orchestrate loading, splitting, pipeline, evaluation, and demo."""
    # 1) Load data
    # 2) Split (test_size=0.3, stratify=y, random_state=42)
    # 3) Build pipeline
    # 4) Train & evaluate
    # 5) Run live demo
    print("Loading data...")
    X,y = load_data("./dataset.csv")
    
    print("Splitting data...")
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, stratify=y, random_state=42)
    
    print("Building pipeline...")
    pipe = build_pipeline()
    
    print("Training and evaluating...")
    train_and_evaluate(pipe, X_train, X_test, y_train, y_test)
    feature_names = X.columns.tolist()
    
    print("Running live demo...")
    while True:
        live_demo(pipe, feature_names)
        cont = input("Do you want to continue? (y/n): ").strip().lower()
        if cont != 'y':
            break
    

if __name__ == "__main__":
    main()
