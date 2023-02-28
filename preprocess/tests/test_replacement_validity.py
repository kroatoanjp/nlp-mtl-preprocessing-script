import unittest


from preprocess.nlp_mtl_preprocess import NLP_MTL_Preprocess
from preprocess.tokenizer.fugashi_tokenizer import FugashiTokenizer

class ReplacementValidityTestCase(unittest.TestCase):

    def test_successful_term_replacement(self):
        replacement_table = {
            "basic": {
                "『": "«",
                "』": "»"
            }
        }
        text = "『あいうえお』"
        expected = "«あいうえお»"
        name_list = NLP_MTL_Preprocess.generate_name_list_from_replacement_table(replacement_table)
        tokenizer = FugashiTokenizer(proper_noun_list=name_list)
        preprocess = NLP_MTL_Preprocess(
            text=text, 
            tokenizer=tokenizer,
            replacement_table=replacement_table
        )

        actual = preprocess.replace()
        self.assertEqual(actual, expected)

    def test_successful_name_replacement(self):
        replacement_table = {
            "single-names": {
                "Al": "アル"
            }
        }
        text = "「お前、一人なの？　アルとかクソ野郎とか可愛い執事くんとかは？」"
        expected = "「お前、一人なの？　Alとかクソ野郎とか可愛い執事くんとかは？」"
        name_list = NLP_MTL_Preprocess.generate_name_list_from_replacement_table(replacement_table)
        tokenizer = FugashiTokenizer(proper_noun_list=name_list)
        preprocess = NLP_MTL_Preprocess(
            text=text, 
            tokenizer=tokenizer,
            replacement_table=replacement_table
        )
        actual = preprocess.replace()
        self.assertEqual(actual, expected)    

    def test_skips_partial_match_name_replacement(self):
        replacement_table = {
            "single-names": {
                "Al": "アル"
            }
        }
        text = "「思ったより、幻想的な感じじゃないな……がっかりなリアル感だ」"
        expected = "「思ったより、幻想的な感じじゃないな……がっかりなリアル感だ」"
        name_list = NLP_MTL_Preprocess.generate_name_list_from_replacement_table(replacement_table)
        tokenizer = FugashiTokenizer(proper_noun_list=name_list)
        preprocess = NLP_MTL_Preprocess(
            text=text, 
            tokenizer=tokenizer,
            replacement_table=replacement_table
        )
        actual = preprocess.replace()
        self.assertEqual(actual, expected)

    # Test is redundant but keeping it anyway
    # since the イライラ issue has shown up in arc 7
    def test_skips_partial_match_name_replacement_2(self):
        replacement_table = {
            "single-names": {
                "Lyra": "ライラ",
            }
        }
        text = "「……なに、その顔。あんたのその顔、イライラする」"
        expected = "「……なに、その顔。あんたのその顔、イライラする」"
        name_list = NLP_MTL_Preprocess.generate_name_list_from_replacement_table(replacement_table)
        tokenizer = FugashiTokenizer(proper_noun_list=name_list)
        preprocess = NLP_MTL_Preprocess(
            text=text, 
            tokenizer=tokenizer,
            replacement_table=replacement_table
        )
        actual = preprocess.replace()
        self.assertEqual(actual, expected)


    # This test is a reflection of the behavior of the original 
    # replacement script, in that middle names will not be replaced
    # when they show up by themselves.
    def test_skips_isolated_middle_name_replacement(self):
        replacement_table = {
            "names": {
                "Wilhelm van Astrea": ["ヴィルヘルム", "ヴァン", "アストレア"],
            }
        }
        text = "その曇りなき白い刀身を目の当たりにするのは、剣士の誉れである" + \
            "『ヴァン』の名を頂いたヴィルヘルムですら、生涯でたった三度目のことだった。"
        expected = "その曇りなき白い刀身を目の当たりにするのは、剣士の誉れである" + \
            "『ヴァン』の名を頂いたWilhelmですら、生涯でたった三度目のことだった。"
        name_list = NLP_MTL_Preprocess.generate_name_list_from_replacement_table(replacement_table)
        tokenizer = FugashiTokenizer(proper_noun_list=name_list)
        preprocess = NLP_MTL_Preprocess(
            text=text, 
            tokenizer=tokenizer,
            replacement_table=replacement_table
        )
        actual = preprocess.replace()
        self.assertEqual(actual, expected)

    def test_successful_single_kanji_name_replacement(self):
        replacement_table = {
            "full-names": {
                "Karuizawa Kei": [
                    "軽井沢",
                    "恵"
                ],
            }
        }
        text = "不思議と恵のことを聞いてきた直後の方が"
        expected = "不思議とKeiのことを聞いてきた直後の方が"
        name_list = NLP_MTL_Preprocess.generate_name_list_from_replacement_table(replacement_table)
        tokenizer = FugashiTokenizer(proper_noun_list=name_list)
        preprocess = NLP_MTL_Preprocess(
            text=text, 
            tokenizer=tokenizer,
            replacement_table=replacement_table,
            single_kanji_filter=False
        )
        actual = preprocess.replace()
        self.assertEqual(actual, expected) 

    def test_successful_katakana_phrase_name_replacement(self):
        replacement_table = {
            "single-names": {
                "Arakiya": "アラキア",
            }
        }
        text = "ああ……『血命の儀』と『アラキアパニック』ですわね。"
        expected = "ああ……『血命の儀』と『Arakiyaパニック』ですわね。"
        name_list = NLP_MTL_Preprocess.generate_name_list_from_replacement_table(replacement_table)
        tokenizer = FugashiTokenizer(proper_noun_list=name_list)
        preprocess = NLP_MTL_Preprocess(
            text=text, 
            tokenizer=tokenizer,
            replacement_table=replacement_table
        )
        actual = preprocess.replace()
        self.assertEqual(actual, expected) 

    def test_skips_non_noun_single_kanji_name_replacement(self):
        replacement_table = {
            "full-names": {
                "Karuizawa Kei": [
                    "軽井沢",
                    "恵"
                ],
            }
        }
        text = "私は健康に恵まれている"
        expected = "私は健康に恵まれている"
        name_list = NLP_MTL_Preprocess.generate_name_list_from_replacement_table(replacement_table)
        tokenizer = FugashiTokenizer(proper_noun_list=name_list)
        preprocess = NLP_MTL_Preprocess(
            text=text, 
            tokenizer=tokenizer,
            replacement_table=replacement_table,
        )
        actual = preprocess.replace()
        self.assertEqual(actual, expected)    


if __name__ == '__main__':
    unittest.main()