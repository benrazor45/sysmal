import pandas as pd

malware_csv = 'dataset_feature/cleaned/pseudo_sequence_malware_cleaned.csv'
# benign_csv = 'dataset_feature/cleaned/pseudo_sequence_benign_cleaned.csv'
additional_csv = 'dataset_feature/cleaned/additional_ransome_dataset_v5.csv'

df_malware = pd.read_csv(malware_csv)
# df_benign = pd.read_csv(benign_csv)
df_additional = pd.read_csv(additional_csv)

# Add label if not there
if 'label' not in df_malware.columns:
    df_malware['label'] = 'malware'
if 'label' not in df_additional.columns:
    df_additional['label'] = 'malware'

df_combined = pd.concat([df_malware, df_additional], ignore_index=True)

df_combined.to_csv('dataset_feature/cleaned/pseudo_sequence_mal_new.csv', index=False)
print("✅ Dataset digabung dan disimpan ke 'pseudo_sequence_mal_new.csv'")
