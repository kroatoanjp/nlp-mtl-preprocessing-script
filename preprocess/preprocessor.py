#!/usr/bin/env python

import argparse
import json
import os
from typing import Optional

from dotenv import load_dotenv
import inquirer

from preprocess.nlp_mtl_preprocess import NLP_MTL_Preprocess
from preprocess.mtl_preprocess import MTL_Preprocess
from preprocess.tokenizer.fugashi_tokenizer import FugashiTokenizer
from preprocess.tokenizer.sudachi_tokenizer import SudachiTokenizer
from preprocess.tokenizer.spacy_tokenizer import SpacyTokenizer
from preprocess.tagger import Tagger
from preprocess.tools.mecab_dict_generator import MecabDictGenerator
from preprocess.tools.sudachi_dict_generator import SudachiDictGenerator

class PreprocessorEnvConfig:
    ENV_PREFIX = "PREPROCESSOR"
    def __init__(
        self, 
        tokenizer:Optional[str]=None,
        replacement_table_json:Optional[str]=None,
        tag_potential_proper_nouns:Optional[bool]=False,
        use_user_dict:Optional[bool]=False,
        user_dic_path:Optional[str]=None,
        use_single_kanji_filter:Optional[bool]=False,
    ):
        self.tokenizer = tokenizer
        self.replacement_table_json = replacement_table_json
        self.tag_potential_proper_nouns = tag_potential_proper_nouns
        self.use_user_dict = use_user_dict
        self.user_dic_path = user_dic_path
        self.use_single_kanji_filter = use_single_kanji_filter

    def write_env(self):
        env_rows = [
            f"{self.ENV_PREFIX}_TOKENIZER={self.tokenizer}",
            f"{self.ENV_PREFIX}_REPLACEMENT_TABLE_JSON={self.replacement_table_json}",
            f"{self.ENV_PREFIX}_TAG_POTENTIAL_PROPER_NOUNS={self.tag_potential_proper_nouns}",
            f"{self.ENV_PREFIX}_USE_USER_DICT={self.use_user_dict}",
            f"{self.ENV_PREFIX}_USER_DICT_PATH={self.user_dic_path}",
            f"{self.ENV_PREFIX}_USE_SINGLE_KANJI_FILTER={self.use_single_kanji_filter}",
        ]
        with open(".env", "w") as env_file:
            env_file.write("\n".join(env_rows))
        print("Preprocessor config written to: .env")

    @classmethod
    def read_env(cls) -> "PreprocessorEnvConfig":
        # convert str to bool
        tag_potential_proper_nouns = os.getenv(f"{cls.ENV_PREFIX}_TAG_POTENTIAL_PROPER_NOUNS")=='True'
        use_user_dict = os.getenv(f"{cls.ENV_PREFIX}_USE_USER_DICT")=='True'
        use_user_dict = os.getenv(f"{cls.ENV_PREFIX}_USE_SINGLE_KANJI_FILTER")=='True'
        return PreprocessorEnvConfig(
            tokenizer=os.getenv(f"{cls.ENV_PREFIX}_TOKENIZER"),
            replacement_table_json=os.getenv(f"{cls.ENV_PREFIX}_REPLACEMENT_TABLE_JSON"),
            tag_potential_proper_nouns=tag_potential_proper_nouns,
            use_user_dict=use_user_dict, 
            user_dic_path=os.getenv(f"{cls.ENV_PREFIX}_USER_DICT_PATH"),
            use_single_kanji_filter=use_user_dict,
        )


def out_filename_generator(in_filename):
    p, e = os.path.splitext(in_filename)
    return f'{p}-rep{e}'

def load_replacement_table(filename):
    with open(filename, "r") as replacement_json_file:
        replacement_table = json.loads(replacement_json_file.read())
    return replacement_table

def parse_args():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(required=True, dest="preprocessor_type")
    basic_parser = subparsers.add_parser('basic', help="Original MTL Preprocessor")
    basic_parser.add_argument("input_file")
    basic_parser.add_argument("replacement_json")
    basic_parser.add_argument('-v', '--verbose', action="store_true")
    basic_parser.add_argument('--disable_single_kanji_filter', action="store_true")
    nlp_parser = subparsers.add_parser('nlp', help="NLP MTL Preprocessor")
    nlp_subparsers = nlp_parser.add_subparsers(required=True, dest="nlp_processor_command")
    nlp_run_parser = nlp_subparsers.add_parser('run', help="Run NLP Preprocessor")
    nlp_run_parser.add_argument("input_file")
    nlp_run_parser.add_argument('-v', '--verbose', action="store_true")
    nlp_setup_parser = nlp_subparsers.add_parser('setup', help="Setup NLP Preprocessor")
    tools_subparsers = subparsers.add_parser('tools', help="Additional preprocessor tools")
    tools_parser = tools_subparsers.add_subparsers(required=True, dest="tools_command")
    tools_build_mecab_dict_parser = tools_parser.add_parser(
        'build_mecab_dict', 
        help="Build a MeCab user dictionary"
    )
    tools_build_mecab_dict_parser.add_argument("dictionary_type", choices=['unidic', "ipadic"])
    tools_build_mecab_dict_parser.add_argument("replacement_json")
    tools_build_mecab_dict_parser.add_argument("dictionary_source_directory")
    tools_build_sudachi_dict_parser = tools_parser.add_parser(
        'build_sudachi_dict',
         help="Build a Sudachi user dictionary"
    )
    tools_build_sudachi_dict_parser.add_argument("replacement_json")
    tools_build_sudachi_dict_parser.add_argument("dictionary_source_file")
    return parser.parse_args()

def run_basic_mtl_preprocessor(args):
    use_single_kanji_filter = not args.disable_single_kanji_filter
    with open(args.input_file, "r") as input_file:
        text = input_file.read()
    replacement_table = load_replacement_table(args.replacement_json)
    preprocess = MTL_Preprocess(
        text=text, 
        replacement=replacement_table,
        verbose=args.verbose,
        single_kanji_filter=use_single_kanji_filter
    )
    preprocessed_text = preprocess.replace()    
    out_filename = out_filename_generator(args.input_file)
    with open(out_filename, 'w', encoding='utf-8') as outfile:
        outfile.write(preprocessed_text)
    print(f'Output written to: {out_filename}')

def run_nlp_mtl_preprocessor(args):
    with open(args.input_file, "r") as input_file:
        text = input_file.read()
    env_config = PreprocessorEnvConfig.read_env()
    if env_config.tokenizer == "fugashi":
        if env_config.use_user_dict:
            tokenizer = FugashiTokenizer(user_dic_path=env_config.user_dic_path)
        else:
            tokenizer = FugashiTokenizer()
    elif env_config.tokenizer == "sudachi":
        if env_config.use_user_dict:
            tokenizer = SudachiTokenizer(user_dic_path=env_config.user_dic_path)
        else:
            tokenizer = SudachiTokenizer()
    elif env_config.tokenizer == "spacy":
        if env_config.use_user_dict:
            tokenizer = SpacyTokenizer(user_dic_path=env_config.user_dic_path)
        else:
            tokenizer = SpacyTokenizer()
    else:
        raise ValueError(f"Received unexpected tokenizer: {env_config.tokenizer}")
    replacement_table = load_replacement_table(env_config.replacement_table_json)
    proper_noun_list = NLP_MTL_Preprocess.generate_name_list_from_replacement_table(replacement_table)
    tagger = Tagger(
        tokenizer=tokenizer,
        tag_potential_proper_nouns=env_config.tag_potential_proper_nouns,
        proper_noun_list=proper_noun_list,
    )
    preprocess = NLP_MTL_Preprocess(
        text=text, 
        tagger=tagger, 
        replacement_table=replacement_table,
        verbose=args.verbose,
        single_kanji_filter=env_config.use_single_kanji_filter
    )
    preprocessed_text = preprocess.replace()    
    out_filename = out_filename_generator(args.input_file)
    with open(out_filename, 'w', encoding='utf-8') as outfile:
        outfile.write(preprocessed_text)
    print(f'Output written to: {out_filename}')

def setup_nlp_mtl_preprocessor():
    initial_questions = [
        inquirer.List(
            "tokenizer",
            message="Select tokenizer",
            choices=['spacy','sudachi','fugashi']
        ),
        inquirer.Path(
            'replacement_table_json',
            message="Path to replacement table json",
            path_type=inquirer.Path.FILE,
        ),
        inquirer.List(
            'tag_potential_proper_nouns',
            message="Subdivide tagged words that are likely to contain names",
            choices=['Yes', "No"]
        ),
        inquirer.List(
            'use_single_kanji_filter',
            message="Use single kanji filter",
            choices=['Yes', "No"]
        ),
        inquirer.List(
            'use_user_dict',
            message="Use user dictionary",
            choices=['Yes', "No"]
        ),
    ]
    initial_answers = inquirer.prompt(initial_questions)
    use_user_dict = True if initial_answers['use_user_dict'] == "Yes" else False
    use_single_kanji_filter = True if initial_answers['use_single_kanji_filter'] == "Yes" else False
    tag_potential_proper_nouns = True if initial_answers['tag_potential_proper_nouns'] == "Yes" else False
    additional_questions = []
    if use_user_dict:
        additional_questions.append(
            inquirer.Path(
                'user_dict_path',
                message="Path to user dictionary",
                path_type=inquirer.Path.FILE,
            )
        )
    if len(additional_questions) > 0:
        additional_answers = inquirer.prompt(additional_questions)
    else:
        additional_answers = {}
    env_config = PreprocessorEnvConfig(
        tokenizer=initial_answers['tokenizer'],
        replacement_table_json=initial_answers['replacement_table_json'],
        tag_potential_proper_nouns=tag_potential_proper_nouns,
        use_user_dict=use_user_dict,
        user_dic_path=additional_answers.get('user_dict_path'),
        use_single_kanji_filter=use_single_kanji_filter,
    )
    env_config.write_env()

def build_mecab_dict(args):
    replacement_table = load_replacement_table(args.replacement_json)
    dict_generator = MecabDictGenerator(
        dictionary_type=args.dictionary_type,
        dictionary_source_directory=args.dictionary_source_directory,
        replacement_table=replacement_table
    )
    dict_generator.generate()

def build_sudachi_dict(args):
    replacement_table = load_replacement_table(args.replacement_json)
    dict_generator = SudachiDictGenerator(
        dictionary_source_file=args.dictionary_source_file,
        replacement_table=replacement_table
    )
    dict_generator.generate()

def main():
    args = parse_args()
    if args.preprocessor_type == "basic":
        run_basic_mtl_preprocessor(args)
    elif args.preprocessor_type == "nlp":
        if args.nlp_processor_command == "setup":
            setup_nlp_mtl_preprocessor()
        elif args.nlp_processor_command == "run":
            run_nlp_mtl_preprocessor(args)
        else:
            raise Exception(
                f"Received unexpected nlp_processor_command: {args.nlp_processor_command}"
            )
    elif args.preprocessor_type == "tools":
        if args.tools_command == "build_mecab_dict":
            build_mecab_dict(args)
        elif args.tools_command == "build_sudachi_dict":
            build_sudachi_dict(args)
        else:
            raise Exception(f"Received unexpected tools_command: {args.tools_command}")
    else:
        raise Exception(f"Received unexpected preprocessor_type: {args.preprocessor_type}")

   
    
if __name__ == "__main__":
    load_dotenv()
    main()