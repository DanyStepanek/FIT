
from keras import layers
from keras import models
from keras import optimizers
from keras import utils
from keras.layers.advanced_activations import LeakyReLU

from ikrlib import png2fea
import numpy as np
import matplotlib.pyplot as plt
import datetime
import time

# Load data
train_t = np.vstack(tuple(png2fea('../data/target_train').values()))
print(train_t.shape)
train_t = train_t.reshape(train_t.shape[0] //80, 80, 80, 3)
print(train_t.shape)

train_n = np.vstack(tuple(png2fea('../data/non_target_train').values()))
print(train_n.shape)
train_n = train_n.reshape(train_n.shape[0] //80, 80, 80, 3)
print(train_t.shape)

val_t = np.vstack(tuple(png2fea('../data/target_dev').values()))
print(val_t.shape)
val_t = val_t.reshape(val_t.shape[0] //80, 80, 80, 3)
print(val_t.shape)

val_n = np.vstack(tuple(png2fea('../data/non_target_dev').values()))
print(val_n.shape)
val_n = val_n.reshape(val_n.shape[0] //80, 80, 80, 3)
print(val_n.shape)


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

batch_size = 64
epochs = 7
num_classes = 2
print(num_classes)
start = datetime.datetime.now()

# Defining network architecture
model = models.Sequential()
model.add(layers.Conv2D(32, (3, 3), input_shape=(80, 80, 3)))
model.add(LeakyReLU(alpha=0.3))
model.add(layers.MaxPooling2D((2, 2)))

model.add(layers.Conv2D(64, (3, 3)))
model.add(LeakyReLU(alpha=0.3))
model.add(layers.MaxPooling2D((2, 2)))

model.add(layers.Conv2D(128, (3, 3)))
model.add(LeakyReLU(alpha=0.3))

model.add(layers.Flatten())
model.add(layers.Dropout(0.5))
model.add(layers.Dense(256))
model.add(LeakyReLU(alpha=0.3))
model.add(layers.Dense(num_classes, activation='softmax'))
# Compiling model
model.compile(loss='categorical_crossentropy',
              optimizer='rmsprop',
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

#evaluataing
score = model.evaluate(val_x, val_y, verbose=0)
print('Test loss:', score[0])
print('Test accuracy:', score[1])


model.save("cnn_image.h5")

#plot training results
acc = history.history['acc']
val_acc = history.history['val_acc']
loss = history.history['loss']
val_loss = history.history['val_loss']


epochs = range(1, len(acc) + 1)

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
