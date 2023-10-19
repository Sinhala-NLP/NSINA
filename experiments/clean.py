import os
import json
import codecs

def merge_json_files(root_dir, output_file):
    merged_data = []

    for foldername, subfolders, filenames in os.walk(root_dir):
        print(foldername)
        for filename in filenames:
            if filename.endswith('.json'):
                file_path = os.path.join(foldername, filename)
                with codecs.open(file_path, 'r', encoding='utf-8') as json_file:
                    try:
                        data = json.load(json_file)
                        merged_data.append(data)
                    except json.JSONDecodeError:
                        print(f"Error reading file: {file_path}")

    with codecs.open(output_file, 'w', encoding='utf-8') as output_json:
        json.dump(merged_data, output_json, ensure_ascii=False)

if __name__ == "__main__":
    root_directory = "data/"  # Change this to the directory where your JSON files are located
    output_filename = "merged.json"  # Change this to your desired output filename

    merge_json_files(root_directory, output_filename)