import time
import threading
from src.utils import *

video_urls = load_data('../../resources/video_urls.txt')
# Specify the folder and file name
log_folder_name = "../../output/log"
log_file_name = "log.txt"
log_file_path = os.path.join(log_folder_name, log_file_name)

#Create a semaphore with a maximum of 5 threads
connection_semaphore = threading.Semaphore(5)
# Create a lock object to ensure only one thread writes to the file at a time
log_file_lock = threading.Lock()

def download_video(video_url):
  # Acquire the semaphore before downloading video
  connection_semaphore.acquire()

  try:
    # Download video using utils
    get_video(video_url)

  finally:
    # Release the semaphore after video is downloaded
    connection_semaphore.release()
    log(video_url)

def log(video_url):
  log_file_lock.acquire()
  try:
    with open(log_file_path, "a") as file:
      log_entry = f"\"Timestamp\":" + time.ctime() + ", \"URL\":\"" + video_url + ", \"Download\":True\n"
      file.write(log_entry)
  finally:
    # Release the lock after writing to the file
    log_file_lock.release()

# Function to run the download_video in a thread
def thread_function(data):
  download_video(video_url)

if __name__ == "__main__":
  # Create the folder if it doesn't exist
  os.makedirs(log_folder_name, exist_ok=True)
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