import json
import os
import pandas as pd

def extract_summary_features(mal_folder):
    all_api_calls = []

    for file_name in os.listdir(mal_folder):
        mal_file = os.path.join(mal_folder, file_name)

        if mal_file.endswith('.json'):
            try:
                with open(mal_file, "r") as f:
                    data = json.load(f)
                    api_data = data["behavior"]["summary"].get("resolved_apis", [])
                    # api_data = data["summary"].get("resolved_apis", [])
                    print(api_data)

                    if api_data :
                        all_api_calls.extend(api_data)
            except Exception as e:
                print(f"Error in file {file_name}: {e}")
    
    return all_api_calls

# def save_api_data_mal_to_csv(api_data_list, output_file):
#     df = pd.DataFrame(api_data_list)
#     df.insert(0, 'label', 'malware')
#     df.to_csv(output_file, index=False)
#     print(f"File save to {output_file}")

extracted = extract_summary_features(mal_folder='dataset')
def save_api_data_mal_to_txt(api_data_list, output_file):
    with open(output_file, "w", encoding='utf-8')  as f:
        f.write(''.join(api_data_list))

# save_api_data_mal_to_csv(extracted, output_file='dataset_feature/api-mal-extracted.csv')
save_api_data_mal_to_txt(extracted, output_file='dataset_feature/txt/api-mal-extracted.txt')
