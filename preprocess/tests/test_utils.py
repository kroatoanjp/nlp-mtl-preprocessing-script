import unittest

from preprocess.utils import is_katakana, sort_list_by_string_length, \
                             is_punctuation

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

    def test_sort_list_by_string_length_empty_list(self):
        sample_list = []
        actual = []
        expected = sort_list_by_string_length(sample_list)
        self.assertEqual(actual, expected)

    def test_sort_list_by_string_length_sorted_list_noop(self):
        sample_list = ["a", "bb", "ccc"]
        actual = ["a", "bb", "ccc"]
        expected = sort_list_by_string_length(sample_list)
        self.assertEqual(actual, expected)

    def test_sort_list_by_string_length_successful(self):
        sample_list = ["ccc", "bb", "a"]
        actual = ["a", "bb", "ccc"]
        expected = sort_list_by_string_length(sample_list)
        self.assertEqual(actual, expected)

    def test_sort_list_by_string_length_reverse_empty_list(self):
        sample_list = []
        actual = []
        expected = sort_list_by_string_length(sample_list, reverse=True)
        self.assertEqual(actual, expected)

    def test_sort_list_by_string_length_reverse_sorted_list_noop(self):
        sample_list = ["ccc", "bb", "a"]
        actual = ["ccc", "bb", "a"]
        expected = sort_list_by_string_length(sample_list, reverse=True)
        self.assertEqual(actual, expected)

    def test_sort_list_by_string_length_reverse_successful(self):
        sample_list = ["a", "bb", "ccc"]
        actual = ["ccc", "bb", "a"]
        expected = sort_list_by_string_length(sample_list, reverse=True)
        self.assertEqual(actual, expected)

    def test_is_punctuation_true_punctation_only_string(self):
        sample_str = "※※$$$※$$$※$$$※$$$※$$$※$$$※$$$※$$$※$$$※$$$※$$$"
        actual = is_punctuation(sample_str)
        self.assertTrue(actual)

    def test_is_punctuation_false_punctation_partial_string(self):
        sample_str = "※※a$$$"
        actual = is_punctuation(sample_str)
        self.assertFalse(actual)

    def test_is_punctuation_false_no_punctation_string(self):
        sample_str = "abc"
        actual = is_punctuation(sample_str)
        self.assertFalse(actual)

if __name__ == "__main__":
    unittest.main()