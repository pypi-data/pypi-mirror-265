import os
import shutil
import unittest

from utils_lang import TTS, Language


class TestTTS(unittest.TestCase):
    def test_write(self):
        for lang, text in [
            (
                Language.ENGLISH,
                "It is a truth universally acknowledged"
                + " that a single man in possession of a good fortune"
                + " must be in want of a wife.",
            ),
            (
                Language.SINHALA,
                "කොග්ගල වූ කලි එක් පැත්තකින් මුහුකින්ද අනික්"
                + " පැත්තෙන් සුන්දර වු නදියකින් ද සීමාවුනු බිම්තීරයකි.",
            ),
            (Language.TAMIL, "இதை எழுதியவர் நுவன்"),
        ]:
            tts = TTS(lang)

            tts.write_nocache(text)
            file_path = tts.write(text)
            self.assertTrue(os.path.exists(file_path))
            shutil.copyfile(
                file_path,
                os.path.join('tests', '_output', f'test_tts.{lang.iso2}.mp3'),
            )


if __name__ == '__main__':
    unittest.main()
