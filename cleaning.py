import pandas as pd
import re

def clean_token(token):
    # Hapus prefix sebelum titik jika ada
    if '.' in token:
        token = token.split('.', 1)[1]
    # Hapus token yang mengandung karakter aneh seperti ? atau @ (mangled symbols C++)
    if re.search(r'[\?@]', token):
        return ''
    else:
        return token
    

def remove_consecutive_duplicates(tokens):
    if not tokens:
        return tokens
    result = [tokens[0]]
    for t in tokens[1:]:
        if t != result[-1]:
            result.append(t)
    return result

def filter_short_or_empty_sequences(df, column='sequence', min_tokens=3):
    def is_valid_sequence(seq):
        if not isinstance(seq, str) or seq.strip() == '':
            return False
        tokens = seq.split()
        return len(tokens) >= min_tokens
    
    return df[df[column].apply(is_valid_sequence)]

# Baca file CSV
df = pd.read_csv('dataset_feature/cleaned/combined_dataset_new_cleaned_v11.csv')

# Ganti NaN di kolom sequence dengan string kosong supaya tidak error saat split
df['sequence'] = df['sequence'].fillna('')

# Bersihkan spasi berlebih di awal dan akhir
df['sequence'] = df['sequence'].str.strip()
df['sequence'] = df['sequence'].str.replace(r'\s+', ' ', regex=True)

# Hapus semua token #angka
df['sequence'] = df['sequence'].str.replace(r'#\d+', '', regex=True)
df['sequence'] = df['sequence'].str.replace(r'\s+', ' ', regex=True)  # bersihkan spasi ganda akibat penghapusan

# Cleaning setiap sequence baris
cleaned_sequences = []
for seq in df['sequence']:
    tokens = seq.split()
    tokens = [clean_token(t) for t in tokens]
    tokens = [t for t in tokens if t]  # hilangkan token kosong dari clean_token
    tokens = remove_consecutive_duplicates(tokens)  # hilangkan duplikat token berurutan
    cleaned_seq = ' '.join(tokens)
    cleaned_seq = re.sub(r'\s+', ' ', cleaned_seq).strip()  # bersihkan spasi berlebih
    cleaned_sequences.append(cleaned_seq)

df['sequence'] = cleaned_sequences

df = filter_short_or_empty_sequences(df, 'sequence', 4)

# Pola sequence pendek yang ingin dibuang (harus cocok persis)
patterns_to_remove = {
    "GetNativeSystemInfo",
    "VirtualAlloc",
    "RegQueryValueExW",
    "GetTickCount GetTickCount Sleep Sleep",
    "Sleep Sleep",
    "GetTickCount GetTickCount",
    "SetFileTime SetFileTime",
    "GetTickCount GetTickCount IsDebuggerPresent IsDebuggerPresent SetFileTime SetFileTime",
    "GetTickCount GetTickCount SetFileTime SetFileTime",
    "GetTickCount GetTickCount IsDebuggerPresent IsDebuggerPresent",
    "IsDebuggerPresent IsDebuggerPresent SetFileTime SetFileTime",
    "GetAdaptersAddresses GetAdaptersAddresses GetTickCount GetTickCount Sleep Sleep",
    "GetAdaptersAddresses GetAdaptersAddresses GetTickCount GetTickCount GetTickCount64 GetTickCount64",
    "AES AES RSA RSA",
    "RC4 RC4 RSA RSA",
    "RSA RSA",
    "3DES 3DES RC4 RC4 RSA RSA",
    "GetTickCount GetTickCount SetFileTime SetFileTime Sleep Sleep",
    "GetSystemMetrics GetSystemMetrics GetTickCount GetTickCount SetFileTime SetFileTime Sleep Sleep",
    "FlsAlloc FlsGetValue FlsSetValue FlsFree",
    "VirtualAlloc WerRegisterMemoryBlock GetThemeBackgroundRegion",
    "SortGetHandle SortCloseHandle",
    "GetDiskFreeSpaceExA",
    "RtlExitUserThread",
    "LpkEditControl RtlExitUserThread",
    "GetTickCount IsDebuggerPresent Sleep",
    "GetSystemMetrics GetTickCount GetTickCount64 IsDebuggerPresent",
    "GetAdaptersAddresses GetTickCount GetTickCount64 Sleep",
    "chcp IsDebuggerPresent",
    "GetTickCount Sleep RegOpenKeyExW",
    "exe",
    "GetSystemMetrics GetTickCount IsDebuggerPresent SetFileTime",
    "exe" "DOS Device MODE Utility" "DOS Device MODE Utility",
    "exe" "Command Line Interface for Microsoft������ Volume Shadow Copy Service" "Command Line Interface for Microsoft������ Volume Shadow Copy Service",
    "GetAdaptersAddresses GetTickCount GetTickCount64 IsDebuggerPresent",
    "nslookup bit ru nslookup bit ru nslookup bit ru nslookup bit ru nslookup bit ru nslookup bit ru",
    "GetAdaptersAddresses GetTickCount SetFileTime Sleep",
    "GetAdaptersAddresses GetSystemMetrics GetTickCount Sleep",
    "SortCloseHandle SortGetHandle GetTickCount Sleep",
    "GetTickCount Sleep ExitProcess TerminateProcess",
    "{'file': ''} {'file': ''}",
    "GetTickCount IsDebuggerPresent exe",
    "---=== ===---[+] Whats [+]Your files are encrypted, and currently You can check it: ---=== ===---[+] Whats [+]Your files are encrypted, and currently You can check it:",
    "GetAdaptersAddresses GetSystemMetrics GetTickCount Sleep",
    "RtlWow64GetCurrentMachine RtlWow64IsWowGuestMachineSupported GetTickCount SetFileTime",
    "exe 12288 exe 12288",
    "GetAdaptersAddresses GetTickCount GetTickCount64 SetFileTime",
    "RtlWow64GetCurrentMachine RtlWow64IsWowGuestMachineSupported GetTickCount IsDebuggerPresent",
    "GetSystemMetrics GetTickCount IsDebuggerPresent Sleep",
    "GetAdaptersAddresses GetSystemMetrics GetTickCount IsDebuggerPresent Sleep",
    "GetAdaptersAddresses GetSystemMetrics GetTickCount IsDebuggerPresent SetFileTime Sleep",
    ""

}

df_cleaned = df[~df['sequence'].isin(patterns_to_remove)]
df_cleaned = df_cleaned[df_cleaned['sequence'].fillna('').str.strip() != '']


# Simpan hasil
df_cleaned.to_csv('dataset_feature/cleaned/combined_dataset_new_cleaned_v12.csv', index=False)

print("Cleaning selesai. Prefix dihapus, duplikat token berurutan dibuang, token #angka dihapus, simbol mangled dibersihkan, sequence pendek/kosong dihapus, dan sequence tidak informatif dibuang.")
