from flask import Flask, jsonify
import pandas as pd
import numpy as np

app = Flask(__name__)


datasets_info = [
    {"taskID": "task1", "file_path": "dataset_example.csv", "description": "All datasets"},
    {"taskID": "task2", "file_path": "school_gt.csv", "description": "Ground Truth Data"},
    #{"taskID": "task3", "file_path": "path_to_ground_truth_data.csv", "description": "Ground Truth Data"},
    # Add more datasets with their respective taskID and descriptions here
]

def load_dataset(dataset_info):
    df = pd.read_csv(dataset_info["file_path"])
    
    # For numeric columns, replace NaN with a numeric placeholder (e.g., 0) or convert to string
    numeric_columns = df.select_dtypes(include=[np.number]).columns
    df[numeric_columns] = df[numeric_columns].fillna(0)  # or use np.nan if you prefer to keep NaN
    
    # For string columns, replace NaN with empty strings
    string_columns = df.select_dtypes(include=[object]).columns
    df[string_columns] = df[string_columns].fillna('')
    
    return {
        "taskID": dataset_info["taskID"],
        "description": dataset_info["description"],
        "data": df.to_dict(orient='records')
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
