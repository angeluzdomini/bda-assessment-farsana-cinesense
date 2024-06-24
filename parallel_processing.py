import time
import threading
from src.utils import *

video_urls = load_data('../../resources/video_urls.txt')

#Create a semaphore with a maximum of 5 threads
connection_semaphore = threading.Semaphore(5)

def download_video(video_url):
  # Acquire the semaphore before downloading video
  connection_semaphore.acquire()

  try:
    # Download video using utils
   get_video(video_url)

  finally:
   # Release the semaphore after video is downloaded
   connection_semaphore.release()

# Function to run the download_video in a thread
def thread_function(data):
  download_video(video_url)

if __name__ == "__main__":
  # Create and start threads
  threads = []
  t1 = time.perf_counter()
  for video_url in video_urls:
    thread = threading.Thread(target=thread_function, args=(video_url,))
    threads.append(thread)
    thread.start()

  # Wait for all threads to finish
  for thread in threads:
    thread.join()

  t2 = time.perf_counter()
  print(f'Finished in {t2-t1} seconds')
