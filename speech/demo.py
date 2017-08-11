from __future__ import division, print_function, absolute_import
# Deep learning library featuring  a higher level api for tensorflow
import tflearn
# Helper Class to fetch data and format it
import speech_data
import tensorflow as tf

# To apply it to weight updating process.
# Greater the learning rate faster the network trains.
# Lower the Learning rate more acurate our network trains
learning_rate = 0.0001
# Number of steps for training
training_iters = 100  # steps
batch_size = 64

width = 20  # mfcc features
height = 80  # (max) length of utterance
classes = 10  # digits

# Download set of wave file. Return the label speech files as a batch
batch = word_batch = speech_data.mfcc_batch_generator(batch_size)
# Train and test using next
X, Y = next(batch)
trainX, trainY = X, Y
testX, testY = X, Y #overfit for now

# RNN Network building
# Initial Gateway to feed data into the Network
# Input tensor is a multi dimensional array of data
# width - Number of features extracted using each utterance
# height - max length of each utterance
net = tflearn.input_data([None, width, height])
# LSTM
# feed previous layer.
# dropout - helps prevent overfeeding  by randomnly turning of some neurons so data is forced to new path allowing for more generalized modal
net = tflearn.lstm(net, 128, dropout=0.8)
# fully connected neurons
# classes - recognizing on 10 digits
# activation function to softmax which will convert numerical data to probability
net = tflearn.fully_connected(net, classes, activation='softmax')
# output layer which will output a single predicted layer for our utterance
# Using atom optimizer to minimize categorical crossentropy loss function overtime to get more accurate prediction
net = tflearn.regression(net, optimizer='adam', learning_rate=learning_rate, loss='categorical_crossentropy')
# Training

### add this "fix" for tensorflow version errors
col = tf.get_collection(tf.GraphKeys.TRAINABLE_VARIABLES)
for x in col:
    tf.add_to_collection(tf.GraphKeys.VARIABLES, x )

# Initialize deep neural network
model = tflearn.DNN(net, tensorboard_verbose=3)
for x in range(1,training_iters):
  model.fit(trainX, trainY, n_epoch=10, validation_set=(testX, testY), show_metric=True,
          batch_size=batch_size)
  _y=model.predict(X)
model.save("tflearn.lstm.model")
print (_y)
