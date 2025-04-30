import pandas as pd
import json
import os


folder = 'D:\SYSMAL\dataset'

for dataset in os.listdir(folder) :
    
    if dataset.endswith('.json'):
        file_path = os.path.join(folder, dataset)

        try :

            with open(file_path, "r") as f :
                data = json.load(f)
                
                #Ekstrak fitur
                behavior = data.get("behavior", {})
                print(behavior)
        except Exception as e:
            print("Error membuka data", e)




