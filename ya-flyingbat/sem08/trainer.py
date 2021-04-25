import resource
import datetime
import json
import os
import sys
from keras.callbacks import ModelCheckpoint, Callback, ReduceLROnPlateau
from entries import arguments
from entries.brains import Brains
from entries.data import Data


LOGGING_DIR = "temp/output/history/"
EXPERIMENTS_LOG_PATH = "temp/output/experiments.json"


class MemoryCallback(Callback):
    def on_epoch_end(self, epoch, logs=None):
        vmem = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
        print("\nCurrent memory usage: %d kb" % (vmem / 1024))


class LoggingCallback(Callback):
    """Callback that logs message at end of epoch."""

    def __init__(self, directory, prefix):
        Callback.__init__(self)
        self.prefix = prefix
        self.batch_filename = os.path.join(directory, prefix) + "_batch.txt"
        self.epoch_filename = os.path.join(directory, prefix) + "_epoch.txt"
        self.batch_file = open(self.batch_filename, "wt")
        self.epoch_file = open(self.epoch_filename, "wt")
        self.print_batch_header = False
        self.print_epoch_header = False
        self.epoch = -1

    @staticmethod
    def header(where, logs):
        where.write(", ".join(logs.keys()) + "\n")

    @staticmethod
    def log_it(where, logs):
        where.write(", ".join("%f" % v for v in logs.values()) + "\n")
        where.flush()

    def on_batch_end(self, batch, logs=None):
        if not self.print_batch_header:
            self.header(self.batch_file, logs)
            self.print_batch_header = True
        self.log_it(self.batch_file, logs)

    def on_epoch_end(self, epoch, logs=None):
        if not self.print_epoch_header:
            self.header(self.epoch_file, logs)
            self.print_epoch_header = True
        self.log_it(self.epoch_file, logs)


def create_experiment_record(
        args=None,
        prefix=None,
        weights_pattern=None,
        train_batch_log=None,
        train_epoch_log=None,
        rid=0):
    date = datetime.datetime.now()
    return {
        "id": rid,
        "datetime": date.strftime("%Y-%m-%d %H:%M:%S"),
        "prefix": prefix,
        "train_batch_log": train_batch_log,
        "train_epoch_log": train_epoch_log,
        "weights_pattern": weights_pattern,
        "args": vars(args) if args is not None else args
    }


def save_experiments_log(experiments_path, history):
    data = json.dumps(history, indent=4, sort_keys=True)
    with open(experiments_path, "wt") as f:
        f.write(data)


def load_experiments_log(experiments_path):
    if not os.path.isfile(experiments_path):
        history = [create_experiment_record()]
        save_experiments_log(experiments_path, history)
    with open(experiments_path, "rt") as f:
        history = json.loads(f.read())
    return history


def append_experimental_log(experiments_path, record):
    history = load_experiments_log(experiments_path)
    record["id"] = history[-1]["id"] + 1
    history.append(record)
    save_experiments_log(experiments_path, history)


def main(argv):
    fit_callbacks = []

    args = arguments.parse(argv, train=True)
    data = Data.from_args(args, train=True)
    brains = Brains.from_args(args, data)

    print(f"Loading data "
          f"train[BS={args.train_batch_size}]={args.train_path} and "
          f"test[BS={args.validation_batch_size}]={args.validation_path}")

    train_generator = data.generator(
        directory=args.train_path,
        width=brains.img_width,
        height=brains.img_height,
        batch_size=args.train_batch_size,
        preprocess_image=brains.preprocess_image,
        horizontal_flip=args.horizontal_flip,
        vertical_flip=args.vertical_flip,
        save_to_dir=args.save_to_dir,
        rotation_range=args.rotation_range,
        width_shift_range=args.width_shift_range,
        height_shift_range=args.height_shift_range,
    )

    validation_generator = data.generator(
        directory=args.validation_path,
        width=brains.img_width,
        height=brains.img_height,
        batch_size=args.validation_batch_size,
        preprocess_image=brains.preprocess_image,
    )

    history = load_experiments_log(EXPERIMENTS_LOG_PATH)
    exp_id = history[-1]["id"] + 1

    fit_callbacks.append(MemoryCallback())

    weights_pattern = "%s/%s-c%d-id%d-{epoch:02d}-{val_acc:.2f}.hdf5" % \
                      (args.snapshots, args.model, brains.data.num_class, exp_id)
    fit_callbacks.append(ModelCheckpoint(
        filepath=weights_pattern,
        monitor='val_acc',
        verbose=1,
        save_best_only=True,
        mode='max'
    ))

    if args.lr_monitor is not None:
        fit_callbacks.append(ReduceLROnPlateau(
            monitor=args.lr_monitor,
            verbose=1,
            factor=args.lr_factor,
            patience=args.lr_patience,
            min_lr=args.min_lr,
            epsilon=args.lr_epsilon,
        ))

    prefix = datetime.datetime.now().strftime("%Y%m%d%H%M") + "_%s_%s" % (args.model, args.optimizer)
    logger = LoggingCallback(directory=LOGGING_DIR, prefix=prefix)
    fit_callbacks.append(logger)

    record = create_experiment_record(
        args=args, prefix=prefix,
        weights_pattern=weights_pattern,
        train_batch_log=logger.batch_filename,
        train_epoch_log=logger.epoch_filename)
    record["id"] = exp_id
    history.append(record)
    save_experiments_log(EXPERIMENTS_LOG_PATH, history)

    print("Training model... history will be with prefix %s" % prefix)

    brains.model.fit_generator(
        generator=train_generator,
        steps_per_epoch=args.steps_per_epoch,
        epochs=args.epochs,
        validation_data=validation_generator,
        validation_steps=args.validation_steps,
        callbacks=fit_callbacks,
    )


if __name__ == "__main__":
    main(sys.argv[1:])
