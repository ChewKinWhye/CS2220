from sklearn.metrics import roc_curve, accuracy_score, recall_score, precision_score
import numpy as np


def evaluation_metrics_binary(true, pred):
    return recall_score(true, pred), precision_score(true, pred), accuracy_score(true, pred)


def evaluation_metrics_float(y_test, y_predicted):
    fpr, tpr, thresholds = roc_curve(y_test, y_predicted)

    optimal_idx = np.argmax(tpr - fpr)
    optimal_threshold = thresholds[optimal_idx]

    y_predicted_binary = [0 if i < optimal_threshold else 1 for i in y_predicted]

    accuracy = accuracy_score(y_test, y_predicted_binary)
    sensitivity = recall_score(y_test, y_predicted_binary)
    precision = precision_score(y_test, y_predicted_binary)
    return sensitivity, precision, accuracy
