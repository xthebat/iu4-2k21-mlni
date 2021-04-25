import numpy as np
from keras import backend as K
from keras.layers.convolutional import MaxPooling2D, Conv2D
from keras.layers.core import Dense, Dropout, Activation, Flatten
from keras.layers.normalization import BatchNormalization
from keras.models import Sequential
from keras.regularizers import l2


def Caffenet_initialization(shape, name=None):
    """
    Custom weights initialization
    From Convolution2D:
    weights: list of Numpy arrays to set as initial weights.
            The list should have 2 elements, of shape `(input_dim, output_dim)`
            and (output_dim,) for weights and biases respectively.
    From train_val.prototxt
    weight_filler
    {
      type: "gaussian"
      std: 0.01
    }
    bias_filler
    {
      type: "constant"
      value: 0
    }
    Si pasamos esta funcion en el parametro init, pone este peso a las W y las b las deja a 0 (comprobado leyendo el codigo de Keras)
    """
    mu, sigma = 0, 0.01
    return K.variable(np.random.normal(mu, sigma, shape), name=name)


def create(outputs):
    """
    Caffe also allows you to choose between L2 regularization (default) and L1 regularization, by setting
    regularization_type: "L1"
    En Caffenet tenemos:     weight_decay: 0.0005
    """

    weight_decay = 0.0005

    model = Sequential()

    # Conv1
    model.add(Conv2D(
        filters=96,
        kernel_size=(11, 11),
        padding='valid',
        input_shape=(3, 227, 227),
        kernel_initializer=Caffenet_initialization,
        strides=(4, 4),
        kernel_regularizer=l2(weight_decay)))
    model.add(Activation('relu'))
    model.add(MaxPooling2D(pool_size=(3, 3), strides=(2, 2)))
    model.add(BatchNormalization())

    # Conv2
    model.add(Conv2D(
        filters=256,
        kernel_size=(5, 5),
        padding='same',
        kernel_initializer=Caffenet_initialization,
        kernel_regularizer=l2(weight_decay)))
    model.add(Activation('relu'))
    model.add(MaxPooling2D(pool_size=(3, 3), strides=(2, 2)))
    model.add(BatchNormalization())

    # Conv3
    model.add(Conv2D(
        filters=384,
        kernel_size=(3, 3),
        padding='same',
        kernel_initializer=Caffenet_initialization,
        kernel_regularizer=l2(weight_decay)))
    model.add(Activation('relu'))

    # Conv4
    model.add(Conv2D(
        filters=384,
        kernel_size=(3, 3),
        padding='same',
        kernel_initializer=Caffenet_initialization,
        kernel_regularizer=l2(weight_decay)))
    model.add(Activation('relu'))

    # Conv5
    model.add(Conv2D(
        filters=256,
        kernel_size=(3, 3),
        padding='same',
        kernel_initializer=Caffenet_initialization,
        kernel_regularizer=l2(weight_decay)))
    model.add(Activation('relu'))
    model.add(MaxPooling2D(pool_size=(3, 3), strides=(2, 2)))

    model.add(Flatten())

    # Fc6
    model.add(Dense(4096, kernel_initializer=Caffenet_initialization, kernel_regularizer=l2(weight_decay)))
    model.add(Activation('relu'))
    model.add(Dropout(0.5))

    # Fc7
    model.add(Dense(4096, kernel_initializer=Caffenet_initialization, kernel_regularizer=l2(weight_decay)))
    model.add(Activation('relu'))
    model.add(Dropout(0.5))

    # Fc8
    model.add(Dense(outputs, kernel_initializer=Caffenet_initialization, kernel_regularizer=l2(weight_decay)))
    model.add(Activation('softmax'))

    return model
