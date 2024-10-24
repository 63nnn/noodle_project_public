import csv
import json

def csv_to_jsonl(csv_file, jsonl_file):
    with open(csv_file, 'r', encoding='utf-8') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        with open(jsonl_file, 'w', encoding='utf-8') as jsonl_file:
            for row in csv_reader:
                message = {
                    "messages": [
                        {"role": "system", "content": row["instruction"]},
                        {"role": "user", "content": row["user"]},
                        {"role": "assistant", "content": row["model"]}
                    ]
                }
                jsonl_file.write(json.dumps(message, ensure_ascii=False) + '\n')

csv_to_jsonl('../datasets/Noodle Traning data_with_instruction_for_gpt.csv', 'noodle_gpt.jsonl')
