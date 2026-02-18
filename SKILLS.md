# Agent Skills for File-Based Operations

This document defines reusable "Agent Skills" for performing file-based operations in a folder project using standard Python file I/O.

## Skill: List_and_read_pending_tasks

**Purpose**: Scan Needs_Action/ folder and read contents of .md files

**Description**: This skill scans the Needs_Action/ folder to identify all pending tasks by looking for .md files. It then reads the content of each .md file to provide a comprehensive overview of pending tasks.

**Example Claude Instructions**:
```
Please scan the Needs_Action/ folder and list all pending tasks. For each task file, read and summarize the content to help me understand what needs to be done.
```

**Implementation Example**:
```python
import os
from pathlib import Path

def list_and_read_pending_tasks():
    needs_action_dir = Path("Needs_Action")
    task_files = list(needs_action_dir.glob("*.md"))

    tasks = []
    for task_file in task_files:
        with open(task_file, 'r', encoding='utf-8') as f:
            content = f.read()
            tasks.append({
                'filename': task_file.name,
                'content': content
            })

    return tasks

# Example usage
pending_tasks = list_and_read_pending_tasks()
for task in pending_tasks:
    print(f"File: {task['filename']}")
    print(f"Content: {task['content'][:200]}...")  # First 200 chars
```

**Expected Output**:
- List of all .md files in Needs_Action/ folder
- Content of each task file for review

---

## Skill: Create_simple_plan

**Purpose**: Read one task file and generate Plan_*.md with checklist

**Description**: This skill reads a single task file from Needs_Action/, analyzes its content, and creates a structured plan in the form of a Plan_*.md file with a checklist of actionable items.

**Example Claude Instructions**:
```
Based on the task file FILE_report_analysis.md in Needs_Action/, create a detailed plan with a checklist of steps needed to complete this task. Save it as Plan_report_analysis.md.
```

**Implementation Example**:
```python
import os
from pathlib import Path

def create_simple_plan(task_filename):
    # Read the task file
    task_path = Path("Needs_Action") / task_filename
    with open(task_path, 'r', encoding='utf-8') as f:
        task_content = f.read()

    # Extract the base name for the plan file
    base_name = task_path.stem.replace('FILE_', '')
    plan_filename = f"Plan_{base_name}.md"
    plan_path = Path("Needs_Action") / plan_filename

    # Generate a simple plan based on the task content
    plan_content = f"""# Plan for {base_name}

## Original Task
{task_content}

## Action Items
- [ ] Analyze the requirements
- [ ] Gather necessary resources
- [ ] Execute the primary task
- [ ] Review and validate results
- [ ] Document the outcomes
- [ ] Mark task as complete
"""

    # Write the plan file
    with open(plan_path, 'w', encoding='utf-8') as f:
        f.write(plan_content)

    return plan_path

# Example usage
plan_file = create_simple_plan("FILE_report_analysis.md")
print(f"Created plan file: {plan_file}")
```

**Expected Output**:
- New Plan_*.md file in Needs_Action/ folder
- Checklist of steps to complete the original task

---

## Skill: Mark_task_complete

**Purpose**: Move processed file + plan to Done/ folder and update Dashboard.md

**Description**: This skill moves completed task files and their corresponding plan files from Needs_Action/ to Done/, and updates the Dashboard.md file to reflect the completion of the task.

**Example Claude Instructions**:
```
Mark the task FILE_data_processing.md as complete by moving it and its plan file Plan_data_processing.md to the Done/ folder. Update the dashboard to reflect this completion.
```

**Implementation Example**:
```python
import os
from pathlib import Path
from datetime import datetime

def mark_task_complete(task_filename, plan_filename=None):
    needs_action_dir = Path("Needs_Action")
    done_dir = Path("Done")
    done_dir.mkdir(exist_ok=True)  # Create Done/ if it doesn't exist

    # Move the task file
    task_src = needs_action_dir / task_filename
    task_dest = done_dir / task_filename
    task_src.rename(task_dest)

    # Move the plan file if provided
    if plan_filename:
        plan_src = needs_action_dir / plan_filename
        plan_dest = done_dir / plan_filename
        if plan_src.exists():
            plan_src.rename(plan_dest)

    # Update the dashboard
    update_dashboard_on_completion(task_filename)

    return f"Moved {task_filename} and {plan_filename or 'no plan file'} to Done/"

def update_dashboard_on_completion(completed_task):
    dashboard_path = Path("Dashboard.md")

    # Read current dashboard content
    if dashboard_path.exists():
        with open(dashboard_path, 'r', encoding='utf-8') as f:
            content = f.read()
    else:
        content = "# AI Employee Dashboard\n\n## Status\n- Last checked: \n- Pending actions: 0\n- Recent activity: \n\n## Bank / Finance\n- Current balance: \n- Last transaction: \n\n## Recent Updates"

    # Update the timestamp and recent activity
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M")
    updated_content = content.replace(
        "## Status\n- Last checked: ",
        f"## Status\n- Last checked: {current_time}\n"
    )

    # Add completion to recent activity
    recent_activity_start = "Recent activity: "
    if recent_activity_start in updated_content:
        updated_content = updated_content.replace(
            recent_activity_start,
            f"Recent activity: {current_time} - Completed {completed_task}; "
        )

    # Write updated content back to dashboard
    with open(dashboard_path, 'w', encoding='utf-8') as f:
        f.write(updated_content)

# Example usage
result = mark_task_complete("FILE_data_processing.md", "Plan_data_processing.md")
print(result)
```

**Expected Output**:
- Task file moved to Done/ folder
- Plan file (if exists) moved to Done/ folder
- Dashboard.md updated with completion information