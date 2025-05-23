from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.preprocessing.text import Tokenizer
import base64

def decode_base64_ps(encoded_str):
    try:
        return base64.b64decode(encoded_str).decode('utf-16le')
    except Exception:
        return encoded_str

def preprocess_sequence(text):
    # Jika ada base64 powershell, decode dulu (contoh deteksi sederhana)
    if "powershell -e " in text:
        parts = text.split()
        for i, part in enumerate(parts):
            if part == "-e" and i+1 < len(parts):
                parts[i+1] = decode_base64_ps(parts[i+1])
        text = " ".join(parts)

    # Lowercase
    text = text.lower()

    # Tokenisasi spasi
    tokens = text.split()

    # Contoh hapus token noise (bisa ditambah)
    noise_tokens = {"/c", "|", "&", ";", "/y",}
    tokens = [t for t in tokens if t not in noise_tokens]

    # Contoh normalisasi angka ke <num>
    tokens = [t if not t.isdigit() else "<num>" for t in tokens]

    return tokens

# Contoh input
data = {
"powershell -e RwBlAHQALQBXAG0AaQBPAGIAagBlAGMAdAAgAFcAaQBuADMAMgBfAFMAaABhAGQAbwB3AGMAbwBwAHkAIAB8ACAARgBvAHIARQBhAGMAaAAtAE8AYgBqAGUAYwB0ACAAewAkAF8ALgBEAGUAbABlAHQAZQAoACkAOwB9AA==",
"exe -e RwBlAHQALQBXAG0AaQBPAGIAagBlAGMAdAAgAFcAaQBuADMAMgBfAFMAaABhAGQAbwB3AGMAbwBwAHkAIAB8ACAARgBvAHIARQBhAGMAaAAtAE8AYgBqAGUAYwB0ACAAewAkAF8ALgBEAGUAbABlAHQAZQAoACkAOwB9AA=="
}



tokens = preprocess_sequence(data)
print(tokens)

# Tokenizer dan padding
tokenizer = Tokenizer()
tokenizer.fit_on_texts([tokens])
seq = tokenizer.texts_to_sequences([tokens])
padded_seq = pad_sequences(seq, maxlen=100, padding='post')
print(padded_seq)
