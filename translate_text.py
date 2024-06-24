import os
import time
from googletrans import Translator
import asyncio

from src.utils import get_video_file_names

async def translate_text_worker(text, target_language):
  translator = Translator()
  translated = translator.translate(text, dest=target_language)
  return translated.text

# Translate from English to target language using asyncio
async def translate_text_async(text_path, output_path, target_language="es"):
  with open(text_path, "r") as file:
    text = file.read()

  translated_text = await translate_text_worker(text, target_language)

  translation_path = os.path.join(output_path, f"translation_{target_language}.txt")
  with open(translation_path, "w") as file:
    file.write(translated_text)

  return translation_path

if __name__ == "__main__":

  target_language = "es"
  video_file_names = get_video_file_names('../../output/video')
  for video_file_name in video_file_names:
    text_path = f'../../output/transcribe/{video_file_name}/transcription.txt'
    output_path = f'../../output/translate/{video_file_name}'
    if not os.path.exists(output_path):
      os.makedirs(output_path)
    t1 = time.perf_counter()
    asyncio.run(translate_text_async(text_path, output_path, target_language))
    t2 = time.perf_counter()
    print(f'Translating from "en" to "{target_language}" using multiprocessing finished in {t2 - t1} seconds for {video_file_name}.')
