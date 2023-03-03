# Test validity of NLP-based MTL replacement by comparing output with
# that of the original MTL script for the first 620 chapters of the
# Re:Zero WN

import difflib
import glob
import json
import time
import datetime
import os
from typing import List

from preprocess.mtl_preprocess import MTL_Preprocess
from preprocess.nlp_mtl_preprocess import NLP_MTL_Preprocess
from preprocess.tokenizer.fugashi_tokenizer import FugashiTokenizer
from preprocess.tokenizer.sudachi_tokenizer import SudachiTokenizer
from preprocess.tokenizer.spacy_tokenizer import SpacyTokenizer
from preprocess.tagger import Tagger

DOCS_FOLDER = "preprocess/tests/docs/rezero"
REPLACEMENT_TABLE_FILENAME = "replacement_table/rezero.json"
FUGASHI_USER_DIC_PATH = "data/dictionaries/rezero-fugashi.dic"
SUDACHI_USER_DIC_PATH = "data/dictionaries/rezero-sudachi.dic"
RESULTS_FOLDER = "validity-test-results"

def run_validity_test(
        fileset: List[str],
        old_preprocess_name:str,
        old_preprocess_factory,
        new_preprocess_name:str,
        new_preprocess_factory,
    ):
    diff_list = []
    DIFF_LIST_DELIMITER = '\n===================\n'
    matching_file_count = 0
    differing_file_count = 0
    start_time = time.time()
    for filename in fileset:
        print("Starting " + filename)
        with open(filename) as docfile:
            chapter_text = docfile.read()
            old_preprocess = old_preprocess_factory(chapter_text)
            old_preprocess.replace()
            new_preprocess = new_preprocess_factory(chapter_text)
            new_preprocess.replace()
            if old_preprocess.text == new_preprocess.text:
                matching_file_count += 1
                print(f"{new_preprocess_name} aligns with {old_preprocess_name} for chapter file: {filename}")
            else:
                differing_file_count += 1
                print(f"{new_preprocess_name} differs from {old_preprocess_name} for chapter file: {filename}")
                diff = difflib.unified_diff(
                    old_preprocess.text.split("\n"), 
                    new_preprocess.text.split("\n"), 
                    fromfile=f"Old Replacement ({filename})",
                    tofile=f"New Replacement ({filename})"
                )
                diff_list.append("\n".join(diff))
    end_time = time.time()
    total_elapsed_time = end_time - start_time
    print(f"Total time taken: {total_elapsed_time} seconds")
    if not os.path.exists(RESULTS_FOLDER):
        os.mkdir(RESULTS_FOLDER)
    timestamp = datetime.datetime.now().isoformat()
    result_file_name = f"{RESULTS_FOLDER}/results-{timestamp}.diff"
    with open(result_file_name, "w") as results_file:
        results_header = "\n".join([
            "-------------------------------",
            f"Old Preprocess: {old_preprocess_name}",
            f"New Preprocess: {new_preprocess_name}",
            f"Total files handled: {matching_file_count + differing_file_count}",
            f"Matching files: {matching_file_count}",
            f"Differing files: {differing_file_count}",
            f"Run at: {timestamp}",
            f"Total time taken: {total_elapsed_time}",
            "-------------------------------"
        ])
        results_body = DIFF_LIST_DELIMITER.join(reversed(diff_list))
        results_str = f"{results_header}\n{results_body}"
        results_file.write(results_str)
    print(f"Validity test results written to: {result_file_name}")

def build_original_preprocess_factory(replacement_table):
    def factory(chapter_text):
        return MTL_Preprocess(chapter_text, replacement_table)
    return factory

def build_nlp_preprocess_factory(
        replacement_table, 
        tokenizer, 
        tag_potential_proper_nouns=True,
        single_kanji_filter=False
    ):
    name_list = NLP_MTL_Preprocess.generate_name_list_from_replacement_table(replacement_table)
    def factory(chapter_text):
        tagger = Tagger(
            tokenizer=tokenizer,
            tag_potential_proper_nouns=tag_potential_proper_nouns,
            proper_noun_list=name_list,
        )
        return NLP_MTL_Preprocess(
            text=chapter_text, 
            tagger=tagger, 
            replacement_table=replacement_table,
            single_kanji_filter=single_kanji_filter
        )
    return factory


def main():
    fugashi_tokenizer = FugashiTokenizer(user_dic_path=FUGASHI_USER_DIC_PATH)
    sudachi_tokenizer = SudachiTokenizer(user_dic_path=SUDACHI_USER_DIC_PATH)
    spacy_tokenizer = SpacyTokenizer(user_dic_path=SUDACHI_USER_DIC_PATH)
    with open(REPLACEMENT_TABLE_FILENAME) as replacement_table_file:
        replacement_table = json.loads(replacement_table_file.read())
    fileset = sorted(glob.glob(f"{DOCS_FOLDER}/*.txt"))
    old_preprocess_factory = build_nlp_preprocess_factory(replacement_table, fugashi_tokenizer)
    new_preprocess_factory = build_nlp_preprocess_factory(replacement_table, spacy_tokenizer)
    run_validity_test(
        fileset=fileset,
        old_preprocess_name="Fugashi MTL Preprocess",
        old_preprocess_factory=old_preprocess_factory,
        new_preprocess_name="Spacy MTL Preprocess",
        new_preprocess_factory=new_preprocess_factory,
    )

if __name__ == "__main__":
    main()