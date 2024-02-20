from flask import Flask, jsonify
import csv

app = Flask(__name__)

datasets_info = [
    {"taskID": "task1", "file_path": "dataset_example.csv", "description": "All datasets"},
    {"taskID": "task2", "file_path": "school_gt.csv", "description": "Ground Truth Data"},
    # Add more datasets with their respective taskID and descriptions here
]

def load_dataset(dataset_info):
    # Initialize an empty list to store the dataset records
    data = []

    # Open the CSV file and read data
    with open(dataset_info["file_path"], mode='r', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        
        # Iterate over each row in the CSV file and add it to the data list
        for row in reader:
            # Manually handle missing values if necessary
            for key, value in row.items():
                if value == '':
                    row[key] = None  # Replace empty strings with None or a suitable placeholder
            data.append(row)

    return {
        "taskID": dataset_info["taskID"],
        "description": dataset_info["description"],
        "data": data
    }

# Function to load all datasets
def load_all_datasets():
    return [load_dataset(info) for info in datasets_info]

@app.route('/api/data', methods=['GET'])
def get_data():
    # Serve all datasets with their taskID and metadata as JSON
    return jsonify({"datasets": load_all_datasets()})

if __name__ == '__main__':
    app.run(debug=True)
