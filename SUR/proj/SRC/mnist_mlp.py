'''Trains a simple deep NN on the MNIST dataset.

Gets to 98.40% test accuracy after 20 epochs
(there is *a lot* of margin for parameter tuning).
2 seconds per epoch on a K520 GPU.
'''

from __future__ import print_function

from ikrlib import png2fea, plot2dfun, eval_nnet, train_nnet, wav16khz2mfcc
import matplotlib.pyplot as plt
import keras
from keras.datasets import mnist
from keras.models import Sequential
from keras.layers import Dense, Dropout
from keras.optimizers import RMSprop, SGD
import numpy as np

def vectorize_sequences(sequences, dimension=256):
    results = np.zeros((len(sequences), dimension))
    for i, sequence in enumerate(sequences):
        results[i, sequence.astype(int)] = 1.
    return results

batch_size = 128
num_classes = 100
epochs = 10


# the data, shuffled and split between train and test sets
x_train = np.vstack(tuple(png2fea('../data/target_train').values()))
x_test = np.vstack(tuple(png2fea('../data/target_dev').values()))

y_train = np.vstack(tuple(wav16khz2mfcc('../data/target_train').values()))
y_test = np.vstack(tuple(wav16khz2mfcc('../data/target_dev').values()))

#(x_train, y_train), (x_test, y_test) = mnist.load_data()

#####################################
plt.figure()
for i in range(25):
  plt.subplot(5,5,i+1)
  plt.imshow(x_test[i], cmap='gray')
#####################################

#x_test.transpose(2,0,1).reshape(3,-1)
#y_test.transpose(2,0,1).reshape(3,-1)

x_train = x_train.reshape(3840, 100)
x_test = x_test.reshape(1920, 100)
x_train = x_train.astype('float32')
x_test = x_test.astype('float32')
x_train /= 255
x_test /= 255
print(x_train.shape[0], 'train samples')
print(x_test.shape[0], 'test samples')

# convert class vectors to binary class matrices
y_train = keras.utils.to_categorical(y_train, num_classes)
y_test = keras.utils.to_categorical(y_test, num_classes)

model = Sequential()
model.add(Dense(512, activation='relu', input_shape=(100,)))
#model.add(Dropout(0.2))
model.add(Dense(512, activation='relu'))
#model.add(Dropout(0.2))
model.add(Dense(100, activation='softmax'))

model.summary()

model.compile(loss='sparse_categorical_crossentropy',
              optimizer=SGD(lr=0.1), #optimizer=RMSprop(),
              metrics=['accuracy'])

_x = 1
for i in range(1, len(x_test.shape)):
     _x = _x * x_test.shape[i]
     print('x: ',_x)

_y = 1
for i in range(1, len(y_test.shape)):
     _y = _y * y_test.shape[i]
     print('y: ',_y)

x_test = x_test.reshape((x_test.shape[0], _x))

y_test = y_test.reshape((y_test.shape[0], _y))

history = model.fit(x_train, y_train,
                    batch_size=batch_size,
                    epochs=epochs,
                    verbose=1,
                    validation_data=(x_test.reshape((x_test.shape[0], _x)), y_test.reshape((y_test.shape[0], _y))))
score = model.evaluate(x_test, y_test, verbose=0)
print('Test loss:', score[0])
print('Test accuracy:', score[1])

################################################
p_test=model.predict(x_test, batch_size=128)
p_test=np.argmax(p_test, axis=1)
p_test[:25].reshape(5,5)


weights=model.get_weights()
weights=weights[0]
plt.figure()
for i in range(25):
  plt.subplot(5,5,i+1)
  plt.imshow(weights[:,i].reshape(28,28), cmap='gray')
