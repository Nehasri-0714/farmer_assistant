import cv2
import mediapipe as mp
import json

def extract_poses(video_path):
    cap = cv2.VideoCapture(video_path)
    mp_pose = mp.solutions.pose
    pose = mp_pose.Pose()
    results = {}

    frame_id = 0
    while cap.isOpened():
        success, image = cap.read()
        if not success: break
        frame_id += 1
        if frame_id % 30 != 0: continue  # Sample every second (30 FPS)

        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        result = pose.process(image_rgb)
        if result.pose_landmarks:
            results[f"frame_{frame_id}"] = [
                {
                    "x": lm.x,
                    "y": lm.y,
                    "z": lm.z
                }
                for lm in result.pose_landmarks.landmark
            ]

    with open("knowledge_base/step_poses.json", "w") as f:
        json.dump(results, f)

    print("Pose data saved to step_poses.json")
