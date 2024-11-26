import csv
import os
import pandas as pd
import json


def load_json_files_and_merge(base_directory):
    lst = []
    merged_df = pd.DataFrame()
    # 디렉토리 내의 모든 json 파일 순회
    for filename in os.listdir(base_directory):
        if filename.endswith('.json'):
            file_path = os.path.join(base_directory, filename)

            df = pd.read_json(file_path)
            df = df.dropna()
            df['date'] = df['date'].astype(str)
            df['keywords'] = df['keywords'].str.replace(r"IndieWire, |, IndieWire| IndieWire,|, Indiewire", "", regex=True)

            df = df.drop_duplicates()
            merged_df = pd.concat([merged_df, df], ignore_index=True)

    lst = merged_df.to_dict(orient='records') 

    return lst


merged_data_list = load_json_files_and_merge('.')


file_path = 'indiewire_data.json'

with open(file_path, 'w', encoding='utf-8') as f:
    json.dump(merged_data_list, f, ensure_ascii=False, indent=4)
