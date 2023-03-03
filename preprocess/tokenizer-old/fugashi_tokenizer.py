from typing import Optional, Iterable, List

import fugashi
from preprocess.ner.basic_named_entity_recognizer import BasicNamedEntityRecognizer
from preprocess.sentence import Sentence, Word
from preprocess.tokenizer.whitespace_ignoring_tokenizer import WhitespaceIgnoringTokenizer
from preprocess.tokenizer.part_of_speech import PartOfSpeech

# Fugashi (python wrapper of MeCab)
# Repo: https://github.com/polm/fugashi
class FugashiTokenizer(WhitespaceIgnoringTokenizer):
    def __init__(
        self, 
        # Path to MeCab user dic
        user_dic_path:Optional[str] = None, 
        # If True, will subdivide words that contain proper nouns, as
        # listed in proper_noun_list  
        tag_potential_proper_nouns:Optional[bool] = True, 
        proper_noun_list:Optional[Iterable[str]] = None
    ):
        self._name_recognizer = BasicNamedEntityRecognizer()
        if user_dic_path:
            self._tagger = fugashi.Tagger(f"-u {user_dic_path}")
        else:
            self._tagger = fugashi.Tagger()
        self._tag_potential_proper_nouns = tag_potential_proper_nouns
        self._proper_noun_list = []
        if not proper_noun_list:
            proper_noun_list = []
        # Sort list of additional taggable proper nouns from longest 
        # to shortest to avoid accidental replacements of a common
        # substring
        len_tagged_proper_noun_list = {(len(word), word) for word in proper_noun_list}
        for word_len, word in sorted(len_tagged_proper_noun_list, reverse=True):
            self._proper_noun_list.append(
                Word(word, PartOfSpeech.PROPER_NOUN)
            )

    def tag(self, text:str) -> Sentence:
        NEWLINE_WORD = Word(text='\n', part_of_speech=PartOfSpeech.WHITESPACE)
        combined_word_list = []
        for line in text.split("\n"):
            tagged_sentence = self.tag_line(line)
            combined_word_list += tagged_sentence.words
            combined_word_list.append(NEWLINE_WORD)
        combined_word_list.pop() # Remove final added NEWLINE_WORD
        return Sentence(combined_word_list)

    def tag_line(self, text:str) -> Sentence:
        preprocessed_text = self._preprocess_text(text)
        word_list = self._create_tagged_word_list(preprocessed_text)
        if self._tag_potential_proper_nouns:
            name_checked_word_list = []
            for word in word_list:
                if self._name_recognizer.is_name(word.text):
                    tagged_subwords = self._tag_with_word_list(
                        text=word.text, 
                        word_list=self._proper_noun_list, 
                        word_list_presorted=True
                    )
                    for subword in tagged_subwords:
                        name_checked_word_list.append(subword)
                else:
                    name_checked_word_list.append(word)
            word_list = name_checked_word_list
        tagged_sentence = Sentence(word_list)
        validated_tagged_sentence = self._validate_tagging(text, tagged_sentence)
        return validated_tagged_sentence


    # Divide a string into words with preference given to a list of
    # provided words. Any unrecognized should then be retagged with
    # Fugashi.
    def _tag_with_word_list(
            self, 
            text:str, 
            word_list:List[Word],
            word_list_presorted=False
        ) -> List[Word]:
        if len(text) == 0:
            return []
        # Known words should be checked from longest to shortest to 
        # avoid unintentionally matching shorter words
        if word_list_presorted:
            sorted_word_list = word_list
        else:
            sorted_word_list = []
            len_tagged_word_list = {(len(word), word) for word in word_list}
            for word_len, word in sorted(len_tagged_word_list, reverse=True):
                sorted_word_list.append(word)
        tagged_words = [] 
        matching_word_found = False
        for i, word in enumerate(sorted_word_list):
            if word.text == text:
                tagged_words.append(word)
                matching_word_found = True
                break
            elif word.text in text:
                unchecked_words = sorted_word_list[i+1:]
                non_matching_text_parts = text.split(word.text)
                for part in non_matching_text_parts:
                    subword_list = self._tag_with_word_list(part, unchecked_words, True)
                    for subword in subword_list:
                        tagged_words.append(subword)
                    tagged_words.append(word)
                tagged_words.pop() # Last appended word is extra
                matching_word_found = True
                break
        # Default to Fugashi tagging once all the words in the provided
        # word list have been tried
        if not matching_word_found:
            return self._create_tagged_word_list(text)
        else:
            return tagged_words

    def _create_tagged_word_list(self, text:str) -> List[Word]:
        word_list = []
        tagged_words = self._tagger(text)
        for word in tagged_words:
            word_text = word.surface
            part_of_speech = word.feature[0]
            # Prefer the more specific proper noun pos tag when available,
            # as it enables more accurate single kanji replacement
            if word.feature[0] == PartOfSpeech.NOUN and \
                word.feature[1] == PartOfSpeech.PROPER_NOUN:
                part_of_speech = word.feature[1]
            word_list.append(Word(word_text, part_of_speech))
        return word_list