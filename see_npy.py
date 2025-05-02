import numpy as np

sequences = np.load('dataset_feature/tokenization/tokenized_sequences.npy', allow_pickle=True)
labels = np.load('dataset_feature/labels_tokenization/labels.npy', allow_pickle=True)

# Lihat bentuk array
print("Bentuk sequences:", sequences.shape)
print("Bentuk labels:", labels.shape)

# Tampilkan beberapa contoh
print("\nContoh sequence pertama:")
print(sequences[0])

print("\nLabel pertama:", labels[0])
