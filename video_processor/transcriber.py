import os
import wave
import subprocess
from vosk import Model, KaldiRecognizer
import json

def transcribe_video(video_path, model_path):
    audio_path = "temp.wav"

    # Step 1: Extract audio from video
    if not os.path.exists(video_path):
        print(f"❌ Video file not found at: {video_path}")
        return

    print("🔄 Extracting audio from video...")
    subprocess.call([
        "ffmpeg", "-i", video_path,
        "-ar", "16000", "-ac", "1",
        audio_path, "-y"
    ])

    # Step 2: Transcribe audio
    if not os.path.exists(audio_path):
        print("❌ Audio extraction failed: temp.wav not found.")
        return

    print("🔄 Loading model and transcribing...")
    wf = wave.open(audio_path, "rb")
    model = Model(model_path)
    rec = KaldiRecognizer(model, wf.getframerate())

    results = []
    while True:
        data = wf.readframes(4000)
        if len(data) == 0:
            break
        if rec.AcceptWaveform(data):
            results.append(json.loads(rec.Result())["text"])
    results.append(json.loads(rec.FinalResult())["text"])

    # Step 3: Save transcript
    transcript = " ".join(results).strip()
    os.makedirs("knowledge_base", exist_ok=True)
    with open("knowledge_base/instructions.txt", "w", encoding="utf-8") as f:
        f.write(transcript)

    print("✅ Transcription completed. Saved to knowledge_base/instructions.txt")

    wf.close()  # 🧹 Important!
    os.remove(audio_path)
    print("🧹 Temp file removed.")

# Example usage
if __name__ == "__main__":
    video_path = "client_videos/sample.mp4"
    model_path = "vosk_models/vosk-model-small-en-us-0.15"
    transcribe_video(video_path, model_path)
