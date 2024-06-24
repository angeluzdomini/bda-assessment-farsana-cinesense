import os
import time
import spacy
import nltk
from nrclex import NRCLex
from collections import Counter
from multiprocessing import Pool

from src.utils import get_video_file_names

def emotion_analysis_worker(text):
  # Load spaCy model
  nlp = spacy.load('en_core_web_sm')
  doc = nlp(text)
  tokens = [token.text for token in doc]
  # Perform emotion analysis using NRCLex
  emotion = NRCLex(' '.join(tokens))
  # Count the emotions
  emotion_counts = Counter(emotion.raw_emotion_scores)
  return emotion_counts

# Extract emotions from text using multiprocessing
def extract_emotions(text_path, output_path):
  with open(text_path, "r") as file:
      text = file.read()
  with Pool() as pool:
    results = pool.map(emotion_analysis_worker, [text])

  emotion_counts = results[0]
  # Write the emotion counts to a file
  emotions_path = os.path.join(output_path, "emotions.txt")
  with open(emotions_path, "w") as file:
      for emotion, count in emotion_counts.items():
          file.write(f"{emotion}: {count}\n")
  return emotions_path

if __name__ == "__main__":
  # Download NLTK data
  nltk.download('punkt')
  video_file_names = get_video_file_names('../../output/video')
  for video_file_name in video_file_names:
    text_path = f'../../output/transcribe/{video_file_name}/transcription.txt'
    output_path = f'../../output/emotion/{video_file_name}'
    if not os.path.exists(output_path):
      os.makedirs(output_path)
    t1 = time.perf_counter()
    extract_emotions(text_path, output_path)
    t2 = time.perf_counter()
    print(f'Emotions analysis using multiprocessing finished in {t2 - t1} seconds for {video_file_name}.')