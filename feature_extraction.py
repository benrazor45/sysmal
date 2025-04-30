import json
import os
import pandas as pd
from collections import Counter


def extract_summary_features(json_folder, output_csv):
    data_rows = []
    # api_counter_global = Counter()

    #Pilih TOP_N dari resolve_api
    # for filename in os.listdir(json_folder):
    #     if not filename.endswith('.json'):
    #         break

    #     file_path = os.path.join(json_folder, filename)
    #     with open(file_path, 'r', encoding='utf-8') as f:
    #         try:
    #             report = json.load(f)
    #             summary = report.get('behavior', {}).get('summary', {})
    #             resolved_apis = summary.get('resolved_apis', {})

    #             if isinstance(resolved_apis, dict):
    #                 api_counter_global.update(resolved_apis)
    #             elif isinstance(resolved_apis, list):
    #                 api_counter_global.update(resolved_apis)

    #         except Exception as e:
    #             print(f"Error reading APIs from {filename}: {e}")
    #             break

    # top_apis = [api for api, _ in api_counter_global.most_common(top_n_apis)]

    #Ekstrak fitur
    for filename in os.listdir(json_folder):
        if not filename.endswith('.json'):
            break

        file_path = os.path.join(json_folder, filename)
        with open(file_path, 'r', encoding='utf-8') as f:
            try:
                report = json.load(f)
                # summary = report.get('behavior', {}).get('summary', {})
                summary = report.get('summary', {})
                api_stats = len(summary.get('resolved_apis', []))

                # name_parts = filename.replace(".json", "").split("_")
                # if len(name_parts) < 0:
                #     print(f"Format nama file tidak sesuai: {filename}")
                #     break
                mal_name = f"goodware"
                category = f"benign"
                # sha256 = "_".join(name_parts[2:])

                row = {
                    'name': mal_name,
                    'category': category,
                    'resolved_apis': api_stats,
                    'open_key': len(summary.get('keys', [])),
                    'key_log': len(summary.get('read_keys', [])),
                    'write_key': len(summary.get('write_keys', [])),
                    'delete_key': len(summary.get('delete_keys', [])),
                    'executed_commands': len(summary.get('executed_commands', [])),
                    'open_file': len(summary.get('files', [])),
                    'read_file': len(summary.get('read_files', [])),
                    'write_file': len(summary.get('write_files', [])),
                    'delete_file': len(summary.get('delete_files', [])),
                    'started_service': len(summary.get('started_services', [])),
                    'created_service': len(summary.get('created_services', [])),
                    'mutexes': len(summary.get('mutexes', []))
                }
                print(row)

                # Ambil Top-N API dari laporan
                # api_counter = Counter()
                # if isinstance(resolved_apis, dict):
                #     api_counter.update(resolved_apis)
                # elif isinstance(resolved_apis, list):
                #     api_counter.update(resolved_apis)

                # for api in top_apis:
                #     row[f'api_{api}'] = api_counter.get(api, 0)

                data_rows.append(row)
                print("masih berjalan")

            except Exception as e:
                print(f"Error processing {filename}: {e}")
                break

    df = pd.DataFrame(data_rows)
    df.fillna(0, inplace=True)
    df.to_csv(output_csv, index=False)
    print(f"Sukses menyimpan fitur ke {output_csv}")


extract_summary_features(json_folder='benign_dataset', output_csv='dataset_feature/full-features-benign.csv')
