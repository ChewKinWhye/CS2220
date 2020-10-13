from utils.assignment1.data import load_fast_data
from utils.assignment1.model import feed_forward_tis
from utils.assignment1.evaluate import evaluation_metrics_float
from sklearn.model_selection import train_test_split
from tensorflow.keras.callbacks import EarlyStopping
import numpy as np


if __name__=="__main__":
    X_pos, y_pos = load_fast_data("Dataset/Assignment1/pos.fasta")
    X_neg, y_neg = load_fast_data("Dataset/Assignment1/neg.fasta")
    X = np.concatenate((X_pos, X_neg), axis=0)
    y = np.concatenate((y_pos, y_neg), axis=0)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    print(f"Train shape: {X_train.shape}")
    model = feed_forward_tis()
    es = EarlyStopping(monitor='val_loss', mode='min', patience=5)
    model.fit(X_train, y_train, epochs=30, batch_size=128, validation_split=0.2, callbacks=[es])
    y_predictions = model.predict(X_test)
    metrics = evaluation_metrics_float(y_test, y_predictions)
    print(metrics)
