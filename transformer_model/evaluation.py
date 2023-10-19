import numpy as np
from scipy.stats import pearsonr, spearmanr
from sklearn.metrics import mean_absolute_error, f1_score, recall_score, precision_score


def macro_f1(y_true, y_pred):
    return f1_score(y_true, y_pred, average='macro')

def weighted_f1(y_true, y_pred):
    return f1_score(y_true, y_pred, average='weighted')

def print_stat(df, real_column, pred_column):
    predictions = df[pred_column].tolist()
    real_values = df[real_column].tolist()

    print()
    print("Weighted Recall {}".format(recall_score(real_values, predictions, average='weighted')))
    print("Weighted Precision {}".format(precision_score(real_values, predictions, average='weighted')))
    print("Weighter F1 Score {}".format(f1_score(real_values, predictions, average='weighted')))

    print("Macro F1 Score {}".format(f1_score(real_values, predictions, average='macro')))
