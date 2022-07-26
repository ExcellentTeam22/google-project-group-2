import os

# Networking and
PATH_OF_FILES = r"C:\tar5\Archive"
PATH_OF_TEXT = r"C:\tar5\words_alpha.txt"
ALPHABET = "#abcdefghijklmnopqrstuvwxyz1234567890 "
GLOBAL_DICT = {}
MAX_FILES = 3


def add_to_global_dict(filename):
    """

    :param filename:
    :return:
    """
    with open(filename, encoding='utf-8') as fin:
        for lineno, line in enumerate(fin):
            for position, word in enumerate(line.split()):
                word = handle_input(word)
                GLOBAL_DICT.setdefault(word, []).append((filename, lineno, position))


def initialization(path: str):
    """
    Receive a file path and return list of all words in the file
    :param path:
    """
    list_of_files = []
    for path, dirnames, filenames in os.walk(PATH_OF_FILES):
        for filename in filenames:
            list_of_files.append(path + "\\" + filename)
    for file_name in list_of_files[:MAX_FILES:]:
        add_to_global_dict(file_name)


# def search_substring(dict_of_words: dict, substring: str) -> str:
    """
    Receive a list of words and a substring and return a list with only the words that
    contains the given substring
    :param dict_of_words:
    :param substring:
    :return:
    """
    #return [value for key, value in dict_of_words.items() if substring in key]


def my_intersection(set_1,set_2):
    matches= {}
    for series_of_tuples in (set_1, set_2):
        for tuple in series_of_tuples:
            matches.setdefault(tuple[:2], []).append(tuple)
    return [values for values in matches.values() if len(values) > 1]


def relevant_matching(matchings:list)->list:
    return [matching[1] for matching in matchings if matching[0][2]+1 == matching[1][2]]



def search_substring(substring: str):
    match_1 = []
    if " " not in substring: # One word search
        # (looking for part of word)
        # match = [value for key, value in GLOBAL_DICT.items() if substring in key]
        # (only complete word)
        match_1 = GLOBAL_DICT.get(substring)
    else:  # If the search has more than one word
        substring_list = substring.split(" ")
        # list of indexes for first word
        match_1 = GLOBAL_DICT.get(substring_list[0])
        for word in substring_list[1:]:
            # list of indexes for first word
            match_2 = GLOBAL_DICT.get(word)
            # list of pair lists, each pair has the same line and file, and different index
            intersection = my_intersection(match_1, match_2)
            # new list of relevant match, only the last index
            match_1 = relevant_matching(intersection)
    return match_1


def handle_input(my_str):
    my_str = my_str.lower()
    return "".join([i for i in my_str if i in ALPHABET])


def print_by_tuple(list_of_tuples):
    for i in list_of_tuples:
        with open (i[0], encoding='utf-8') as f:
            print(f.readlines()[i[1]])


if __name__ == '__main__':
    print("The system is ready. ")
    # offline
    initialization(PATH_OF_TEXT)
    # online
    substring = handle_input(input("Enter your text:"))
    while "#" not in substring:
        print("Here are the suggestions:")
        list_of_sentences_with_substring = search_substring(substring)
        print_by_tuple(list_of_sentences_with_substring)
        substring += handle_input(input(substring))
