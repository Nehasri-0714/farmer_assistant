import json
import cv2
import os

# CONFIG
video_path = "client_videos/sample.mp4"
pose_path = "knowledge_base/step_poses.json"
output_dir = "knowledge_base/reference_frames"

# Load step poses
with open(pose_path) as f:
    step_poses = json.load(f)

# Create output folder
os.makedirs(output_dir, exist_ok=True)

# Open video
cap = cv2.VideoCapture(video_path)

# Step → First frame number
step_frames = {
    step: poses[0]["frame"] for step, poses in step_poses.items() if poses
}

# Save one frame per step
for step, frame_no in step_frames.items():
    cap.set(cv2.CAP_PROP_POS_FRAMES, frame_no - 1)
    ret, frame = cap.read()
    if ret:
        clean_name = step.replace(" ", "_").replace(":", "").replace("?", "")
        out_path = os.path.join(output_dir, f"{clean_name}.jpg")
        cv2.imwrite(out_path, frame)
        print(f"✅ Saved: {out_path}")
    else:
        print(f"❌ Couldn't capture frame for {step}")

cap.release()
print("📸 All reference frames saved.")
