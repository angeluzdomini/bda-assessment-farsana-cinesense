import os
import time
import speech_recognition as sr
import threading

from src.utils import get_video_file_names

def transcribe_audio_worker(audio_path, text_path):
  recognizer = sr.Recognizer()
  audio_file = sr.AudioFile(audio_path)
  with audio_file as source:
    audio_data = recognizer.record(source)
  try:
    text = recognizer.recognize_google(audio_data)
  except sr.UnknownValueError:
    text = "Could not understand the audio"
  except sr.RequestError as e:
    text = f"Could not request results from Google Speech Recognition service; {e}"
  with open(text_path, "w") as file:
    file.write(text)

# Transcribe audio using threading
def transcribe_audio(audio_path, output_path):
  text_path = os.path.join(output_path, "transcription.txt")
  thread = threading.Thread(target=transcribe_audio_worker, args=(audio_path, text_path))
  thread.start()
  thread.join()
  return text_path

if __name__ == "__main__":
  video_file_names = get_video_file_names('../../output/video')
  for video_file_name in video_file_names:
    audio_path = f'../../output/audio/{video_file_name}/audio.wav'
    output_path = f'../../output/transcribe/{video_file_name}'
    if not os.path.exists(output_path):
      os.makedirs(output_path)
    t1 = time.perf_counter()
    transcribe_audio(audio_path, output_path)
    t2 = time.perf_counter()
    print(f'Transcribing audio using multiprocessing finished in {t2 - t1} seconds for {video_file_name}.')
