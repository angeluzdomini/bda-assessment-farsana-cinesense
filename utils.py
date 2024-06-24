import os  # Import the os module for interacting with the operating system
from os import listdir
from os.path import isfile, join
from pytube import YouTube  # Import the Youtube module for handling youtube videos

def load_data(file_path):
  video_url_list = []
  with open(file_path, 'r') as file:
    for line in file:
      line_data = line.strip()
      video_url_list.append(line_data)
  return(video_url_list)

def get_video(video_url):
  # Define the output directory where images will be saved
  output_dir = "../../output/video"
  # Create the output directory if it does not exist, if exists do not create
  os.makedirs(output_dir, exist_ok=True)
  yt = YouTube(video_url)
  stream = yt.streams.get_highest_resolution()
  stream.download(output_path=output_dir)

def get_video_file_names(video_folder):
  video_files = [f for f in listdir(video_folder) if isfile(join(video_folder, f))]
  video_file_names = [s.replace('.mp4', '') for s in video_files]
  return video_file_names