# NLP MTL Preprocessing Script

Integrates a JP tokenizer into @thevoidzero's original [MTL preprocessing script](https://github.com/Atreyagaurav/mtl-related-scripts) to avoid unintentional substitutions.

## Setup

```bash
pip3 install -r requirements.txt
# Using fugashi for tokenization requires installing Unidic
python3 -m unidic download
```

## Usage

### Non-NLP Usage

The `basic` preprocessor is a copy the original preprocessor.

```bash
# Run in plain-text replacement mode
# python3 -m preprocess.preprocessor basic [-h] [-v] [--disable_single_kanji_filter] input_file replacement_json
python3 -m preprocess.preprocessor basic ch100.txt replacement_table/rezero.json
```

### NLP Usage

In order to avoid unintentional replacements as well as increase the accuracy of replacements when it comes to single kanji names, `nlp` mode makes use of a tokenizer to divide sentences into words, and then make replacements along word boundaries. 

Before preprocessing chapters in `nlp` mode, first run `nlp setup`

```bash
python3 -m preprocess.preprocessor nlp setup
# Sample Setup
# [?] Select tokenizer: spacy
# [?] Path to replacement table json: replacement_table/rezero.json
# [?] Subdivide tagged words that are likely to contain names: Yes
# [?] Use single kanji filter: No
# [?] Use user dictionary: Yes
# [?] Path to user dictionary: data/dictionaries/rezero-sudachi.dic
```

#### Setup options:

-   `PREPROCESSOR_TOKENIZER`:  Tokenization is currently supported with `spacy` (recommended for Re:Zero), `sudachi`, and `fugashi` . 
-   `PREPROCESSOR_REPLACEMENT_TABLE_JSON`: Path to the replacement table file. Same as what would be used with the old preprocessor. Use `replacement_table/rezero.json` for Re:Zero.
-   `PREPROCESSOR_TAG_POTENTIAL_PROPER_NOUNS`: If `True`, will split apart katakana words that likely contain names. Does cause some false-positive replacements, but will greatly reduce the false-negative rate for strings that contain katakana names.
-   `PREPROCESSOR_USE_SINGLE_KANJI_FILTER`: If `True`, will skip all replacements for names that only 1 character. A holdover from the old preprocessor that was seemingly used to avoid accidentally replacing parts of random words, but is not longer strictly necessary in the NLP version.
-   `PREPROCESSOR_USE_USER_DICT`: Only set to `True` if you are using a user dictionary (instructions for set-up below). For Re:Zero, set to `True`, as user dictionaries are provided in `data/dictionaries/`.
-   `PREPROCESSOR_USER_DICT_PATH`: Path to the user dictionary. For Re:Zero, use `data/dictionaries/rezero-sudachi.dic`  if tokenizing with `spacy` or `sudachi`, and use `data/dictionaries/rezero-fugashi.dic` if tokenizing with `fugashi`.

#### Running in NLP Mode

Once setup is complete, preprocessing chapters is relatively simple

```bash
# Run in NLP replacement mode
# python3 -m preprocess.preprocessor nlp run [-h] [-v] input_file
python3 -m preprocess.preprocessor nlp run ch100.txt
```

### Custom Dictionary Usage
Although their default tokenization is mostly accurate, Fugashi, Sudachi, etc. struggle with separating unknown katakana sequences. Since these most frequently occur in katakana character names, the accuracy of tokenization can be improved by adding these names to a user dictionary.

#### Sudachi/spaCy

Since spaCy uses Sudachi for its underlying tokenization, the same user dictionary can be used for both.

```bash
# python3 -m preprocess.preprocessor tools build_sudachi_dict [-h] replacement_json dictionary_source_file
python3 -m preprocess.preprocessor tools build_sudachi_dict replacement_table/rezero.json venv/lib/python3.10/site-packages/sudachidict_core/resources/system.dic
```
`tools build_sudachi_dict` takes two arguments:

-   `replacement_json`: Path to a json replacement table
-   `dictionary_source_file`: Path to the  `system.dic` file wherever Sudachi was installed.

Running `tools build_sudachi_dict` will generate a new user dictionary in `data/dictionaries`

#### Fugashi
```bash
# python3 -m preprocess.preprocessor tools build_mecab_dict [-h] {unidic,ipadic} replacement_json dictionary_source_directory
python3 -m preprocess.preprocessor tools build_mecab_dict unidic replacement_table/rezero.json venv/lib/python3.10/site-packages/unidic/dicdir/
```

`tools build_mecab_dict` takes three arguments:

-   `dictionary_type`: Either `unidic` (recommended) or `ipadic`. IPAdic is an older Japanese dictionary that is no longer maintained, but is commonly bundled with MeCab. Unidic is a newer dictionary that is currently being maintained. Fugashi by default uses Unidic.
-   `replacement_json`: Path to a json replacement table
-   `dictionary_source_directory`: Path to a directory where either IPAdic or Unidic has been installed. Can be identified by the presence of `dicrc` file.

Running `tools build_mecab_dict` will generate a new user dictionary in `data/dictionaries`

## Notes

### Katakana name splitting

When `tag_potential_proper_nouns` is `True`, words that are likely to be names are subdivided, allowing for additional replacements beyond the initial tagging. The determination for whether a tagged word contains a name is based off the following:

1. The word must only consist of katakana characters
2. The word must not be an actual katakana word, as sourced from the word lists below
3. The word must contain a katakana name from the replacement table

Given these requirements, the chance of a false-positive replacement in the middle of an actual katakana word is relatively slim. However, there is a fair chance of false-positive replacement for names that are not contained in the replacement table.

**Example:**

> ロイ・アルファルド => ロイ・Al ファルド

The simplest way to remediate this would be to include more names in the replacement table. Additionally, a fourth condition could be added before splitting a word, namely that once the word is split, the remaining text must also consist of other katakana words or known names.

**Katakana Word Lists:**

* Leeds Corpus - http://corpus.leeds.ac.uk/frqc/internet-jp-forms.num
* Katakana Core 10k - https://ankiweb.net/shared/info/1723626457

#### Tokenizer Comparison
Diffs for the outputs of the different preprocess modes when run on a large subset of Re:Zero WN chapters can be found [here](https://github.com/kroatoanjp/nlp-mtl-preprocessing-script/tree/master/benchmarks/rezero).
