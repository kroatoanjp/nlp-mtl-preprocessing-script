# Test validity of NLP-based MTL replacement by comparing output with
# that of the original MTL script for the first 620 chapters of the
# Re:Zero WN

import difflib
import glob
import json
import time
import datetime
import os

from preprocess.mtl_preprocess import MTL_Preprocess
from preprocess.nlp_mtl_preprocess import NLP_MTL_Preprocess
from preprocess.tokenizer.fugashi_tokenizer import FugashiTokenizer

DOCS_FOLDER = "preprocess/tests/docs/rezero"
REPLACEMENT_TABLE_FILENAME = "replacement_table/rezero.json"
USER_DIC_PATH = "data/dictionaries/rezero.dic"
RESULTS_FOLDER = "validity-test-results"

def main():
    with open(REPLACEMENT_TABLE_FILENAME) as replacement_table_file:
        replacement_table = json.loads(replacement_table_file.read())

    name_list = NLP_MTL_Preprocess.generate_name_list_from_replacement_table(replacement_table)
    diff_list = []
    DIFF_LIST_DELIMITER = '\n===================\n'
    matching_file_count = 0
    differing_file_count = 0
    start_time = time.time()
    for filename in sorted(glob.glob(f"{DOCS_FOLDER}/*.txt")):
        with open(filename) as docfile:
            print("Starting " + filename)
            chapter_text = docfile.read()
            old_preprocess = MTL_Preprocess(chapter_text, replacement_table)
            old_preprocess.replace()
            tokenizer = FugashiTokenizer(
                user_dic_path=USER_DIC_PATH,
                tag_potential_proper_nouns=True,
                proper_noun_list=name_list,
            )
            new_preprocess = NLP_MTL_Preprocess(
                text=chapter_text, 
                tokenizer=tokenizer, 
                replacement_table=replacement_table,
                single_kanji_filter=False,
            )
            new_preprocess.replace()
            if old_preprocess.text == new_preprocess.text:
                matching_file_count += 1
                print(f"NLP MTL Preprocess aligns with original MTL_Preprocess for chapter file: {filename}")
            else:
                differing_file_count += 1
                print(f"NLP MTL Preprocess differs from original MTL_Preprocess for chapter file: {filename}")
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

if __name__ == "__main__":
    main()