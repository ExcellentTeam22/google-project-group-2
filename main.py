import os

# Networking and
PATH_OF_FILES = r"C:\tar5\Archive"
PATH_OF_TEXT = r"C:\tar5\words_alpha.txt"
ALPHABET = "#abcdefghijklmnopqrstuvwxyz1234567890 "
GLOBAL_DICT = {}
MAX_FILES = 3


def add_to_global_dict(filename):
    with open(filename, encoding='utf-8') as fin:
        for lineno, line in enumerate(fin):
            for position, word in enumerate(line.split()):
                word = handle_input(word.lower())
                GLOBAL_DICT.setdefault(word, []).append((filename, lineno, position))


def initialization(path: str) -> list:
    """
    Receive a file path and return list of all words in the file
    :param path:
    :return: list of words
    """
    list_of_files = []
    for path, dirnames, filenames in os.walk(PATH_OF_FILES):
        for filename in filenames:
            list_of_files.append(path + "\\" + filename)
    for file_name in list_of_files[:MAX_FILES:]:
        add_to_global_dict(file_name)


def search_substring(dict_of_words: dict, substring: str) -> str:
    """
    Receive a list of words and a substring and return a list with only the words that
    contains the given substring
    :param list_of_words:
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


def check_order(matchings:list, substring: str)->list:
    list_of_correct_matchings= []
    for matching in matchings:
        if matching[0][2]+1 == matching[1][2]:
            list_of_correct_matchings.append(matching[1])
    return list_of_correct_matchings





def new_search(substring: str):
    match_1 = []
    if " " not in substring: # One word search
        # match = [value for key, value in GLOBAL_DICT.items() if substring in key]
        match_1 = GLOBAL_DICT.get(substring)
    else:  # If the search has more than one word
        substring_list = substring.split(" ")

        match_1 = GLOBAL_DICT.get(substring_list[0])
        for word in substring_list[1:]:
            match_2 = GLOBAL_DICT.get(word)
            intersection = my_intersection(match_1, match_2)
            intersection = check_order(intersection,substring)
            match_1 = intersection

    return match_1


def handle_input(my_str):
    new_str = "".join([i for i in my_str if i in ALPHABET])
    return new_str
def print_by_tuple(list_of_tuples):
    for i in list_of_tuples:
        with open (i[0], encoding='utf-8') as f:
            print(f.readlines()[i[1]])

if __name__ == '__main__':
    print("The system is ready. ")
    # offline
    list_of_words = initialization(PATH_OF_TEXT)
    # online
    substring = input("Enter your text:").lower()
    substring = handle_input(substring)
    while "#" not in substring:
        print("Here are the suggestions:")
        list_of_sentences = new_search(substring)
        print_by_tuple(list_of_sentences)
        substring += input(substring).lower()
        substring = handle_input(substring)
