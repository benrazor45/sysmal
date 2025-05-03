import numpy as np
import tensorflow as tf
import pickle
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Embedding, LSTM, Dense, Dropout
from tensorflow.keras.callbacks import EarlyStopping
from tensorflow.keras.preprocessing.sequence import pad_sequences
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.metrics import AUC
from tensorflow.keras.layers import Bidirectional


X_train = np.load('dataset_feature/tokenization/X_train_v2.npy')
X_test = np.load('dataset_feature/tokenization/X_test_v2.npy')
y_train = np.load('dataset_feature/labels_tokenization/y_train_v2.npy')
y_test = np.load('dataset_feature/labels_tokenization/y_test_v2.npy')

with open('tokenizer.pkl', 'rb') as f:
    tokenizer = pickle.load(f)

with open('maxlen.txt', 'r') as mx:
    max_len = int(mx.read())

vocab_size = len(tokenizer.word_index) + 1

model = Sequential([
    Embedding(input_dim=vocab_size, output_dim=64, input_length=max_len),
    Bidirectional(LSTM(64, return_sequences=True)),
    Bidirectional(LSTM(64)),
    Dropout(0.3),
    Dense(1, activation='sigmoid')
])

optimizer = Adam(learning_rate=1e-4)

model.compile(loss='binary_crossentropy', optimizer=optimizer, metrics=['accuracy', AUC()])
# model.compile(loss='binary_crossentropy', optimizer=optimizer, metrics=['accuracy'])

es = EarlyStopping(monitor='val_loss', patience=3, restore_best_weights=True)

history = model.fit(
    X_train, y_train,
    epochs=10,
    batch_size=64,
    validation_split=0.2,
    callbacks=[es]
)

loss, acc, auc = model.evaluate(X_test, y_test)
# loss, acc = model.evaluate(X_test, y_test)

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

model.save('model/lstm_v2_without_auc_v2.h5')
print("Model trained and saved.")