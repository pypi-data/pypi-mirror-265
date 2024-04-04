import os
import tempfile
from functools import cache, cached_property

from deep_translator import GoogleTranslator
from utils_base import JSONFile, Log

from utils_lang.Language import Language

log = Log('Translator')


class Translator:
    def __init__(self, source_lang: Language, target_lang: Language):
        self.source_lang = source_lang
        self.target_lang = target_lang
        self.translator = GoogleTranslator(
            source=self.source_lang.iso2, target=target_lang.iso2
        )
        self.cache_idx = self.load_cache()

    @cached_property
    def cache_file_path(self) -> str:
        return os.path.join(
            tempfile.gettempdir(),
            f"Translate.{self.source_lang.iso2}-{self.target_lang.iso2}.json",
        )

    @property
    def cache_file(self) -> JSONFile:
        return JSONFile(self.cache_file_path)

    def load_cache(self) -> dict:
        return self.cache_file.read() if self.cache_file.exists else {}

    def save_cache(self):
        self.cache_file.write(self.cache_idx)

    def translate_nocache(self, text: str) -> str:
        translated_text = self.translator.translate(text)
        log.debug(f'"{text}" -> "{translated_text}"')
        return translated_text

    @cache
    def translate(self, text: str) -> str:
        if text in self.cache_idx:
            return self.cache_idx[text]

        translation = self.translate_nocache(text)
        self.cache_idx[text] = translation
        self.save_cache()

        return translation
