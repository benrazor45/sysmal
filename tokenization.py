import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from sklearn.preprocessing import LabelEncoder
import pickle

df = pd.read_csv('dataset_feature/cleaned/combined_dataset.csv')

X_train_text, X_test_text, y_train_text, y_test_text = train_test_split(
    df['sequence'], df['label'], test_size=0.2, random_state=42, stratify=df['label']
)

tokenizer = Tokenizer()
tokenizer.fit_on_texts(X_train_text)

X_train_seq = tokenizer.texts_to_sequences(X_train_text)
X_test_seq = tokenizer.texts_to_sequences(X_test_text)

maxlen = max(len(seq) for seq in X_train_seq) 

X_train_pad = pad_sequences(X_train_seq, padding='post', maxlen=maxlen)
X_test_pad = pad_sequences(X_test_seq, padding='post', maxlen=maxlen)

label_encoder = LabelEncoder()
y_train_enc = label_encoder.fit_transform(y_train_text)
y_test_enc = label_encoder.transform(y_test_text)

np.save('dataset_feature/tokenization/X_train.npy', X_train_pad)
np.save('dataset_feature/tokenization/X_test.npy', X_test_pad)
np.save('dataset_feature/labels_tokenization/y_train.npy', y_train_enc)
np.save('dataset_feature/labels_tokenization/y_test.npy', y_test_enc)

with open('tokenizer.pkl', 'wb') as f:
    pickle.dump(tokenizer, f)

with open('maxlen.txt', 'w') as mx:
    mx.write(str(maxlen))

print("Tokenization done")