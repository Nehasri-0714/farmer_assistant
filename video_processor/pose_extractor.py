import cv2
import mediapipe as mp
import json
import os

mp_pose = mp.solutions.pose
pose = mp_pose.Pose()
cap = cv2.VideoCapture("client_videos/sample.mp4")

poses = []
frame_no = 0

while cap.isOpened():
    success, frame = cap.read()
    if not success:
        break
    frame_no += 1
    image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = pose.process(image)

    if result.pose_landmarks:
        keypoints = []
        for lm in result.pose_landmarks.landmark:
            keypoints.append({'x': lm.x, 'y': lm.y, 'z': lm.z})
        poses.append({'frame': frame_no, 'landmarks': keypoints})

cap.release()
os.makedirs("knowledge_base", exist_ok=True)
with open("knowledge_base/raw_pose_data.json", "w") as f:
    json.dump(poses, f, indent=2)

print("✅ Pose extraction done. Saved to raw_pose_data.json")
