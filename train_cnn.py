import pandas as pd
import numpy as np
import tensorflow
from sklearn.feature_extraction.text import CountVectorizer
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.callbacks import EarlyStopping, ReduceLROnPlateau
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv1D, MaxPooling1D, Flatten, Dense
import matplotlib.pyplot as plt
from keras.layers import Dropout
from keras.callbacks import EarlyStopping
from keras.regularizers import l2
from keras.layers import Input


dataset_raw = pd.read_csv('/content/drive/MyDrive/dataset_cnn/combined_dataset.csv')

le = LabelEncoder()
y_encoded = le.fit_transform(dataset_raw['label'].values).astype(np.float32)

X_train_seq, X_test_seq, y_train, y_test = train_test_split(
    dataset_raw['sequence'], y_encoded, test_size=0.2, random_state=42, stratify=y_encoded)

tokenizer = Tokenizer(lower=False, split=' ')
tokenizer.fit_on_texts(X_train_seq)

MAXLEN = 287
X_train_pad = pad_sequences(tokenizer.texts_to_sequences(X_train_seq), maxlen=MAXLEN, padding='post')
X_test_pad = pad_sequences(tokenizer.texts_to_sequences(X_test_seq), maxlen=MAXLEN, padding='post')

X_train_cnn = X_train_pad.reshape(-1, MAXLEN, 1)
X_test_cnn = X_test_pad.reshape(-1, MAXLEN, 1)

model = Sequential([
    Input(shape=(X_train_cnn.shape[1], 1)),
    Conv1D(32, kernel_size=5, activation='relu', kernel_regularizer=l2(0.01)),
    MaxPooling1D(pool_size=2),
    Dropout(0.2),
    Conv1D(64, kernel_size=3, activation='relu', kernel_regularizer=l2(0.01)),
    MaxPooling1D(pool_size=2),
    Dropout(0.2),
    Flatten(),
    Dense(32, activation='relu', kernel_regularizer=l2(0.01)),
    Dropout(0.2),
    Dense(1, activation='sigmoid')
])

optimizer = Adam(learning_rate=5e-4)

model.compile(optimizer=optimizer, loss='binary_crossentropy', metrics=['accuracy'])

early_stop = EarlyStopping(monitor='val_loss', patience=5, restore_best_weights=True)
reduce_lr = ReduceLROnPlateau(monitor='val_loss', factor=0.5, patience=3, min_lr=1e-6, verbose=1)


history = model.fit(X_train_cnn, y_train, epochs=20, batch_size=32, validation_data=(X_test_cnn, y_test),
                    callbacks=[early_stop, reduce_lr])

loss, acc = model.evaluate(X_test_cnn, y_test)
print(f"Test Accuracy: {acc:.4f}")

plt.plot(history.history['accuracy'], label='Train Accuracy')
plt.plot(history.history['val_accuracy'], label='Validation Accuracy')
plt.title('Akurasi Model')
plt.xlabel('Epoch')
plt.ylabel('Accuracy')
plt.legend()
plt.grid(True)
plt.show()

# Plot loss
plt.plot(history.history['loss'], label='Train Loss')
plt.plot(history.history['val_loss'], label='Validation Loss')
plt.title('Loss Model')
plt.xlabel('Epoch')
plt.ylabel('Loss')
plt.legend()
plt.grid(True)
plt.show()

model.save("/content/drive/MyDrive/dataset_cnn/cnn_malware_model_seq_v11.h5")