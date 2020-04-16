'''Trains a simple convnet on the MNIST dataset.

Gets to 99.25% test accuracy after 12 epochs
(there is still a lot of margin for parameter tuning).
16 seconds per epoch on a GRID K520 GPU.
'''

from __future__ import print_function
import keras
import matplotlib.pyplot as plt
from keras.datasets import mnist
from keras.models import Sequential
from keras.layers import Dense, Dropout, Flatten
from keras.layers import Conv2D, MaxPooling2D
from keras import backend as K
import numpy as np
from ikrlib import png2fea, plot2dfun, eval_nnet, train_nnet, wav16khz2mfcc
from sklearn.model_selection import train_test_split

import re



# the data, shuffled and split between train and test sets
train = png2fea('../data/target_train')
test = png2fea('../data/target_dev')


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

x_train = np.vstack(tuple(train.values()))
x_test = np.vstack(tuple(test.values()))
y_train = np.vstack(tuple(train_labels))
y_test = np.vstack(tuple(test_labels))

print(x_train.shape, x_test.shape, y_train.shape, y_test.shape)

batch_size = 128
num_classes = 20
epochs = 1

# input image dimensions
img_rows, img_cols = 16, 15

# the data, shuffled and split between train and test sets
#(x_train, y_train), (x_test, y_test) = mnist.load_data()

#####################################
plt.figure()
for i in range(25):
  plt.subplot(5,5,i+1)
  plt.imshow(x_test[i], cmap='gray')
#####################################

x_train = x_train.reshape(x_train.shape[0], img_rows, img_cols, 1)
x_test = x_test.reshape(x_test.shape[0], img_rows, img_cols, 1)
input_shape = (img_rows, img_cols, 1)

x_train = x_train.astype('float32')
x_test = x_test.astype('float32')
x_train /= 255
x_test /= 255
print('x_train shape:', x_train.shape)
print(x_train.shape[0], 'train samples')
print(x_test.shape[0], 'test samples')

# convert class vectors to binary class matrices
y_train = keras.utils.to_categorical(y_train)
y_test = keras.utils.to_categorical(y_test)


print(y_train.shape, y_test.shape)

model = Sequential()
model.add(Conv2D(32, kernel_size=(5, 5), activation='relu', input_shape=input_shape))
#model.add(Conv2D(64, (3, 3), activation='relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Dropout(0.25))
model.add(Flatten())
model.add(Dense(128, activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(20, activation='softmax'))

model.compile(loss=keras.losses.categorical_crossentropy,
              optimizer=keras.optimizers.Adadelta(),
              metrics=['accuracy'])

model.fit(x_train, y_train,
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
p_test[:25].reshape(5,5)


weights=model.get_weights()
weights=weights[0]
for i in range(32):
  plt.subplot(4,8,i+1)
  plt.imshow(weights[:,:,0,i], cmap='gray')
