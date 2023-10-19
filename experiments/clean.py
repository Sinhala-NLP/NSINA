import os
import json

def merge_json_files(root_dir, output_file):
    merged_data = []

    for foldername, subfolders, filenames in os.walk(root_dir):
        for filename in filenames:
            if filename.endswith('.json'):
                file_path = os.path.join(foldername, filename)
                with open(file_path, 'r',encoding="utf8") as json_file:
                    try:
                        data = json.load(json_file)
                        merged_data.append(data)
                    except json.JSONDecodeError:
                        print(f"Error reading file: {file_path}")

    with open(output_file, 'w') as output_json:
        json.dump(merged_data, output_json)

if __name__ == "__main__":
    root_directory = "data/"  # Change this to the directory where your JSON files are located
    output_filename = "NSINa.json"  # Change this to your desired output filename

    merge_json_files(root_directory, output_filename)