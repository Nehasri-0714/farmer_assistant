import pyttsx3
import os

engine = pyttsx3.init()
engine.setProperty('rate', 150)

qa_file = "knowledge_base/qa_context.txt"
output_dir = "knowledge_base/answers_audio"
os.makedirs(output_dir, exist_ok=True)

with open(qa_file, "r", encoding="utf-8") as f:
    lines = f.readlines()

count = 0
for line in lines:
    if line.startswith("A:"):
        text = line[2:].strip()
        output_path = os.path.join(output_dir, f"answer_{count}.wav")
        engine.save_to_file(text, output_path)
        engine.runAndWait()
        print(f"🔊 Saved: {output_path}")
        count += 1
