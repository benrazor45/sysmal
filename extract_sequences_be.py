import os
import json
import pandas as pd

def clean_api(api):
    if '.' in api:
        return api.split('.')[-1]
    return api

def extract_sequence_from_json(json_path):
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
        resolved_apis = data.get('summary', {}).get('resolved_apis', [])
        if isinstance(resolved_apis, list):
            cleaned = [clean_api(api) for api in resolved_apis]

            result = []
            prev = ''
            count = 0
            for api in cleaned:
                if api == prev:
                    count += 1
                else:
                    count = 1
                if count <= 2:
                    result.append(api)
                prev = api
            return ' '.join(result)
        return ''

# malware_folder = 'dataset'
benign_folder = 'benign_dataset'
# max_files = 8600 #only extract 8600 files, since i have over 48000+ files.


def process_folder(folder, label):
    result = []
    for file_name in os.listdir(folder):
        if file_name.endswith('.json'):
            json_path = os.path.join(folder, file_name)
            sequence = extract_sequence_from_json(json_path)
            if sequence:
                result.append({'sequence': sequence, 'label': label})
    return result


# malware_data = process_folder(malware_folder, 'malware', max_files)
benign_data = process_folder(benign_folder, 'benign')

df = pd.DataFrame(benign_data)
df.to_csv('dataset_feature/sequence/pseudo_sequence_be_dataset.csv', index=False)
print("Dataset saved as pseudo_sequence_dataset.csv")
