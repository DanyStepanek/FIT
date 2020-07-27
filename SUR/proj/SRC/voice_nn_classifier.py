import matplotlib.pyplot as plt
from ikrlib import wav16khz2mfcc

import numpy as np

from keras import layers
from keras import models
from keras import optimizers
from keras import utils
from keras import metrics
import datetime
import time


# Load data
train_t = np.vstack(tuple(wav16khz2mfcc('../data/target_train').values()))


train_n = np.vstack(tuple(wav16khz2mfcc('../data/non_target_train').values()))

val_t = np.vstack(tuple(wav16khz2mfcc('../data/target_dev').values()))

val_n = np.vstack(tuple(wav16khz2mfcc('../data/non_target_dev').values()))

print('train_t: ',train_t.shape)
print('train_n: ',train_n.shape)
print('val_t: ',val_t.shape)
print('val_n: ',val_n.shape)


#preparing data
train_x = np.r_[train_t, train_n]
train_y = np.r_[np.ones(len(train_t)), np.zeros(len(train_n))]

val_x = np.r_[val_t, val_n]
val_y = np.r_[np.ones(len(val_t)), np.zeros(len(val_n))]

train_x = train_x.astype('float32')
val_x = val_x.astype('float32')
train_x /= 255
val_x /= 255

train_y = utils.to_categorical(train_y)
val_y = utils.to_categorical(val_y)

print('train_x: ',train_x.shape)
print('train_y: ',train_y.shape)
print('test_x: ',val_x.shape)
print('test_y: ',val_y.shape)


batch_size = 64
epochs = 6
num_classes = train_y.shape[1]
print(num_classes)
start = datetime.datetime.now()
# Defining network architecture
model = models.Sequential()
model.add(layers.Dense(16, activation='relu', input_shape=(train_x[0].shape)))
model.add(layers.Dense(32, activation='relu'))
model.add(layers.Dense(32, activation='relu'))
model.add(layers.Dense(16, activation='relu'))
model.add(layers.Dense(num_classes, activation='softmax'))
# Compiling model
model.compile(loss="categorical_crossentropy",
              optimizer="rmsprop",
              metrics=['acc'])

end= datetime.datetime.now()
elapsed= end-start
print ('Time: ', elapsed)

model.summary()
#train model
history = model.fit(train_x, train_y,
                  batch_size=batch_size,
                  epochs=epochs,
                  verbose=1,
                  validation_data=(val_x, val_y))

model.save('nn_voice.h5')
#evaluataing
score = model.evaluate(val_x, val_y, verbose=0)
print('Test loss:', score[0])
print('Test accuracy:', score[1])

acc = history.history['acc']
val_acc = history.history['val_acc']
loss = history.history['loss']
val_loss = history.history['val_loss']

epochs = range(1, len(acc) + 1)
#plot training results
plt.plot(epochs, acc, 'bo', label='Training acc')
plt.plot(epochs, val_acc, 'b', label='Validation acc')
plt.title('Trainin and validation accuracy')
plt.legend()

plt.figure()

plt.plot(epochs, loss, 'bo', label='Training_loss')
plt.plot(epochs, val_loss, 'b', label='Validation_loss')
plt.title('Training and validation loss')
plt.legend()

plt.show()
