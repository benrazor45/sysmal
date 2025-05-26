import csv
import json
from collections import defaultdict


# with open('reports/15_report.json', "r") as f:
#     data = json.load(f)

# api_calls = []
# api_counter = defaultdict(int)

# if 'behavior' in data and 'processes' in data['behavior']:
#     for process in data['behavior']['processes']:
#         if 'calls' in process:
#             for call in process['calls']:
#                  api_name = call.get('api')
#                  if api_name:
#                     if api_counter[api_name] < 2:
#                         api_calls.append(api_name)
#                         api_counter[api_name] += 1

# with open("reports/api_sequence.csv", "w", newline="") as csvfile:
#     writer = csv.writer(csvfile)
#     writer.writerow(["sequence"])
#     for api in api_calls:
#         writer.writerow([api])

# print("Berhasil disimpan ke api_sequence.csv")

with open('reports/2_report.json', "r") as f:
    data = json.load(f)

api_calls_with_duplicates = []
# If you want to count, you would use api_counter here
# api_counter = defaultdict(int)

if 'behavior' in data and 'processes' in data['behavior']:
    for process in data['behavior']['processes']:
        if 'calls' in process:
            for call in process['calls']:
                 api_name = call.get('api')
                 if api_name:
                    api_calls_with_duplicates.append(api_name)
                    # If counting: api_counter[api_name] += 1

# To get unique APIs while preserving order of first appearance
unique_api_calls = []
seen_apis = set()
for api in api_calls_with_duplicates:
    if api not in seen_apis:
        unique_api_calls.append(api)
        seen_apis.add(api)

with open("reports/2_api_sequence_unique.csv", "w", newline="") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["sequence"]) # Or "unique_api_calls"
    for api in unique_api_calls:
        writer.writerow([api])

print("Berhasil disimpan ke 2_api_sequence_unique.csv")


