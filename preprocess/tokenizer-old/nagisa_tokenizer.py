from difflib import SequenceMatcher
from typing import Optional

import nagisa

from preprocess.sentence import Sentence, Word
from preprocess.tokenizer.tokenizer import Tokenizer

# Nagisa (neural net jp tokenizer)
# Repo: https://github.com/taishi-i/nagisa
# Docs: https://nagisa.readthedocs.io/en/latest/?badge=latest
#
# Attributes:
#   _skip_tagging_validation: Nagisa will attempt to normalize certain 
#       characters (punctuation, whitespace, etc.) when it tags text. 
#       The tokenizer will attempt to denormalize these words after
#       tagging, so that the final tagged sentence aligns with the 
#       original passed text. Enabling this flag will skip the alignment 
#       process.
#   _replace_nonpunctuation_words: Validation process will by default
#       only make replacements when the characters being altered are 
#       punctuation or whitespace, and will throw an exception if 
#       a non-punctuation discrepency is found between the tagged 
#       sentence and original text. Enabling this flag will permit text
#       replacements regardles of character type.
class NagisaTokenizer(Tokenizer):

    PUNCTUATION_PART_OF_SPEECH = "補助記号"
    WHITESPACE_PART_OF_SPEECH = "空白"
    # Nagisa does not properly flag all punctuation chars
    ALLOWLISTED_PUNCTUATION_CHARS = {"~",} 
    
    def __init__(self, 
            skip_tagging_validation: Optional[bool] = False, 
            replace_nonpunctuation_words: Optional[bool] = False
        ):
        self._tagger = nagisa.Tagger()
        self._skip_tagging_validation = skip_tagging_validation
        self._replace_nonpunctuation_words = replace_nonpunctuation_words

    def tag(self, text:str) -> Sentence:
        NEWLINE_WORD = Word(text='\n', part_of_speech='補助記号')
        combined_word_list = []
        for line in text.split("\n"):
            tagged_sentence = self.tag_line(line)
            combined_word_list += tagged_sentence.words
            combined_word_list.append(NEWLINE_WORD)
        combined_word_list.pop() # Remove final added NEWLINE_WORD
        return Sentence(combined_word_list)

    def tag_line(self, text:str) -> Sentence:
        word_list = []
        tagged_words = self._tagger.tagging(text)
        for i, word_text in enumerate(tagged_words.words):
            part_of_speech = tagged_words.postags[i]
            word_list.append(Word(word_text, part_of_speech))
        tagged_sentence = Sentence(word_list)
        if self._skip_tagging_validation:
            return tagged_sentence
        validated_tagged_sentence = self._validate_tagging(text, tagged_sentence)
        return validated_tagged_sentence

    def _validate_tagging(self, text:str, sentence:Sentence) -> Sentence:
        sentence_str = str(sentence)
        if text == sentence_str:
            return sentence
        seq_match = SequenceMatcher(None, text, sentence_str)
        matching_blocks = seq_match.get_matching_blocks()
        old_word_list = sentence.words
        old_word_list_starting_indices = []
        old_word_list_ending_indices = []
        current_starting_index = 0
        for word in old_word_list:
            old_word_list_starting_indices.append(current_starting_index)
            current_starting_index += len(word.text)
            old_word_list_ending_indices.append(current_starting_index - 1)
        # Validate that each matching block starts on the starting index of
        # one of the words, and ends on the ending index of one of the words
        # as opposed to in the middle a random word. Skip last block as it
        # is a dummy block with values (a=len(text), b=len(sentence), size=0)
        old_word_list_starting_index_set = set(old_word_list_starting_indices)
        old_word_list_ending_index_set = set(old_word_list_ending_indices)
        for block in matching_blocks[:-1]:
            if block.b not in old_word_list_starting_index_set or \
               block.b + block.size - 1 not in old_word_list_ending_index_set:
                raise RuntimeError(
                    "Unexpected discrepancy between original text and tagged " + \
                    "text occurred in the middle of a tagged word."
                )

        new_word_list = []
        current_block_index = 0
        current_word_index = 0
        while current_block_index < len(matching_blocks) - 1 and \
            current_word_index < len(old_word_list):
            current_block = matching_blocks[current_block_index]
            # The range of indices such that any word whose starting index is
            # in this range will be matching between text and sentence_str
            current_matching_range = range(current_block.b, current_block.b + current_block.size)
            next_block = matching_blocks[current_block_index + 1]
            current_word = old_word_list[current_word_index]
            current_word_starting_index = old_word_list_starting_indices[current_word_index]
            if current_word_starting_index in current_matching_range:
                new_word_list.append(current_word)
            else:
                if not self._replace_nonpunctuation_words and \
                    current_word.text not in NagisaTokenizer.ALLOWLISTED_PUNCTUATION_CHARS and \
                    current_word.part_of_speech not in (
                        NagisaTokenizer.PUNCTUATION_PART_OF_SPEECH,
                        NagisaTokenizer.WHITESPACE_PART_OF_SPEECH
                    ):
                    raise RuntimeError(
                        f"Unexpected discrepancy in non-punctuation word: {current_word}"
                    )
                if current_word_starting_index >= current_block.b + current_block.size:
                    # If the current word lies beyond the current matching block,
                    # insert a word containing the expected substring from the 
                    # original text, and then update current block to the next 
                    # matching block.
                    if current_block.a + current_block.size < len(text):
                        # The substring of non-matching from the original text 
                        # will be between the indices:
                        # current_block.a + current_block.size = index of first 
                        #   non-matching character.
                        # next_block.a = index of first matching character of 
                        #   the next block.
                        expected_substring = text[current_block.a+current_block.size:next_block.a]
                        new_word_list.append(Word(expected_substring, current_word.part_of_speech))
                        current_block_index += 1
            current_word_index += 1
        validated_sentence = Sentence(new_word_list)
        if str(validated_sentence) != text:
            raise RuntimeError(
                f"Failed to clean-up all discrepancies between original and tagged text."
            )
        return validated_sentence
