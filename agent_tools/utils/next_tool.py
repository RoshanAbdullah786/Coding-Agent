import json
import os
from Agents.agent_tools.utils.file_operations.path_normalizer import fix_path
from Agents.logg.logger import logger
def next_task_g():
    summary_path = os.path.join('tasks', 'tasks_summary.json')
    summary_path = fix_path(summary_path)
    # Load the task list
    with open(summary_path, 'r', encoding="utf-8") as f:
        tasks = json.load(f)

    # Step 1: Complete the task that is currently "Working"
    for task in tasks:
        if task['status'] == 'Working':
            task['status'] = 'Completed'
            break  # Assume only one task can be "Working" at a time

    # Step 2: Assign the next "Not Completed" task to "Working"
    next_task_content = None
    for task in tasks:
        if task['status'] == 'Not Completed':
            task['status'] = 'Working'
            try:
                with open(task['file_path'], 'r',encoding="utf-8") as tf:
                    next_task_content = tf.read()
            except FileNotFoundError:
                next_task_content = f"File not found: {task['file_path']}"
            break

    # Save the updated task list
    with open(summary_path, 'w', encoding="utf-8") as f:
        json.dump(tasks, f, indent=4)

    return next_task_content
def next_task():
    logger.info("Coding Agent -- Using Next Task tool ")
    next_task_c = next_task_g()
    logger.info("Coding Agent -- Next Task tool has been used")
    if next_task_c:
        return f"Next task to work on: \n{next_task_c}"
    else:
        return "All tasks are completed!"