import os
import tempfile

from gtts import gTTS
from utils_base import Hash, Log

from utils_lang.Language import Language

log = Log('TTS')


class TTS:
    def __init__(self, lang: Language):
        self.lang = lang

    def get_cache_file_path(self, text: str) -> str:
        hash = Hash.md5(text)
        dir_temp = os.path.join(
            tempfile.gettempdir(), f'tts.{self.lang.iso2}'
        )
        os.makedirs(dir_temp, exist_ok=True)
        return os.path.join(dir_temp, f'{hash}.mp3')

    def write_nocache(self, text: str):
        cache_file_path = self.get_cache_file_path(text)
        tts = gTTS(text=text, lang=self.lang.iso2)
        tts.save(cache_file_path)
        log.debug(f'"{text}" -> "{cache_file_path}"')
        return cache_file_path

    def write(self, text: str):
        cache_file_path = self.get_cache_file_path(text)
        if not os.path.exists(cache_file_path):
            self.write_nocache(text)
        return cache_file_path
