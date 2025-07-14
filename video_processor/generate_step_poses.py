import json
import os

FPS = 30  # Adjust if needed

# Load list of steps and convert to a dictionary
with open("knowledge_base/step_labels.json") as f:
    step_list = json.load(f)

step_times = {
    step["step"]: f"{step['start']}-{step['end']}"
    for step in step_list
}

# Load all poses
with open("knowledge_base/raw_pose_data.json") as f:
    all_poses = json.load(f)

step_poses = {}

# Convert MM:SS to frame number
def time_to_frame(time_str):
    minutes, seconds = map(int, time_str.split(":"))
    return int((minutes * 60 + seconds) * FPS)

# Assign poses to each step
for step_name, time_range in step_times.items():
    start_str, end_str = time_range.split("-")
    start_frame = time_to_frame(start_str)
    end_frame = time_to_frame(end_str)

    poses_in_range = [
        pose for pose in all_poses
        if start_frame <= pose["frame"] <= end_frame
    ]

    step_poses[step_name] = poses_in_range

# Save result
with open("knowledge_base/step_poses.json", "w") as f:
    json.dump(step_poses, f, indent=2)

print("✅ Step-wise poses saved to knowledge_base/step_poses.json")
