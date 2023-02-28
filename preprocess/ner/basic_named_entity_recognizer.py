# Rudimentary named entity recognizer that uses word lists and
# character checking to identify likely words. Might be replaced
# with a dedicated NER library in the future.

from preprocess.ner.named_entity_recognizer import NamedEntityRecognizer
from preprocess.utils import is_katakana

KATAKANA_WORDS_FILE = "data/katakana_words.txt"

class BasicNamedEntityRecognizer(NamedEntityRecognizer):
    def __init__(self):
        self._katakana_words = set()
        with open(KATAKANA_WORDS_FILE) as infile:
            for row in infile:
                word = row.strip()
                if not is_katakana(word):
                    raise ValueError(f"Received unexpected non-katakana word: {word}")
                self._katakana_words.add(row.strip())

    def is_name(self, value:str) -> bool:
        # For the time being treat all kanji names as being not being
        # names.
        if not is_katakana(value):
            return False
        return not self.is_known_katakana_word(value)

    def is_known_katakana_word(self, value:str) -> bool:
        return value in self._katakana_words