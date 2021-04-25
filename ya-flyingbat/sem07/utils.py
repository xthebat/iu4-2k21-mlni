import numpy as np
import scipy.special
from numpy import ndarray


def softmax(x: ndarray) -> ndarray:
    return np.exp(x) / sum(np.exp(x))
    # return scipy.special.softmax(x)


# f*ck u np
def to2d(x: ndarray) -> ndarray:
    return np.reshape(x, (x.size, 1)) if len(x.shape) == 1 else x


def glue(*args: ndarray, axis) -> ndarray:
    return np.concatenate(args, axis=axis)
