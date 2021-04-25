import numpy
from keras.preprocessing.image import ImageDataGenerator


class Data(object):

    @staticmethod
    def calc_mean(datagen, directory, batch_size=500):
        count = 0
        iterator = datagen.flow_from_directory(directory=directory, class_mode='categorical', batch_size=batch_size)
        mean = numpy.zeros(3, dtype=numpy.float64)
        for k in range(iterator.n / iterator.batch_size + 1):
            print("Calculating image mean for batch #%d with %d images" % (k + 1, batch_size))
            data = next(iterator)
            count += data[0].shape[0] * data[0].shape[1] * data[0].shape[2]
            mean += data[0].sum(axis=(0, 1, 2))
        return mean / count

    @staticmethod
    def analyze(args, train=True):
        datagen = ImageDataGenerator()
        directory = args.train_path if train else args.validation_path

        if args.subtract_dataset_mean:
            if args.mean is None:
                mean = Data.calc_mean(datagen, directory)
            else:
                mean = numpy.array(args.mean, dtype=numpy.float64)
            mean = mean.reshape((3, 1, 1))
        else:
            mean = None
        print("Images mean = %s" % mean.flatten())

        iterator = datagen.flow_from_directory(directory=directory, class_mode='categorical', batch_size=1)
        return iterator, mean

    @classmethod
    def from_args(cls, args, train):
        iterator, mean = cls.analyze(args, train)
        return cls(classes=iterator.class_indices, total=iterator.n, mean=mean, equalize_hist=args.equalize_hist)

    def __init__(self, classes, total, mean, equalize_hist):
        self.total = total
        self.mean = mean
        self.equalize_hist = equalize_hist
        self.classes = classes
        self.labels = [k for (k, v) in sorted(classes.items())]
        self.num_class = len(classes)
        self.indexes = sorted(classes.values())
        print(f"Data class count: {self.num_class}")

    @staticmethod
    def generator(
            directory,
            width, height,
            batch_size=5,
            preprocess_image=None,
            horizontal_flip=False,
            vertical_flip=False,
            save_to_dir=None,
            save_prefix="",
            shuffle=True,
            rotation_range=0.0,
            width_shift_range=0.0,
            height_shift_range=0.0,
    ):
        datagen = ImageDataGenerator(
            horizontal_flip=horizontal_flip,
            vertical_flip=vertical_flip,
            rotation_range=rotation_range,
            width_shift_range=width_shift_range,
            height_shift_range=height_shift_range,
            preprocessing_function=preprocess_image
        )

        return datagen.flow_from_directory(
            directory=directory,
            target_size=(width, height),
            batch_size=batch_size,
            class_mode='categorical',
            save_to_dir=save_to_dir,
            save_prefix=save_prefix,
            shuffle=shuffle
        )
