import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from sklearn.preprocessing import LabelEncoder
import pickle
import matplotlib.pyplot as plt


df = pd.read_csv('fix_dataset/combined_dataset_fix_new.csv')

X_train_text, X_test_text, y_train_text, y_test_text = train_test_split(
    df['sequence'], df['label'], test_size=0.2, random_state=42, stratify=df['label']
)

tokenizer = Tokenizer(oov_token="<OOV>")
tokenizer.fit_on_texts(X_train_text)

X_train_seq = tokenizer.texts_to_sequences(X_train_text)
X_test_seq = tokenizer.texts_to_sequences(X_test_text)
 
lengths = [len(seq) for seq in X_train_seq]


print("Beberapa nilai percentile panjang sequence:")
for p in [50, 75, 90, 95, 99, 100]:
    print(f"{p}th percentile: {np.percentile(lengths, p)}")

maxlen = int(np.percentile(lengths, 90))
max_length = max(lengths)
max_index = lengths.index(maxlen)


print(f"Sequence terpanjang ada di index: {max_index}")
print(f"Panjang sequence: {max_length}")
print(f"Isi tokennya: {X_train_seq[max_index]}")
print(f"Teks aslinya: {X_train_text.iloc[max_index]}")

plt.figure(figsize=(10, 5))
plt.hist(lengths, bins=50, color='skyblue', edgecolor='black')
plt.axvline(np.percentile(lengths, 90), color='red', linestyle='--', label='90th percentile')
plt.axvline(np.percentile(lengths, 95), color='orange', linestyle='--', label='95th percentile')
plt.axvline(np.percentile(lengths, 99), color='green', linestyle='--', label='99th percentile')
plt.title('Distribusi Panjang Sequence API')
plt.xlabel('Panjang Sequence')
plt.ylabel('Jumlah Sample')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()

X_train_pad = pad_sequences(X_train_seq, padding='post', truncating='post', maxlen=maxlen)
X_test_pad = pad_sequences(X_test_seq, padding='post', truncating='post', maxlen=maxlen)

label_encoder = LabelEncoder()
y_train_enc = label_encoder.fit_transform(y_train_text)
y_test_enc = label_encoder.transform(y_test_text)

np.save('token/train_pad/X_train.npy', X_train_pad)
np.save('token/train_pad/X_test.npy', X_test_pad)
np.save('token/train_pad/y_train_v3.npy', y_train_enc)
np.save('token/train_pad/y_test_v3.npy', y_test_enc)

with open('token/tokenizer.pkl', 'wb') as f:
    pickle.dump(tokenizer, f)

with open('token/maxlen_v2.txt', 'w') as mx:
    mx.write(str(maxlen))

with open('token/label_encoder.pkl', 'wb') as f:
    pickle.dump(label_encoder, f)

print("Tokenization done")