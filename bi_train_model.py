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
from sklearn.metrics import classification_report, confusion_matrix
import seaborn as sns
import matplotlib.pyplot as plt
import tensorflow as tf



X_train = np.load('/content/drive/MyDrive/dataset-new/token/train_pad/X_train.npy')
X_test = np.load('/content/drive/MyDrive/dataset-new/token/train_pad/X_test.npy')
y_train = np.load('/content/drive/MyDrive/dataset-new/token/train_pad/y_train_v3.npy')
y_test = np.load('/content/drive/MyDrive/dataset-new/token/train_pad/y_test_v3.npy')

with open ('/content/drive/MyDrive/dataset-new/token/tokenizer.pkl', 'rb') as f:
    tokenizer = pickle.load(f)

with open ('/content/drive/MyDrive/dataset-new/token/maxlen_v2.txt', 'r') as mx:
    max_len = int(mx.read())

print("Contoh input token:", X_train[2452])
print("Panjang:", len(X_train[2452]))
print("Max len:", max_len)

unique, counts = np.unique(y_train, return_counts=True)
print(dict(zip(unique, counts)))

vocab_size = len(tokenizer.word_index) + 1

model = Sequential([
    Embedding(input_dim=vocab_size, output_dim=64, input_length=max_len),
    # Dropout(0.3),
    Bidirectional(LSTM(64, return_sequences=True)),
    Dropout(0.5),
    Bidirectional(LSTM(64)),
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

model.save('/content/drive/MyDrive/dataset-new/bi_model_batch64_5_05.h5')
print("Model trained and saved.")

# Prediksi
model = tf.keras.models.load_model('/content/drive/MyDrive/dataset-new/bi_model_batch64_5_05.h5')
y_pred_prob = model.predict(X_test)
y_pred_classes = (y_pred_prob > 0.5).astype("int32").flatten()  # hasil 0/1

# Ground truth
y_true = y_test  

# Confusion matrix
cm = confusion_matrix(y_true, y_pred_classes)
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues')
plt.xlabel("Predicted")
plt.ylabel("Actual")
plt.title("Confusion Matrix")
plt.show()

# Classification report
print(classification_report(y_true, y_pred_classes, digits=4))
