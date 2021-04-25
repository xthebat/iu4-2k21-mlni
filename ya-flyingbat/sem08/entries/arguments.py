import argparse


def parse(argv, train=True):
    parser = argparse.ArgumentParser(description='Trainer for CNN models')

    parser.add_argument('-o', '--optimizer', help='Optimizer name', required=train, type=str)
    parser.add_argument('-lr', '--learning_rate', help='Learning rate', default=0.0001, type=float)
    parser.add_argument('-eps', '--epsilon', help='Epsilon?', default=1e-8, type=float)
    parser.add_argument('-d', '--decay', help='Learning rate decay over each update.', default=1e-6, type=float)

    parser.add_argument('-m', '--model', help='Model name', required=True, type=str)
    parser.add_argument('-w', '--weights', help='Path to load weights', required=not train, type=str)
    parser.add_argument('-s', '--snapshots', help='Path to store weights snapshot', required=train, type=str)

    parser.add_argument('-tbs', '--train_batch_size', help='Size of training batch', default=14, type=int)
    parser.add_argument('-vbs', '--validation_batch_size', help='Size of validation batch', default=1, type=int)
    parser.add_argument('-tp', '--train_path', help='Path to images for training set', required=train)
    parser.add_argument('-vp', '--validation_path', help='Path to images for validation set', required=True)

    parser.add_argument(
        '-spe', '--steps_per_epoch',
        help='Total number of steps (batches of samples)',
        default=100, type=int)
    parser.add_argument(
        '-e', '--epochs',
        help='Total number of iterations on the data.',
        default=100, type=int)

    parser.add_argument(
        '-vs', '--validation_steps',
        help="Number of steps to yield from validation generator at the end of every epoch.",
        default=100, type=int)

    parser.add_argument('-eqh', '--equalize_hist', help='Histogram equalization', default=False, action='store_true')
    parser.add_argument('-imn', '--subtract_image_mean', help='Subtract image mean', default=False, action='store_true')
    parser.add_argument('-smn', '--subtract_dataset_mean', help='Subtract dataset mean', default=False, action='store_true')
    parser.add_argument('--mean', nargs='+', help='Explicitly specify images mean to subtract it')

    parser.add_argument('-rr', '--rotation_range', help="Degree range for random rotations", default=0.0, type=float)
    parser.add_argument('-wsr', '--width_shift_range', help="Range for random horizontal shifts (fraction of total width)", default=0.0, type=float)
    parser.add_argument('-hsr', '--height_shift_range', help="Range for random vertical shifts (fraction of total height)", default=0.0, type=float)
    parser.add_argument(
        '-hf', '--horizontal_flip',
        help='whether to randomly flip images horizontally',
        default=False, action='store_true')
    parser.add_argument(
        '-vf', '--vertical_flip',
        help='whether to randomly flip images vertically',
        default=False, action='store_true')

    parser.add_argument('--save_to_dir', help="Optional directory where to save the pictures being yielded.")
    parser.add_argument('--save_prefix', help="String prefix to use for saving sample", default='')

    parser.add_argument(
        '-lrmon', '--lr_monitor',
        help='Enable learning rate monitor and quantity to be monitored.',
        default=None, required=False, type=str
    )
    parser.add_argument(
        '-lrf', '--lr_factor',
        help='factor by which the learning rate will be reduced. new_lr = lr * factor',
        default=0.5, required=False, type=float
    )
    parser.add_argument(
        '-lrp', '--lr_patience',
        help='number of epochs with no improvement after which learning rate will be reduced.',
        default=5, required=False, type=int
    )
    parser.add_argument(
        '-lrmin', '--min_lr',
        help='lower bound on the learning rate.',
        default=0, required=False, type=float
    )
    parser.add_argument(
        '-lre', '--lr_epsilon',
        help='threshold for measuring the new optimum, to only focus on significant changes.',
        default=1e-4, required=False, type=float
    )

    result = parser.parse_args(argv)

    print(result)

    return result
