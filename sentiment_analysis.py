import os
import time
from textblob import TextBlob
from multiprocessing import Pool

from src.utils import get_video_file_names


def sentiment_analysis_worker(text):
  blob = TextBlob(text)
  return blob.sentiment.polarity, blob.sentiment.subjectivity

# Analyze sentiment form text using multiprocessing
def analyze_sentiment(text_path, output_path):
  with open(text_path, "r") as file:
    text = file.read()

  with Pool() as pool:
    results = pool.map(sentiment_analysis_worker, [text])

  polarity, subjectivity = results[0]

  sentiment_path = os.path.join(output_path, "sentiment.txt")
  with open(sentiment_path, "w") as file:
    file.write(f"Polarity: {polarity}\n")
    file.write(f"Subjectivity: {subjectivity}\n")

  return sentiment_path

if __name__ == "__main__":
  video_file_names = get_video_file_names('../../output/video')
  for video_file_name in video_file_names:
    text_path = f'../../output/transcribe/{video_file_name}/transcription.txt'
    output_path = f'../../output/sentiment/{video_file_name}'
    if not os.path.exists(output_path):
      os.makedirs(output_path)
    t1 = time.perf_counter()
    analyze_sentiment(text_path, output_path)
    t2 = time.perf_counter()
    print(f'Sentiment analysis using multiprocessing finished in {t2 - t1} seconds for {video_file_name}.')
