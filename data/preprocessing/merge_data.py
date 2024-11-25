import csv
import os
import pandas as pd
import json


def load_json_files_and_merge(base_directory):
    lst = []
    # 디렉토리 내의 모든 json 파일 순회
    for filename in os.listdir(base_directory):
        if filename.endswith('.json'):
            file_path = os.path.join(base_directory, filename)

            df = pd.read_json(file_path)
            df = df.dropna()
            df['date'] = df['date'].astype(str)

            lst += df.to_dict(orient='records')       
                
    return lst


merged_data_list = load_json_files_and_merge('.')


file_path = 'indiewire_data.json'

with open(file_path, 'w', encoding='utf-8') as f:
    json.dump(merged_data_list, f, ensure_ascii=False, indent=4)
