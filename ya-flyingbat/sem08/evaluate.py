import glob
import os
import shutil
import sys

import numpy
import scipy.misc
from vis.visualization import overlay
from vis.visualization.saliency import visualize_saliency

from entries import arguments
from entries.brains import Brains
from entries.data import Data
from utils.image import highlight

__author__ = "the bat"


class Statistics(object):

    NAME_SIZE = 5

    def __init__(self, data):
        self.data = data
        self.top1 = 0
        self.top2 = 0
        self.top3 = 0
        self.total_test = 0
        self.num_class = data.num_class
        self.confusion = numpy.zeros((self.data.num_class, self.data.num_class))

    def calc_prediction_matrix(self):
        result = numpy.zeros((self.data.num_class, self.data.num_class), numpy.float32)
        for k in range(self.confusion.shape[0]):
            total = numpy.sum(self.confusion[k, :])
            if total != 0.0:
                result[k, :] = self.confusion[k, :] / float(total)
        return result

    def generate_table_names(self):
        return " ".join(self.name(self.data.labels[k]) for k in range(len(self.data.labels)))

    def print_precision_recall(self):
        def calc(value1, value2):
            if value1 == 0.0 and value2 == 0.0:
                return numpy.nan
            elif value2 == 0.0:
                return numpy.inf
            else:
                return value1 / value2

        precision = dict()
        recall = dict()
        f1score = dict()
        gmeas = dict()

        for label in self.data.labels:
            i = self.data.classes[label]

            true_positive = float(self.confusion[i][i])
            all_positive = float(sum(self.confusion[i, :]))
            total_labeled = float(sum(self.confusion[:, i]))

            precision[label] = calc(true_positive, all_positive)
            recall[label] = calc(true_positive, total_labeled)
            f1score[label] = calc(2 * precision[label] * recall[label], precision[label] + recall[label])
            gmeas[label] = numpy.sqrt(precision[label] * recall[label])

        accuracy = sum(numpy.diag(self.confusion)) / sum(self.confusion.flatten())

        print("\n       Label  precision  recall  f1-score  g-meas")
        for label in self.data.labels:
            print("%12s %10.4f %7.4f %9.4f  %6.4f" %
                  (label, precision[label], recall[label], f1score[label], gmeas[label]))
        print("Accuracy = %.4f" % accuracy)

    @staticmethod
    def name(value, size=NAME_SIZE):
        if len(value) > size:
            value = value[:size]
        return Statistics.value(value, size)

    @staticmethod
    def value(value, size=NAME_SIZE):
        frmt = {int: "d", float: ".1f", str: "s", numpy.uint32: "d", numpy.float64: ".1f"}[type(value)]
        return ("%%%d%s" % (size, frmt)) % value

    def print_confusion_matrix(self):
        values_matrix = numpy.zeros((self.data.num_class, self.data.num_class), numpy.uint32)
        for k in range(self.confusion.shape[0]):
            values_matrix[k, :] = self.confusion[k, :]

        print("\nValues confusion matrix:")
        print("\n%s %s" % (self.name(" "), self.generate_table_names()))
        for r in range(values_matrix.shape[0]):
            values = " ".join([self.value((values_matrix[r, c])) for c in range(values_matrix.shape[1])])
            print("%s %s" % (self.name(self.data.labels[r]), values))

    def print_prediction_matrix(self):
        print("\nPercent confusion matrix:")
        print("\n%s %s" % (self.name(" "), self.generate_table_names()))
        percent_matrix = self.calc_prediction_matrix()
        for r in range(percent_matrix.shape[0]):
            values = " ".join([self.value(percent_matrix[r, c]*100.0) for c in range(percent_matrix.shape[1])])
            print("%s %s" % (self.name(self.data.labels[r]), values))

    def print_total_test(self):
        print("\nTotal images analyzed = %d" % self.total_test)

    def print_all(self):
        self.print_confusion_matrix()
        self.print_prediction_matrix()
        self.print_precision_recall()
        self.print_total_test()

    def update(self, guess, out, truth):
        brain_id = int(numpy.argmax(out))
        real_id = int(numpy.argmax(truth))

        brain_name = self.data.labels[brain_id]
        real_name = self.data.labels[real_id]

        self.total_test += 1

        self.confusion[real_id, brain_id] += 1

        if real_id in guess[0:1]:
            self.top1 += 1
        if real_id in guess[0:2]:
            self.top2 += 1
        if real_id in guess[0:3]:
            self.top3 += 1

        p1 = float(self.top1) / float(self.total_test) * 100.0
        p2 = float(self.top2) / float(self.total_test) * 100.0
        p3 = float(self.top3) / float(self.total_test) * 100.0
        sout = " ".join(map(lambda x: "%.2f" % x, out))
        print("#%4d [%s] top-k = %4.1f%% %4.1f%% %4.1f%% guess n/r -> <%2d>%15s/%-15s<%2d>" %
              (self.total_test, sout, p1, p2, p3, brain_id, brain_name, real_name, real_id))


def analyze(brains, generator):
    tmp = numpy.zeros((brains.data.total, 4096))
    for batch_number in range(brains.data.total):
        images, truths = next(generator)
        data = brains.calc_layer_output(images, 21)
        tmp[batch_number, :] = data
    scipy.misc.imsave('outfile.png', tmp)


def evaluate(brains, generator):
    print_batch_size_threshold = 10

    batch_size = generator.batch_size

    statistics = Statistics(brains.data)

    for batch_number in range(brains.data.total / batch_size + 1):
        if batch_size > print_batch_size_threshold:
            print("Generating %d images and truths from source for %d batch" % (batch_size, batch_number))

        images, truths = next(generator)

        if batch_size > print_batch_size_threshold:
            print("Evaluating model...")

        outs = brains.model.predict(images, verbose=batch_size > print_batch_size_threshold)

        del images

        for k in range(outs.shape[0]):
            truth = truths[k]
            out = outs[k]
            guess = brains.sorted(out)
            statistics.update(guess, out, truth)

        statistics.print_all()


def visualise(brains, input_directory, output_directory, input_extension=".jpg"):

    class_paths = glob.glob(os.path.join(input_directory, "*"))
    for class_path in class_paths:
        if os.path.isdir(class_path):
            label = class_path.split("/")[-1]
            full_directory = os.path.join(output_directory, label)
            print("Prepare output directory: %s" % full_directory)
            if os.path.isdir(full_directory):
                shutil.rmtree(full_directory)
            os.makedirs(full_directory)

    image_paths = glob.glob(os.path.join(input_directory, "*/*%s" % input_extension))
    # random.shuffle(image_paths)

    total = len(image_paths)
    for k, image_path in enumerate(image_paths):
        image_directory = os.path.dirname(image_path)
        image_name = os.path.basename(image_path)

        real_label = image_directory.split("/")[-1]
        real_id = brains.data.classes[real_label]

        image = brains.load_image(image_path)
        out = brains.predict_image(image, convert=True, preprocess=True)

        brain_id = int(numpy.argmax(out))
        brain_label = brains.data.labels[brain_id]

        vals = ", ".join(map(lambda x: "%.2f" % x, out.flatten()))
        print("#%3d/%d [%s] <%2d>%11s/%-11s<%2d> path = %s" %
              (k, total, vals, brain_id, brain_label, real_label, real_id, image_path))

        # The name of the layer we want to visualize (output layer)
        # layer_idx = len(brains.model.layers) - 1
        layer_idx = 22

        # Better results
        heatmap = visualize_saliency(brains.model, layer_idx, [brain_id], image)
        # Added standard overlay, mask overlay disabled if ovl_alpha == None
        result = highlight(
            image, heatmap,
            threshold=100,
            blur_kernel_size=(12, 12),
            fig_type="ellipsis",
            fig_min_size=12,
            ovl_alpha=None,
        )

        output_image_path = os.path.join(output_directory, real_label, "%s_%s" % (brain_label, image_name))
        scipy.misc.imsave(output_image_path, result)


def main(argv):
    args = arguments.parse(argv, train=False)
    brains = Brains.from_args(args, Data.from_args(args, train=False))

    generator = brains.data.generator(
        directory=args.validation_path,
        width=brains.img_width,
        height=brains.img_height,
        batch_size=args.validation_batch_size,
        preprocess_image=brains.preprocess_image,
        save_to_dir=args.save_to_dir,
        shuffle=False
    )

    # analyze(brains, generator)
    # evaluate(brains, generator)
    visualise(brains, input_directory=args.validation_path, output_directory="temp/evaluate/")


if __name__ == "__main__":
    main(sys.argv[1:])
