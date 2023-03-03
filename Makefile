.PHONY: freeze validity-test  unit-test clean

clean:
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '__pycache__' -exec rm -fr {} +
	find . -name 'validity-test-results' -exec rm -fr {} +
	find . -name 'generated-mecab-dict-csv' -exec rm -fr {} +

freeze:
	pip3 freeze > requirements.txt

unit-test:
	-python3 -m unittest preprocess.tests.test_basic_named_entity_recognition
	-python3 -m unittest preprocess.tests.test_tagger
	-python3 -m unittest preprocess.tests.test_replacement_validity
	-python3 -m unittest preprocess.tests.test_sentence
	-python3 -m unittest preprocess.tests.test_utils

validity-test:
	python3 -m preprocess.tests.rezero_exhaustive_replacement_validity_test
# 	python3 -m preprocess.tests.cote_exhaustive_replacement_validity_test
