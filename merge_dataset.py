import pandas as pd

malware_csv = 'dataset_feature\cleaned\pseudo_sequence_malware_cleaned.csv'
benign_csv = 'dataset_feature\cleaned\pseudo_sequence_benign_cleaned.csv'

df_malware = pd.read_csv(malware_csv)
df_benign = pd.read_csv(benign_csv)

# Add label if not there
if 'label' not in df_malware.columns:
    df_malware['label'] = 'malware'
if 'label' not in df_benign.columns:
    df_benign['label'] = 'benign'

df_combined = pd.concat([df_malware, df_benign], ignore_index=True)

df_combined.to_csv('dataset_feature/cleaned/combined_dataset.csv', index=False)
print("✅ Dataset digabung dan disimpan ke 'combined_dataset.csv'")
