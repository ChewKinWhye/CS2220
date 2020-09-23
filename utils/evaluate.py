from sklearn.metrics import accuracy_score, recall_score, precision_score


def evaluation_metrics(true, pred):
    return recall_score(true, pred), precision_score(true, pred), accuracy_score(true, pred)
