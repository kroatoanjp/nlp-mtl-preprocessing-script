import unittest

from preprocess.sentence import Sentence, Word

class SentenceTestCase(unittest.TestCase):

    def test_replace_word_single_occurence(self):
        original_sentence = generate_sentence("本")
        expected = generate_sentence("鞄")
        actual = original_sentence.replace_word(
            Word(text='本', part_of_speech='名詞'),
            "鞄"
        )
        self.assertEqual(actual, expected)

    def test_replace_word_multi_occurence(self):
        original_sentence = generate_sentence("本", "本")
        expected = generate_sentence("鞄", "鞄")
        actual = original_sentence.replace_word(
            Word(text='本', part_of_speech='名詞'),
            "鞄"
        )
        self.assertEqual(actual, expected)

    def test_replace_word_no_occurence(self):
        original_sentence = generate_sentence("本")
        expected = original_sentence
        actual = original_sentence.replace_word(
            Word(text='鉛筆', part_of_speech='名詞'),
            "鞄"
        )
        self.assertEqual(actual, expected)

    def test_replace_multi_word_sequence_single_word_single_occurence(self):
        original_sentence = generate_sentence("本")
        expected = generate_sentence("鞄")
        actual = original_sentence.replace_multi_word_sequence(
            "本",
            Word(text='鞄', part_of_speech='名詞'),
        )
        self.assertEqual(actual, expected)

    def test_replace_multi_word_sequence_single_word_multi_occurence(self):
        original_sentence = generate_sentence("本", "本")
        expected = generate_sentence("鞄", "鞄")
        actual = original_sentence.replace_multi_word_sequence(
            "本",
            Word(text='鞄', part_of_speech='名詞'),
        )
        self.assertEqual(actual, expected)

    def test_replace_multi_word_sequence_single_word_no_occurence(self):
        original_sentence = generate_sentence("本")
        expected = original_sentence
        actual = original_sentence.replace_multi_word_sequence(
            "鉛筆",
            Word(text='鞄', part_of_speech='名詞'),
        )
        self.assertEqual(actual, expected)

    def test_replace_multi_word_sequence_multi_word_single_occurence(self):
        original_sentence = generate_sentence("本")
        expected = Sentence([
            Word(text='その靴', part_of_speech='NA'),
            Word(text='は', part_of_speech='助詞'), 
            Word(text='私', part_of_speech='代名詞'), 
            Word(text='の', part_of_speech='助詞'),
            Word(text='です', part_of_speech='助動詞'),
            Word(text='。', part_of_speech='補助記号')
        ])
        actual = original_sentence.replace_multi_word_sequence(
            "この本",
            Word(text='その靴', part_of_speech='NA'),
        )
        self.assertEqual(actual, expected)

    def test_replace_multi_word_sequence_multi_word_multi_occurence(self):
        original_sentence = Sentence([
            Word(text='この', part_of_speech='連体詞'),
            Word(text='赤い', part_of_speech='形容詞'),
            Word(text='本', part_of_speech='名詞'), 
            Word(text='は', part_of_speech='助詞'), 
            Word(text='私', part_of_speech='代名詞'), 
            Word(text='の', part_of_speech='助詞'),
            Word(text='赤い', part_of_speech='形容詞'),
            Word(text='本', part_of_speech='名詞'), 
            Word(text='です', part_of_speech='助動詞'),
            Word(text='。', part_of_speech='補助記号')
        ])
        expected = Sentence([
            Word(text='この', part_of_speech='連体詞'),
            Word(text='緑の靴', part_of_speech='NA'),
            Word(text='は', part_of_speech='助詞'), 
            Word(text='私', part_of_speech='代名詞'), 
            Word(text='の', part_of_speech='助詞'),
            Word(text='緑の靴', part_of_speech='NA'),
            Word(text='です', part_of_speech='助動詞'),
            Word(text='。', part_of_speech='補助記号')
        ])
        actual = original_sentence.replace_multi_word_sequence(
            "赤い本",
            Word(text='緑の靴', part_of_speech='NA'),
        )
        self.assertEqual(actual, expected)

    def test_replace_multi_word_sequence_multi_word_sequential_multi_occurence(self):
        original_sentence = Sentence([
            Word(text='AA', part_of_speech='NA'),
            Word(text='AA', part_of_speech='NA'),
            Word(text='AA', part_of_speech='NA'),
            Word(text='AA', part_of_speech='NA'),
        ])
        expected = Sentence([
            Word(text='BB', part_of_speech='NA'),
            Word(text='BB', part_of_speech='NA'),
            Word(text='BB', part_of_speech='NA'),
            Word(text='BB', part_of_speech='NA'),
        ])
        actual = original_sentence.replace_multi_word_sequence(
            "AA",
            Word(text='BB', part_of_speech='NA'),
        )
        self.assertEqual(actual, expected)

    def test_replace_multi_word_sequence_multi_word_no_occurence(self):
        original_sentence = generate_sentence("鉛筆", "鉛筆")
        expected = original_sentence
        actual = original_sentence.replace_multi_word_sequence(
            "私の鉛",
            Word(text='私の本', part_of_speech='NA'),
        )
        self.assertEqual(actual, expected)

    def test_replace_multi_word_sequence_replace_whole_sentence(self):
        original_sentence = generate_sentence("本")
        expected = Sentence([Word("猫", "NA")])
        actual = original_sentence.replace_multi_word_sequence(
            "この本は私のです。",
            Word("猫", "NA"),
        )
        self.assertEqual(actual, expected)

    def test_count_single_word_single_occurence(self):
        original_sentence = generate_sentence("本")
        expected = 1
        actual = original_sentence.count("本")
        self.assertEqual(actual, expected)

    def test_count_single_word_multi_occurence(self):
        original_sentence = generate_sentence("本", "本")
        expected = 2
        actual = original_sentence.count("本")
        self.assertEqual(actual, expected)

    def test_count_single_word_no_occurence(self):
        original_sentence = generate_sentence("本")
        expected = 0
        actual = original_sentence.count("鉛筆")
        self.assertEqual(actual, expected)

    def test_count_multi_word_single_occurence(self):
        original_sentence = generate_sentence("本")
        expected = 1
        actual = original_sentence.count("この本")
        self.assertEqual(actual, expected)

    def test_count_multi_word_multi_occurence(self):
        original_sentence = Sentence([
            Word(text='この', part_of_speech='連体詞'),
            Word(text='赤い', part_of_speech='形容詞'),
            Word(text='本', part_of_speech='名詞'), 
            Word(text='は', part_of_speech='助詞'), 
            Word(text='私', part_of_speech='代名詞'), 
            Word(text='の', part_of_speech='助詞'),
            Word(text='赤い', part_of_speech='形容詞'),
            Word(text='本', part_of_speech='名詞'), 
            Word(text='です', part_of_speech='助動詞'),
            Word(text='。', part_of_speech='補助記号')
        ])
        expected = 2
        actual = original_sentence.count("赤い本")
        self.assertEqual(actual, expected)

    def test_count_multi_word_sequential_multi_occurence(self):
        original_sentence = Sentence([
            Word(text='AA', part_of_speech='NA'),
            Word(text='AA', part_of_speech='NA'),
            Word(text='AA', part_of_speech='NA'),
            Word(text='AA', part_of_speech='NA'),
        ])
        expected = 4
        actual = original_sentence.count("AA")
        self.assertEqual(actual, expected)

    def test_count_multi_word_no_occurence(self):
        original_sentence = generate_sentence("鉛筆", "鉛筆")
        expected = 0
        actual = original_sentence.count("私の鉛")
        self.assertEqual(actual, expected)

    def test_count_whole_sentence(self):
        original_sentence = generate_sentence("本")
        expected = 1
        actual = original_sentence.count("この本は私のです。")
        self.assertEqual(actual, expected)

    def test_count_word_single_occurence(self):
        original_sentence = generate_sentence("本")
        expected = 1
        actual = original_sentence.count_word(
            Word(text="本", part_of_speech="名詞")
        )
        self.assertEqual(actual, expected)

    def test_count_word_multi_occurence(self):
        original_sentence = generate_sentence("本", "本")
        expected = 2
        actual = original_sentence.count_word(
            Word(text="本", part_of_speech="名詞")
        )
        self.assertEqual(actual, expected)

    def test_count_word_no_occurence(self):
        original_sentence = generate_sentence("鉛筆")
        expected = 0
        actual = original_sentence.count_word(
            Word(text="本", part_of_speech="名詞")
        )
        self.assertEqual(actual, expected)

    def test_count_word_partial_match_no_occurence(self):
        original_sentence = generate_sentence("鉛筆")
        expected = 0
        actual = original_sentence.count_word(
            Word(text="鉛", part_of_speech="名詞")
        )
        self.assertEqual(actual, expected)

    def test_get_word_index_from_char_index_first_char(self):
        sentence = Sentence([
            Word(text='私', part_of_speech='代名詞'), 
            Word(text='の', part_of_speech='助詞'),
            Word(text='緑の靴', part_of_speech='NA'),
        ])
        expected = 0
        actual = sentence.get_word_index_from_char_index(0)
        self.assertEqual(actual, expected)

    def test_get_word_index_from_char_index_last_char(self):
        sentence = Sentence([
            Word(text='私', part_of_speech='代名詞'), 
            Word(text='の', part_of_speech='助詞'),
            Word(text='緑の靴', part_of_speech='NA'),
        ])
        expected = 2
        actual = sentence.get_word_index_from_char_index(4)
        self.assertEqual(actual, expected)

    def test_get_word_index_from_char_index_mid_word_char(self):
        sentence = Sentence([
            Word(text='私', part_of_speech='代名詞'), 
            Word(text='の', part_of_speech='助詞'),
            Word(text='緑の靴', part_of_speech='NA'),
        ])
        expected = 2
        actual = sentence.get_word_index_from_char_index(3)
        self.assertEqual(actual, expected)

    def test_get_word_index_from_char_index_error_negative_index(self):
        sentence = Sentence([
            Word(text='私', part_of_speech='代名詞'), 
            Word(text='の', part_of_speech='助詞'),
            Word(text='緑の靴', part_of_speech='NA'),
        ])
        with self.assertRaises(IndexError):
            sentence.get_word_index_from_char_index(-1)

    def test_get_word_index_from_char_index_error_out_of_bounds_index(self):
        sentence = Sentence([
            Word(text='私', part_of_speech='代名詞'), 
            Word(text='の', part_of_speech='助詞'),
            Word(text='緑の靴', part_of_speech='NA'),
        ])
        with self.assertRaises(IndexError):
            sentence.get_word_index_from_char_index(5)

def generate_sentence(noun1, noun2=None):
    word_list = [
        Word(text='この', part_of_speech='連体詞'),
        Word(text=noun1, part_of_speech='名詞'), 
        Word(text='は', part_of_speech='助詞'), 
        Word(text='私', part_of_speech='代名詞'), 
        Word(text='の', part_of_speech='助詞')
    ]
    if noun2:
        word_list.append(Word(text=noun2, part_of_speech='名詞'))
    word_list += [
        Word(text='です', part_of_speech='助動詞'),
        Word(text='。', part_of_speech='補助記号')
    ]
    return Sentence(word_list)

if __name__ == '__main__':
    unittest.main()