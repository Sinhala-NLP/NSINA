import os
import json
import codecs
import pandas as pd

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

def json_to_tsv(input_file, output_file):
    # Load the JSON file
    with codecs.open(input_file, 'r', encoding='utf-8') as json_file:
        data = json.load(json_file)

    # Convert JSON to a pandas DataFrame
    df = pd.json_normalize(data)

    # Save DataFrame to a tab-separated CSV
    df.to_csv(output_file, sep='\t', index=False)

if __name__ == "__main__":
    root_directory = "data/"  # Change this to the directory where your JSON files are located
    output_filename = "merged.json"  # Change this to your desired output filename
    tsv_output_filename = "merged.csv"  # Output TSV filename
    
    merge_json_files(root_directory, output_filename)
    json_to_tsv(output_filename , tsv_output_filename)
