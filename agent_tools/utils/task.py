import os
import json
import re

def task_creator():
    # Define the folder path
    folder_path = 'workspace/tasks'

    # Create a pattern to match task files like task-1.txt, task-2.txt, etc.
    task_pattern = re.compile(r'task-(\d+)\.txt')

    # Collect task info
    task_list = []

    for filename in os.listdir(folder_path):
        match = task_pattern.match(filename)
        if match:
            task_id = int(match.group(1))
            file_path = os.path.join(folder_path, filename)
            task_list.append({
                "task id": task_id,
                "status": "Not Completed",
                "file_path": file_path
            })

    # Sort tasks by ID
    task_list.sort(key=lambda x: x["task id"])

    # Write to JSON file
    output_path = os.path.join(folder_path, 'tasks_summary.json')
    with open(output_path, 'w',encoding="utf-8") as json_file:
        json.dump(task_list, json_file, indent=4)

    print(f"Created summary with {len(task_list)} tasks at {output_path}")
