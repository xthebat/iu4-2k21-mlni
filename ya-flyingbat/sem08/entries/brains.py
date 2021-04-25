import numpy
import importlib
import keras.optimizers
from skimage import io, transform
from keras import backend as K
from utils.image import equalize_image_hist
from utils.metrics import mae, acc, recall, precision


class Brains(object):

    @classmethod
    def from_args(cls, args, data):
        return cls(
            model_name=args.model,
            data=data,
            optimizer_name=args.optimizer,
            weights_path=args.weights,
            learning_rate=args.learning_rate,
            decay=args.decay,
            epsilon=args.epsilon,
            subtract_image_mean=args.subtract_image_mean,
        )

    def __init__(
            self,
            model_name,
            data=None,
            optimizer_name=None,
            weights_path=None,
            learning_rate=None,
            decay=None,
            epsilon=None,
            subtract_image_mean=None,
    ):
        self.comp_graph = None

        self.data = data

        self.subtract_image_mean = subtract_image_mean

        print("Importing model...")
        package = importlib.import_module("models.%s" % model_name)

        print("Creating model %s" % model_name)
        self.model = package.create(self.data.num_class)

        self.model_outputs = self.model.output_shape[1]
        if self.model_outputs != self.data.num_class:
            raise "Wrong number of classes %d != %d" % (self.model_outputs, self.data.num_class)

        if optimizer_name is not None and learning_rate is not None and decay is not None and epsilon is not None:
            optimizer_constructor = getattr(keras.optimizers, optimizer_name)
            # optimizer = SGD(lr=args.learning_rate, decay=args.decay, momentum=0.9, nesterov=True)
            # optimizer = Adagrad(lr=args.learning_rate, decay=args.decay, epsilon=args.epsilon)
            # optimizer = Adam(lr=args.learning_rate, decay=args.decay, epsilon=args.epsilon)
            # optimizer = RMSprop(lr=args.learning_rate, decay=args.decay, epsilon=args.epsilon, rho=0.9)
            self.optimizer = optimizer_constructor(lr=learning_rate, decay=decay, epsilon=epsilon)
        else:
            self.optimizer = keras.optimizers.SGD()

        if weights_path is not None:
            print("Loading weights from %s" % weights_path)
            self.model.load_weights(weights_path)

        self.model_outputs = self.model.output_shape[1]
        if self.model_outputs != self.data.num_class:
            raise "Wrong number of classes %d != %d" % (self.model_outputs, self.data.num_class)

        print("Compile model...")
        self.model.compile(
            optimizer=self.optimizer,
            loss='categorical_crossentropy',
            metrics=[mae, acc, recall, precision]
        )

        self.img_width = self.model.layers[0].input_shape[2]
        self.img_height = self.model.layers[0].input_shape[3]
        print("width = %d height = %d" % (self.img_width, self.img_height))

    @staticmethod
    def convert_image(img):
        x = numpy.asarray(img, dtype=numpy.float32)
        x = x.transpose(2, 0, 1)
        return numpy.expand_dims(x, axis=0)

    def preprocess_image(self, img):
        if len(img.shape) == 3:
            result = img.copy()
        elif len(img.shape) == 4:
            result = img[0, :, :, :]
        else:
            raise ValueError("Wrong input image shape == 3 or == 4")

        if self.data.equalize_hist:
            for channel in range(result.shape[0]):
                result[channel, :, :] = equalize_image_hist(result[channel, :, :], 256)

        if self.data.mean is not None:
            result -= self.data.mean

        if self.subtract_image_mean:
            mean = result.mean(axis=(1, 2))
            result[0, :, :] -= mean[0]
            result[1, :, :] -= mean[1]
            result[2, :, :] -= mean[2]

        if len(img.shape) == 4:
            return numpy.expand_dims(result, axis=0)
        else:
            return result

    def init_comp_graph_if_req(self):
        if self.comp_graph is None:
            outputs = [layer.output for layer in self.model.layers]          # all layer outputs
            self.comp_graph = list()
            for k, output in enumerate(outputs):
                func = K.function([self.model.input] + [K.learning_phase()], [output])
                self.comp_graph.append(func)
                print("#%d -> %s output = %s" % (k, func, output))

    def calc_layer_output(self, image, number):
        self.init_comp_graph_if_req()
        result = self.comp_graph[number]([image, 1.0])
        return result[0][0]

    def calc_layer_outputs(self, image):
        self.init_comp_graph_if_req()
        return [self.calc_layer_output(image, k) for k in range(len(self.comp_graph))]

    def load_image(self, path, grayscale=False):
        image = io.imread(path, grayscale)
        return transform.resize(image, (self.img_width, self.img_height), preserve_range=True).astype('uint8')

    def load_and_predict(self, path, grayscale=False, convert=True, preprocess=True, verbose=False):
        image = self.load_image(path, grayscale)
        return self.predict_image(image, convert, preprocess, verbose), image

    def predict_image(self, image, convert=True, preprocess=True, verbose=False):
        if convert:
            image = self.convert_image(image)
        if preprocess:
            image = self.preprocess_image(image)
        return self.predict(image, verbose)

    def predict(self, data, verbose=False):
        return self.model.predict(data, verbose=verbose)

    def sorted(self, probabilities):
        return [index for (prob, index) in sorted(zip(probabilities, self.data.indexes), reverse=True)]