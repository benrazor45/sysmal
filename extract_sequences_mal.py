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
        print(data)
        resolved_apis = data.get('summary', {}).get('resolved_apis', [])
        print(resolved_apis)
        if resolved_apis :
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
        elif not resolved_apis :
            print("No resolved_apis available")
            return ''

malware_folder = 'dataset-virlock/reports_summary'
# benign_folder = 'json_benign'
max_files = 1200 #only extract 8600 files, since i have over 48000+ files.


def process_folder(folder, label, max_files):
    result = []
    files = [f for f in os.listdir(folder) if f.endswith('.json')]
    files = files[:max_files] 

    for file_name in files:
        json_path = os.path.join(folder, file_name)
        sequence = extract_sequence_from_json(json_path)
        if sequence: 
            result.append({'sequence': sequence, 'label': label})
    return result


malware_data = process_folder(malware_folder, 'malware', max_files)
# benign_data = process_folder(benign_folder, 'benign')

df = pd.DataFrame(malware_data)
df.to_csv('dataset_feature/sequence/virlock_dataset.csv', index=False)
print("Dataset saved as virlock_dataset.csv")
