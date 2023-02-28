import unittest

from preprocess.utils import is_katakana

class UtilsTestCase(unittest.TestCase):
    def test_is_katakana_true_for_katakana_only_string(self):
        sample_str = "スバル"
        actual = is_katakana(sample_str)
        self.assertTrue(actual)

    def test_is_katakana_true_for_hyphenated_katakana_string(self):
        sample_str = "スバルー"
        actual = is_katakana(sample_str)
        self.assertTrue(actual)

    def test_is_katakana_true_for_dot_separated_katakana_string(self):
        sample_str = "ナツキ・スバル"
        actual = is_katakana(sample_str)
        self.assertTrue(actual)

    def test_is_katakana_false_for_partial_katakana_string(self):
        sample_str = "スバルの"
        actual = is_katakana(sample_str)
        self.assertFalse(actual)

    def test_is_katakana_false_for_no_katakana_string(self):
        sample_str = "すばる"
        actual = is_katakana(sample_str)
        self.assertFalse(actual)

if __name__ == "__main__":
    unittest.main()