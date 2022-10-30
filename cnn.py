# -*- coding: utf-8 -*-
"""CNN.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1Qbv-CXZOtLf-QkLOFBkshtVZnrxj6MSQ
"""

#εγκατάσταση της βιβλιοθήκης idx2numpy, καθώς πρέπει να διαβαστούν αρχεία αντίστοιχης μορφής
pip install idx2numpy

#φόρτωση αναγκαίων βιβλιοθηκών
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Conv2D, Flatten, Dropout, MaxPooling2D, AveragePooling2D, Conv1D, AveragePooling1D
from tensorflow.keras.preprocessing import image
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.losses import BinaryCrossentropy
from tensorflow.keras.losses import SparseCategoricalCrossentropy, CategoricalCrossentropy


import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import gzip
import seaborn as sns
from sklearn import metrics
import idx2numpy

#άνοιγμα αρχείων με gzip
train_zip = gzip.open('/content/train-images-idx3-ubyte.gz','r')
train_labels_zip = gzip.open('/content/train-labels-idx1-ubyte.gz','r')
test_zip  = gzip.open('/content/t10k-images-idx3-ubyte.gz','r')
test_labels_zip = gzip.open('/content/t10k-labels-idx1-ubyte.gz','r')

#διάβασμα των αρχείων
imagefile1 = train_zip
train = idx2numpy.convert_from_file(imagefile1)

imagefile2 = train_labels_zip
trainlabels = idx2numpy.convert_from_file(imagefile2)

imagefile3 = test_zip
test = idx2numpy.convert_from_file(imagefile3)

imagefile4 = test_labels_zip
testlabels = idx2numpy.convert_from_file(imagefile4)

#οπτικοποίηση ενός τυχαίου παραδείγματος που εμπεριέχεται στο train
sample = 1
image = train[sample]

fig = plt.figure
plt.imshow(image, cmap= 'Greys')
plt.show()

#οπτικοποίηση δέκα εικόνων, μία για κάθε κλάση 0-9 
num_row = 2
num_col = 5

digits = []
j = 0
i = 0

fig, axes = plt.subplots(num_row, num_col, figsize=(2.5*num_col,3*num_row))


fig.subplots_adjust(hspace=0.4, top=1.2)

fig.suptitle("Instances of handwritten digits, accompanied by their labels", fontsize=15)


while j < 10:
     
    if trainlabels[i] not in digits:

      ax = axes[j//num_col, j%num_col]
      ax.imshow(train[i], cmap='gray')
      ax.set_title('Label: {}'.format(trainlabels[i]), fontsize = 15)

      j += 1
      digits.append(trainlabels[i])      
    
    i += 1



plt.tight_layout()
plt.show()

#οι διαστάσεις του train
train.shape

#οι διαστάσεις μιας εικόνας του train
train[0].shape

#δημιουργία της δομής του Συνελικτικού Νευρωνικού Δικτύου
model = Sequential()

model.add(Conv2D(6, (3,3), activation = 'relu', strides = 1, padding = 'same',input_shape = (28,28,1)))

model.add(AveragePooling2D((2,2), strides = 2))

model.add(Conv2D(16, (3,3), activation = 'relu', strides = 1, padding = 'same'))

model.add(AveragePooling2D((2,2), strides = 2))

model.add(Flatten())

model.add(Dense(120, activation = 'relu'))

model.add(Dense(84, activation = 'relu'))

model.add(Dense(10, activation = 'softmax' ))



model.summary()

#καθορισμός του αλγορίθμου εκπαίδευσης, της συνάρτησης σφάλματος και των μετρικών
model.compile(optimizer = 'sgd', loss = 'sparse_categorical_crossentropy', metrics = ['accuracy'])

#καθορισμός αριθμού εποχών εκπαίδευσης και batch size
epochs = 30
batch_size = 32


#καθορισμός του χρησιμοποιούμενου callback κατά την εκπαίδευση
stopping_callback = tf.keras.callbacks.EarlyStopping(
    monitor="val_accuracy",
    min_delta=0,
    patience=3,
    verbose=0,
    mode="auto",
    baseline=None,
    restore_best_weights=True,
)

#εκπαίδευση του δικτύου
history = model.fit(train , trainlabels, epochs = epochs, steps_per_epoch  = None, validation_data = (test,testlabels), 
                    validation_steps = None, batch_size = batch_size, callbacks = [stopping_callback])

#οπτικοποίηση της εξέλιξης της ακρίβειας ταξινόμησης και του σφάλματος κατά την διάρκεια των εποχών εκπαίδευσης για τα σετ εκπαίδευσης και αξιολόγησης
acc = history.history['accuracy']
val_acc = history.history['val_accuracy']

loss = history.history['loss']
val_loss = history.history['val_loss']



plt.figure(figsize=(10, 5))
plt.subplot(1, 2, 1)
plt.plot(acc, label='Training Accuracy')
plt.plot(val_acc, label='Validation Accuracy')
plt.legend(loc='lower right')
plt.title('Training and Validation Accuracy')

plt.subplot(1, 2, 2)
plt.plot(loss, label='Training Loss')
plt.plot(val_loss, label='Validation Loss')
plt.legend(loc='upper right')
plt.title('Training and Validation Loss')
plt.show()

#εξαγωγή του αποτελέσματος του δικτύου για το test set και καθορισμός των πραγματικών ετικετών ταξινόμησης
predicted = model.predict(test)
actual = testlabels

#καθορισμός της προβλεπόμενης κατηγορίας για το test set
predictions = []

for i in range(10000):
  max_prob = max(predicted[i])

  for j in range(10):

    if predicted[i][j] == max_prob:

      predictions.append(j)

print(predictions[0:5])
print(actual[0:5])

#μετατροπή της λίστας των προβλέψεων σε πίνακα
predictions = np.array(predictions)

#Υπολογισμός της ακρίβειας ταξινόμησης για το test set
accuracy = metrics.accuracy_score(actual, predictions)
print('Accuracy on test set is', accuracy)

#συνάρτηση δημιουργίας του πίνακα συνάφειας
def conf_matr(actual, predicted):

  shape = (10,10)
  confusion_matrix = np.zeros(shape)

  for i in range(10000):
    confusion_matrix[actual[i], predictions[i]]+=1


  confusion_matrix = confusion_matrix.astype(int)
  return confusion_matrix

#πίνακας συνάφειας
confusion_matrix = conf_matr(actual,predictions)
confusion_matrix

#μετατροπή του πίνακα συνάφειας, ώστε να περιέχει ποσοστά για κάθε ψηφίο
confusion_matrix  = confusion_matrix.astype(np.float)

for i in range(10):

     confusion_matrix[i] = confusion_matrix[i]/sum(confusion_matrix[i])


confusion_matrix = np.round(confusion_matrix, 3)

#τελική μορφή πίνακα συνάφειας
fig = plt.figure(figsize = (20,9))
ax = plt.subplot()

sns.set(font_scale=1.8)
sns.heatmap(confusion_matrix, annot=True, fmt='', cmap='Blues')

ax.set_xlabel('predicted label', fontsize = 15)
ax.set_ylabel('true label', fontsize = 15)

plt.title('Confusion Matrix', fontsize = 20)

plt.show()