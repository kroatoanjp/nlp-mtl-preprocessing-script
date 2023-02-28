import unittest

from preprocess.ner.basic_named_entity_recognizer import BasicNamedEntityRecognizer

class TestBasicNamedEntityRecognizer(unittest.TestCase):    
    def test_is_name_false_for_kanji_word(self):
        sample_text = "犬"
        name_recognizer = BasicNamedEntityRecognizer()
        actual = name_recognizer.is_name(sample_text)
        self.assertFalse(actual)

    def test_is_name_true_for_unknown_katakana_word(self):
        sample_text = "ルイガ"
        name_recognizer = BasicNamedEntityRecognizer()
        actual = name_recognizer.is_name(sample_text)
        self.assertTrue(actual)

    def test_is_name_false_for_known_katakana_word(self):
        sample_text = "イライラ"
        name_recognizer = BasicNamedEntityRecognizer()
        actual = name_recognizer.is_name(sample_text)
        self.assertFalse(actual)

if __name__ == "__main__":
    unittest.main()