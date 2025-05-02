import pandas as pd

df = pd.read_csv('dataset_feature\sequence\pseudo_sequence_be_dataset.csv')
# df = pd.read_csv('dataset_feature\sequence\pseudo_sequence_mal_dataset.csv')

df_cleaned = df[~df['sequence'].str.contains(r'#218|#217')]

df_cleaned.to_csv('dataset_feature/cleaned/pseudo_sequence_benign_cleaned.csv', index=False)
# df_cleaned.to_csv('dataset_feature/cleaned/pseudo_sequence_mal_cleaned.csv', index=False)

print("Cleaning selesai. Data disimpan di pseudo_sequence_benign_cleaned.csv")
