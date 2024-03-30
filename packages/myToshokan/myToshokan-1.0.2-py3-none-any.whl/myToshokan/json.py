import json

def read_json_file(input_json_path):
    with open(input_json_path, 'r') as file:
        return json.load(file)

def write_json_file(response, output_json_path):
  with open(output_json_path, 'w') as json_file:
    json.dump(response, json_file, indent=4, ensure_ascii=False)
