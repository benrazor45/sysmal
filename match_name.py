import os
import json
import pandas as pd

# def match_and_rename_json(json_folder, csv_file):
#     try:
#         df = pd.read_csv(csv_file)
#         print(f"CSV loaded successfully with {len(df)} rows.")
#     except Exception as e:
#         print(f"Error loading CSV: {e}")
#         return

#     df['sha256'] = df['sha256'].str.strip()

#     file_category_dict = {
#         row['sha256']: (row['classification_family'], row['classification_type']) for _, row in df.iterrows()
#     }
#     print(f"Category dictionary: {file_category_dict}")

#     try:
#         json_files = [f for f in os.listdir(json_folder) if f.endswith('.json')]
#         print(f"Found {len(json_files)} JSON files in the folder.")
#     except Exception as e:
#         print(f"Error accessing folder: {e}")
#         return

#     for json_file in json_files:
#         print(f"Processing file: {json_file}")
        
#         base_name = os.path.splitext(json_file)[0]
        
#         file_category = file_category_dict.get(base_name)

#         if not file_category:
#             print(f"No category found for {json_file} (base name: {base_name}). Skipping.")
#             continue
        
#         classification_family, classification_type = file_category
#         print(f"Classification family: {classification_family}, Classification type: {classification_type}")
        
#         new_name = f"{classification_family}_{classification_type}_{json_file}"
#         new_path = os.path.join(json_folder, new_name)

#         try:
#             os.rename(os.path.join(json_folder, json_file), new_path)
#             print(f"File {json_file} renamed to {new_name}.")
#         except Exception as e:
#             print(f"Error renaming file {json_file}: {e}")
#             continue

def rename_benign_files(benign_folder):
    try :
        json_file = [f for f in os.listdir(benign_folder)]
        print(f"Found {len(json_file)} JSON files in the folder.")
    except Exception as e:
        print("No JSON data was found", e)
    
    for files in json_file :
        base_name = os.path.splitext(files)[0]
        new_name = base_name + '.json'
        new_path = os.path.join(benign_folder, new_name)

        try:
            os.rename(os.path.join(benign_folder, files), new_path)
            # print(f"File {files} renamed to {new_name}")
        except Exception as e:
            print(f"Error renaming file", e)


# json_folder = 'dataset'  
# csv_file = 'public_labels.csv' 
benign_folder = 'benign_dataset'

rename_benign_files(benign_folder)
# match_and_rename_json(json_folder, csv_file)
