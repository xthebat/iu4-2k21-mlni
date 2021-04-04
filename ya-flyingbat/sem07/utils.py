import numpy as np
from numpy import ndarray


def softmax(x: ndarray) -> ndarray:
    return np.exp(x) / sum(np.exp(x))


# f*ck u np
def to2d(x: ndarray) -> ndarray:
    size = len(x.shape)
    assert size <= 2

    if size == 2:
        return x

    rows = x.shape[0]

    return np.reshape(x, (rows, 1))


def glue(*args: ndarray, axis) -> ndarray:
    return np.concatenate(args, axis=axis)
