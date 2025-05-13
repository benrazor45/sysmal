import pandas as pd
import numpy as np
import tensorflow
from sklearn.feature_extraction.text import CountVectorizer
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

vectorizer = CountVectorizer(tokenizer=lambda x: x.split(), lowercase=False)

X = vectorizer.fit_transform(dataset_raw['sequence'])
y = dataset_raw['label'].values

print(f"Jumlah fitur unik: {len(vectorizer.get_feature_names_out())}")
print(vectorizer.get_feature_names_out()[:10])
print(X.shape)


X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

le = LabelEncoder()
y_train = le.fit_transform(y_train)
y_test = le.transform(y_test)

X_train_cnn = X_train.toarray().reshape(X_train.shape[0], X_train.shape[1], 1)
X_test_cnn = X_test.toarray().reshape(X_test.shape[0], X_test.shape[1], 1)


print(X_train_cnn.shape)
print(X_test_cnn.shape)

model = Sequential([
    Input(shape=(X_train_cnn.shape[1], 1)),
    Conv1D(64, kernel_size=5, activation='relu', kernel_regularizer=l2(0.001)),
    MaxPooling1D(pool_size=2),
    Dropout(0.3),
    Flatten(),
    Dense(64, activation='relu', kernel_regularizer=l2(0.001)),
    Dropout(0.3),
    Dense(1, activation='sigmoid')
])

model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

early_stop = EarlyStopping(monitor='val_loss', patience=3, restore_best_weights=True)

history = model.fit(X_train_cnn, y_train, epochs=10, batch_size=32, validation_data=(X_test_cnn, y_test), callbacks=[early_stop])

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

model.save("/content/drive/MyDrive/dataset_cnn/cnn_malware_model_v8.h5")