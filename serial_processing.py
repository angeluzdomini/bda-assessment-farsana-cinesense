from src.utils import *
import time

video_urls = load_data('../../resources/video_urls.txt')

if __name__ == "__main__":
  t1 = time.perf_counter()
  # Download video by serial processing
  for video_url in video_urls:
    get_video(video_url)
  t2 = time.perf_counter()

  print(f'Finished in {t2-t1} seconds')