

import keras
from keras.datasets import mnist
from keras.models import Sequential,Input,Model
from keras.layers import Dense, Dropout, Flatten
from keras.layers import Conv2D, MaxPooling2D
from keras.layers.normalization import BatchNormalization
from keras.layers.advanced_activations import LeakyReLU
import numpy as np
from ikrlib import png2fea, plot2dfun
import matplotlib.pyplot as plt
import re
from load_file import load_file

# load and display an image with Matplotlib
from matplotlib import image
from matplotlib import pyplot

#zdroj: https://www.datacamp.com/community/tutorials/convolutional-neural-networks-python

# the data, shuffled and split between train and test sets
train = load_file('../data/target_train')
test = load_file('../data/target_dev')

# summarize shape of the pixel array

x_train = np.vstack(tuple(train.values()))
x_test = np.vstack(tuple(test.values()))

train_labels = []
test_labels = []

i = 0
for k in train.keys():
    train_labels.append(i)
    i += 1

i = 0
for k in test.keys():
    test_labels.append(i)
    i += 1

y_train = np.vstack(tuple(train_labels))
y_test = np.vstack(tuple(test_labels))

y_train = y_train.reshape(y_train.shape[0])
y_test = y_test.reshape(y_test.shape[0])

print(x_train.shape, x_test.shape, y_train.shape, y_test.shape)


batch_size = 128
num_classes = len(train_labels)
epochs = 100

# input image dimensions
img_rows, img_cols = 80, 80

#####################################
"""
plt.figure()
for i in range(25):
  plt.subplot(5,5,i+1)
  plt.imshow(x_test[i], cmap='gray')
  plt.show()
"""
#####################################

x_train = x_train.reshape(x_train.shape[0] // img_rows, img_rows, img_cols, 1)
x_test = x_test.reshape(x_test.shape[0] // img_rows, img_rows, img_cols, 1)
input_shape = (img_rows, img_cols, 1)

x_train = x_train.astype('float32')
x_test = x_test.astype('float32')
x_train /= 255
x_test /= 255
print('x_train shape:', x_train.shape)
print(x_train.shape[0], 'train samples')
print(x_test.shape[0], 'test samples')


# convert class vectors to binary class matrices
y_train = keras.utils.to_categorical(y_train, num_classes)
y_test = keras.utils.to_categorical(y_test, num_classes)


print(y_train.shape, y_test.shape)

model = Sequential()
model.add(Conv2D(32, kernel_size=(3, 3),activation='linear',input_shape=input_shape,padding='same'))
model.add(LeakyReLU(alpha=0.1))
model.add(MaxPooling2D((2, 2),padding='same'))
model.add(Conv2D(64, (3, 3), activation='linear',padding='same'))
model.add(LeakyReLU(alpha=0.1))
model.add(MaxPooling2D(pool_size=(2, 2),padding='same'))
model.add(Conv2D(128, (3, 3), activation='linear',padding='same'))
model.add(LeakyReLU(alpha=0.1))
model.add(MaxPooling2D(pool_size=(2, 2),padding='same'))
model.add(Flatten())
model.add(Dense(128, activation='linear'))
model.add(LeakyReLU(alpha=0.1))
model.add(Dense(num_classes, activation='softmax'))

model.compile(loss=keras.losses.categorical_crossentropy, optimizer=keras.optimizers.Adam(),metrics=['accuracy'])
model.summary()

train = model.fit(x_train, y_train,
                  batch_size=batch_size,
                  epochs=epochs,
                  verbose=1,
                  validation_data=(x_test, y_test))

score = model.evaluate(x_test, y_test, verbose=0)
print('Test loss:', score[0])
print('Test accuracy:', score[1])

#############################
p_test=model.predict(x_test, batch_size=128)
p_test=np.argmax(p_test, axis=1)
p_test[:25].reshape(5,2)


weights=model.get_weights()
weights=weights[0]
for i in range(32):
  plt.subplot(4,8,i+1)
  plt.imshow(weights[:,:,0,i], cmap='gray')
plt.show()
