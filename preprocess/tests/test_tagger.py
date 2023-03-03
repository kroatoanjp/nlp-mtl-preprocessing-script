import unittest
from unittest.mock import MagicMock

from preprocess.tokenizer.fugashi_tokenizer import FugashiTokenizer
from preprocess.tagger import Tagger
from preprocess.sentence import Word

class TestTagger(unittest.TestCase):
    def test_tag_with_word_list_empty_word_list(self):
        sample_text = "アルデバラン"
        sample_word_list = []
        tokenizer = FugashiTokenizer() # TODO: Mock out tokenizer
        tagger = Tagger(tokenizer=tokenizer)
        expected = [Word(sample_text, "固有名詞")]
        actual = tagger._tag_with_word_list(sample_text, sample_word_list)
        self.assertEqual(actual, expected)

    def test_tag_with_word_list_empty_string(self):
        sample_text = ""
        sample_word_list = [Word('猫', "名詞")]
        tokenizer = FugashiTokenizer()
        tagger = Tagger(tokenizer=tokenizer)
        expected = []
        actual = tagger._tag_with_word_list(sample_text, sample_word_list)
        self.assertEqual(actual, expected)

    def test_tag_with_word_list_single_word_text_single_word_word_list(self):
        sample_text = "猫"
        sample_word_list = [Word('猫', "名詞")]
        tokenizer = FugashiTokenizer()
        tagger = Tagger(tokenizer=tokenizer)
        expected = [Word('猫', "名詞")]
        actual = tagger._tag_with_word_list(sample_text, sample_word_list)
        self.assertEqual(actual, expected)

    def test_tag_with_word_list_multi_word_text_single_word_word_list(self):
        sample_text = "猫猫"
        sample_word_list = [Word('猫', "名詞")]
        tokenizer = FugashiTokenizer()
        tagger = Tagger(tokenizer=tokenizer)
        expected = [Word('猫', "名詞"),Word('猫', "名詞")]
        actual = tagger._tag_with_word_list(sample_text, sample_word_list)
        self.assertEqual(actual, expected)

    def test_tag_with_word_list_single_word_text_multi_word_word_list(self):
        sample_text = "猫"
        sample_word_list = [Word('猫', "名詞"), Word('犬', "名詞")]
        tokenizer = FugashiTokenizer()
        tagger = Tagger(tokenizer=tokenizer)
        expected = [Word('猫', "名詞")]
        actual = tagger._tag_with_word_list(sample_text, sample_word_list)
        self.assertEqual(actual, expected)

    def test_tag_with_word_list_multi_word_text_single_word_word_list(self):
        sample_text = "犬猫"
        sample_word_list = [Word('猫', "名詞"), Word('犬', "名詞")]
        tokenizer = FugashiTokenizer()
        tagger = Tagger(tokenizer=tokenizer)
        expected = [Word('犬', "名詞"),Word('猫', "名詞")]
        actual = tagger._tag_with_word_list(sample_text, sample_word_list)
        self.assertEqual(actual, expected)

    def test_tag_with_word_list_single_matching_katakana_noun(self):
        sample_text = "アルデバラン"
        known_name = "アルデバラン"
        sample_word_list = [Word(known_name, "固有名詞")]
        tokenizer = FugashiTokenizer()
        tagger = Tagger(tokenizer=tokenizer)
        expected = [Word(known_name, "固有名詞")]
        actual = tagger._tag_with_word_list(sample_text, sample_word_list)
        self.assertEqual(actual, expected)

    def test_tag_with_word_list_single_matching_katakana_noun_with_preceding_katakana(self):
        unrelated_katakana_word = "リアル"
        known_name = "アルデバラン"
        sample_text = unrelated_katakana_word+known_name
        sample_word_list = [Word(known_name, "固有名詞")]
        tokenizer = FugashiTokenizer()
        tagger = Tagger(tokenizer=tokenizer)
        expected = [Word(unrelated_katakana_word, "名詞"), Word(known_name, "固有名詞")]
        actual = tagger._tag_with_word_list(sample_text, sample_word_list)
        self.assertEqual(actual, expected)

    def test_tag_with_word_list_single_matching_katakana_noun_with_tailing_katakana(self):
        unrelated_katakana_word = "リアル"
        known_name = "アルデバラン"
        sample_text = known_name + unrelated_katakana_word
        sample_word_list = [Word(known_name, "固有名詞")]
        tokenizer = FugashiTokenizer()
        tagger = Tagger(tokenizer=tokenizer)
        expected = [Word(known_name, "固有名詞"), Word(unrelated_katakana_word, "名詞")]
        actual = tagger._tag_with_word_list(sample_text, sample_word_list)
        self.assertEqual(actual, expected)    

    def test_tag_with_word_list_single_repeating_katakana_noun(self):
        known_name = "チシャ"
        sample_text = known_name * 3
        sample_word_list = [Word(known_name, "固有名詞")]
        tokenizer = FugashiTokenizer()
        tagger = Tagger(tokenizer=tokenizer)
        expected = [
            Word(known_name, "固有名詞"), 
            Word(known_name, "固有名詞"), 
            Word(known_name, "固有名詞")
        ]
        actual = tagger._tag_with_word_list(sample_text, sample_word_list)
        self.assertEqual(actual, expected)

    def test_tag_with_word_list_longest_matching_word_first(self):
        sample_text = "アルデバラン"
        sample_word_list = [
            Word("アル", "固有名詞"),
            Word("アルデバラン", "固有名詞"),
        ]
        tokenizer = FugashiTokenizer()
        tagger = Tagger(tokenizer=tokenizer)
        expected = [Word("アルデバラン", "固有名詞")]
        actual = tagger._tag_with_word_list(sample_text, sample_word_list)
        self.assertEqual(actual, expected)
