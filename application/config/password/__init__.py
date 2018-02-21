import os

dir_path = os.path.dirname(os.path.realpath(__file__))
partial_word_file_path = os.path.join(dir_path, 'password_filter_partial_restricted_words.txt')
full_word_file_path = os.path.join(dir_path, 'password_filter_restricted_words.txt')
with open(partial_word_file_path, 'r') as infile:
    restricted_partial_word_list = [line.strip('\n').lower() for line in infile.readlines()]
with open(full_word_file_path, 'r') as infile:
    restricted_word_list = [line.strip('\n').lower() for line in infile.readlines()]
