from keras import metrics
from keras import backend as K


def mae(y_true, y_pred):
    return metrics.mean_absolute_error(y_true, y_pred)


def acc(y_true, y_pred):
    return metrics.categorical_accuracy(y_true, y_pred)


def precision(y_true, y_pred):
    """
    Precision metric.
    Only computes a batch-wise average of precision.
    Computes the precision, a metric for multi-label classification of
    how many selected items are relevant.
    """
    true_positives = K.sum(K.round(K.clip(y_true * y_pred, 0, 1)))
    predicted_positives = K.sum(K.round(K.clip(y_pred, 0, 1)))
    return true_positives / (predicted_positives + K.epsilon())


def recall(y_true, y_pred):
    """
    Recall metric.
    Only computes a batch-wise average of recall.
    Computes the recall, a metric for multi-label classification of
    how many relevant items are selected.
    """
    true_positives = K.sum(K.round(K.clip(y_true * y_pred, 0, 1)))
    possible_positives = K.sum(K.round(K.clip(y_true, 0, 1)))
    return true_positives / (possible_positives + K.epsilon())


def rand_rel(y_true, y_pred, outputs):
    """
    Accuracy relative to random prediction
    """
    return outputs * metrics.categorical_accuracy(y_true, y_pred)