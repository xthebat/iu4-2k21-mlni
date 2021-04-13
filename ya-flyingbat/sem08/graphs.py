import random

from matplotlib import pyplot as plt
import numpy as np


def tp(model, real):
    return np.sum(model == real)


def fn(model, real):
    return np.sum(real + 0 - model + 0 > 0)


def fp(model, real):
    return np.sum(model + 0 - real + 0 > 0)


def recall(model, real):
    tp0 = tp(model, real)
    fn0 = fn(model, real)
    return tp0 / (tp0 + fn0)


def precision(model, real):
    tp0 = tp(model, real)
    fp0 = fp(model, real)
    return tp0 / (tp0 + fp0)


def main():
    points = 100

    numbers = np.array([random.randint(0, points - 1) for _ in range(1000)])

    # model = np.array([random.randint(0, 99) > 5 for _ in range(10)])
    real = numbers > points / 2

    precisions = []
    recalls = []
    f1score = []
    for threshold in range(points):
        good = numbers - 25 > threshold
        p = precision(good, real)
        r = recall(good, real)
        precisions.append(p)
        recalls.append(r)
        f1score.append(2 * r * p / (r + p))

    plt.plot(precisions)
    plt.plot(recalls)
    plt.plot(f1score)
    plt.show()


if __name__ == '__main__':
    main()
