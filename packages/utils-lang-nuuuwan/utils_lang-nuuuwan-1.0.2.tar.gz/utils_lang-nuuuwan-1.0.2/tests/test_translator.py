import unittest

from utils_lang import Language, Translator


class TestTranslator(unittest.TestCase):
    def test_translate(self):
        for source_lang, target_lang, source_text, target_text in [
            (
                Language.ENGLISH,
                Language.SPANISH,
                "The sea is very clear.",
                'El mar es muy claro.',
            ),
            (
                Language.ENGLISH,
                Language.SINHALA,
                "Colombo is the capital of Sri Lanka.",
                'කොළඹ ශ්‍රී ලංකාවේ අගනුවරයි.',
            ),
            (
                Language.ENGLISH,
                Language.TAMIL,
                "what is the time?",
                'நேரம் என்ன?',
            ),
        ]:
            for source_lang, target_lang, source_text, target_text in [
                (source_lang, target_lang, source_text, target_text),
                (target_lang, source_lang, target_text, source_text),
            ]:
                translator = Translator(source_lang, target_lang)
                for translated_text in [
                    translator.translate(source_text),
                    translator.translate_nocache(source_text),
                ]:
                    self.assertEqual(
                        translated_text,
                        target_text,
                    )


if __name__ == '__main__':
    unittest.main()
