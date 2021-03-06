# -*- coding: utf-8 -*-
"""Lyrics Generator.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1LRHqUIcpvVVTLaHpu6v2L8EtSKOiUG8i
"""

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

import string
import keras
from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences
from keras.layers import Embedding, LSTM, Dense, Dropout, Bidirectional
from keras.models import Sequential
from keras.optimizers import Adam
from keras import regularizers
from keras.utils import np_utils

lyrics = pd.read_csv('Maroon5.csv')

lyrics.head()

l=lyrics['Lyric']

l.isnull().sum()

l.shape

l=l.str.lower()

l = l.str.replace('[{}]'.format(string.punctuation),'')

l

song = list(l)
t = Tokenizer()
t.fit_on_texts(song)

total_words = len(t.word_index)+1
total_words

input_sequence = []
for i in song:
  tokenlist = t.texts_to_sequences([i])[0]
  for j in range (1,len(tokenlist)) :
      n_gram = tokenlist[:j+1]
      input_sequence.append(n_gram)

max_seq_length = max([len(x) for x in input_sequence])
input_sequence = np.array(pad_sequences(input_sequence, maxlen=max_seq_length,padding="pre"))

print(max_seq_length)
print(input_sequence)

model = Sequential()

model.add(Embedding(total_words,160,input_length=max_seq_length-1))
# model.add(Bidirectional(LSTM(200,return_sequences=True)))
model.add(Dropout(0.2))
model.add(LSTM(100))
model.add(Dense(total_words/2,activation='relu',kernel_regularizer=regularizers.l2(0.001)))
model.add(Dense(total_words,activation="softmax"))

model.compile(loss='categorical_crossentropy',optimizer="adam",metrics=['accuracy'])
model.summary()

model_predict,output_label = input_sequence[:,:-1],input_sequence[:,-1]
output_label = np_utils.to_categorical(output_label, num_classes=total_words)

history = model.fit(model_predict, output_label, epochs=1, verbose=1)

def Song_Generate(text, next_words):
    for i in text:
        tokenlist = t.texts_to_sequences([i])[0]
        tokenlist = pad_sequences([tokenlist],maxlen=max_seq_length-1,padding='pre')
        predicted = model.predict_classes(tokenlist, verbose=0)
        output= ""
        for word, index in t.word_index.items():
            if index == predicted:
                output = word
                break
        text += " " + output
    print(text)

next_words = 100
text = "what is life"
Song_Generate(text, next_words)

