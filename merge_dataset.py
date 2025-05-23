import pandas as pd

# malware_csv = 'dataset_feature/cleaned/pseudo_sequence_malware_cleaned.csv'
# # benign_csv = 'dataset_feature/cleaned/pseudo_sequence_benign_cleaned.csv'
# additional_csv = 'dataset_feature/cleaned/additional_ransome_dataset_v5.csv'

# df_malware = pd.read_csv(malware_csv)
# # df_benign = pd.read_csv(benign_csv)
# df_additional = pd.read_csv(additional_csv)

# # Add label if not there
# if 'label' not in df_malware.columns:
#     df_malware['label'] = 'malware'
# if 'label' not in df_additional.columns:
#     df_additional['label'] = 'malware'

# df_combined = pd.concat([df_malware, df_additional], ignore_index=True)

# df_combined.to_csv('dataset_feature/cleaned/pseudo_sequence_mal_new.csv', index=False)
# print("✅ Dataset digabung dan disimpan ke 'pseudo_sequence_mal_new.csv'")

file1 = 'dataset_feature/sequence/pseudo_sequence_mal_dataset.csv'
file2 = 'dataset_feature/sequence/virlock_dataset_cleaned.csv'
file3 = 'dataset_feature/sequence/virustotal_sequences_v4_no_duplicate.csv'
file4 = 'dataset_feature/sequence/additional_ransome_new_no_duplicate.csv'

df1 = pd.read_csv(file1)[['sequence', 'label']].sample(n=4000, random_state=42)

df2 = pd.read_csv(file2)[['sequence', 'label']]

df3 = pd.read_csv(file3)[['sequence', 'label']]
df4 = pd.read_csv(file4)[['sequence', 'label']]

combined_df = pd.concat([df1, df2, df3, df4], ignore_index=True)

combined_df.to_csv('dataset_feature/sequence/combined_dataset_new.csv', index=False)
print("Combined dataset saved as combined_sequences.csv")
