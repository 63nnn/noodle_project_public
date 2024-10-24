import csv
import json

# 讀取CSV檔案
with open("./training/datasets/type3/type3.csv", "r", encoding="utf-8") as file:
    csv_reader = csv.DictReader(file)

    conversation_history = []
    conversation_history.append(
        {
            "text": "你是大呷麵本家元宇宙的虛擬解說員，請注意禮貌，無關於大呷麵本家相關的問題請不要回答"
        }
    )
    for row in csv_reader:
        if row != "":
            print(row)
            conversation_history.append({"text": f"user: {row["user"]}"})
            conversation_history.append({"text": f"model: {row["model"]}"})

# 將結果輸出成JSON檔案
with open("noodle_gemini_1.json", "w", encoding="utf-8") as json_file:
    for i in conversation_history:
        json_file.write(str(i))
        json_file.write(",\n")
