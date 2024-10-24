import csv
import json


def converter(source, destination):
    json_output = []

    with open(source, "r", encoding="utf-8") as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            if row != "":
                instruction_text = row["user"]
                input_text = ""
                output_text = row["model"]
                json_output.append(
                    {
                        "instruction": instruction_text,
                        "input": input_text,
                        "output": output_text,
                    }
                )

    with open(destination, "w", encoding="utf-8") as json_file:
        json.dump(json_output, json_file, ensure_ascii=False, indent=4)


type_num = "type3"


dir_now = f"./training/datasets/{type_num}/"
source = f"{type_num}.csv"
destination = f"{type_num}_noodle_llama.json"
converter(f"{dir_now}{source}", f"{dir_now}{destination}")
