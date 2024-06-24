import os
from moviepy.editor import VideoFileClip
from concurrent.futures import ProcessPoolExecutor
import threading
import asyncio
import time

from src.utils import get_video_file_names

# Extract audio by serial processing
def extract_audio_serial(video_path, output_path):
  video = VideoFileClip(video_path)
  audio_path = os.path.join(output_path, "audio.wav")
  video.audio.write_audiofile(audio_path)
  return audio_path

def extract_audio_worker(video_path, audio_path):
  video = VideoFileClip(video_path)
  video.audio.write_audiofile(audio_path)

# Extract audio by multiprocessing
def extract_audio_multiprocessing(video_path, output_path):
  audio_path = os.path.join(output_path, "audio.wav")
  with ProcessPoolExecutor() as executor:
    future = executor.submit(extract_audio_worker, video_path, audio_path)
    future.result()
  return audio_path

# Extract audio by threading
def extract_audio_threading(video_path, output_path):
  video = VideoFileClip(video_path)
  audio_path = os.path.join(output_path, "audio.wav")
  thread = threading.Thread(target=video.audio.write_audiofile, args=(audio_path,))
  thread.start()
  thread.join()
  return audio_path

# Extract audio by asyncio
async def extract_audio_async(video_path, output_path):
  video = VideoFileClip(video_path)
  audio_path = os.path.join(output_path, "audio.wav")
  loop = asyncio.get_event_loop()
  await loop.run_in_executor(None, video.audio.write_audiofile, audio_path)
  return audio_path

# Compare different methods of processing
def compare_methods(video_path, output_path):
  methods = [
    ("Serial", extract_audio_serial),
    ("Multiprocessing", extract_audio_multiprocessing),
    ("Threading", extract_audio_threading),
    ("Asyncio", lambda vp, op: asyncio.run(extract_audio_async(vp, op))),
  ]
  results = {}
  for name, method in methods:
    t1 = time.perf_counter()
    method(video_path, output_path)
    t2 = time.perf_counter()
    results[name] = t2 - t1
  for method, duration in results.items():
    print(f'Extract audio using {method} finished in {duration} seconds for {video_path}')

if __name__ == "__main__":
  video_file_names = get_video_file_names('../../output/video')
  for video_file_name in video_file_names:
    video_path = f'../../output/video/{video_file_name}.mp4'
    output_path = f'../../output/audio/{video_file_name}'
    if not os.path.exists(output_path):
     os.makedirs(output_path)
    compare_methods(video_path, output_path)
