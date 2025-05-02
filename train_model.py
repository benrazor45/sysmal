import numpy as np
import tensorflow as tf
import pickle
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Embedding, LSTM, Dense, Dropout
from tensorflow.keras.callbacks import EarlyStopping
import matplotlib.pyplot as plt

X_train = np.load('dataset_feature/tokenization/X_train.npy')
X_test = np.load('dataset_feature/tokenization/X_test.npy')
y_train = np.load('dataset_feature/labels_tokenization/y_train.npy')
y_test = np.load('dataset_feature/labels_tokenization/y_test.npy')

with open('tokenizer.pkl', 'rb') as f:
    tokenizer = pickle.load(f)

with open('maxlen.txt', 'r') as mx:
    max_len = int(mx.read())

vocab_size = len(tokenizer.word_index) + 1

model = Sequential([
    Embedding(input_dim=vocab_size, output_dim=128, input_length=max_len),
    LSTM(128, return_sequences=False),
    Dropout(0.5),
    Dense(1, activation='sigmoid')
])

model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])

es = EarlyStopping(monitor='val_loss', patience=3, restore_best_weights=True)

history = model.fit(
    X_train, y_train,
    epochs=10,
    batch_size=64,
    validation_split=0.2,
    callbacks=[es]
)

loss, acc = model.evaluate(X_test, y_test)
print(f" Test Accuracy: {acc:.4f}")
print(f"Test Loss: {loss:.4f}")

plt.figure(figsize=(10,4))

plt.subplot(1,2,1)
plt.plot(history.history['accuracy'], label='Train Acc')
plt.plot(history.history['val_accuracy'], label='Val Acc')
plt.title('Accuracy')
plt.legend()

plt.subplot(1,2,2)
plt.plot(history.history['loss'], label='Train Loss')
plt.plot(history.history['val_loss'], label='Val Loss')
plt.title('Loss')
plt.legend()

plt.tight_layout()
plt.show()

model.save('model/lstm_v2_no_leakage.h5')
print("Model trained and saved.")
