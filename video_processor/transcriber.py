from vosk import Model, KaldiRecognizer
import wave
import subprocess
import json

def transcribe_video(video_path):
    audio_path = "temp.wav"
    subprocess.call(['ffmpeg', '-i', video_path, '-ar', '16000', '-ac', '1', audio_path])
    wf = wave.open(audio_path, "rb")
    model = Model("model")
    rec = KaldiRecognizer(model, wf.getframerate())

    results = []
    while True:
        data = wf.readframes(4000)
        if len(data) == 0:
            break
        if rec.AcceptWaveform(data):
            results.append(json.loads(rec.Result())["text"])
    results.append(json.loads(rec.FinalResult())["text"])

    transcript = ' '.join(results)
    with open("knowledge_base/instructions.txt", "w") as f:
        f.write(transcript)

    print("Transcript saved to instructions.txt")
