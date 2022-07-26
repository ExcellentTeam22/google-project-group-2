import os

# Networking and
PATH_OF_FILES = r"C:\tar5\Archive"
PATH_OF_TEXT = r"C:\tar5\words_alpha.txt"
ALPHABET = "#abcdefghijklmnopqrstuvwxyz1234567890 "
GLOBAL_DICT = {}
MAX_FILES = 1
K = 5


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


# -------------------------------------------------------------------------- #
# -------------------------------------------------------------------------- #
# -------------------------------------------------------------------------- #


def my_intersection(set_1, set_2):
    matches = {}
    for series_of_tuples in (set_1, set_2):
        for tuple in series_of_tuples:
            matches.setdefault(tuple[:2], []).append(tuple)
    return [values for values in matches.values() if len(values) > 1]


def relevant_matching(matchings: list) -> list:
    ret = []
    for matching in matchings:
        for i in range(len(matching)):
            for j in range(len(matching)):
                if matching[i][2] + 1 == matching[j][2]:
                    ret.append(matching[j])
    return ret

    # return [matching[1] for matching in matchings if matching[0][2] + 1 == matching[1][2]]


# noa
def suggest_correction(word: str) -> list:
    existing_words = GLOBAL_DICT.keys()
    length = len(word)
    correct_words = []
    lst_word = list(word)
    new_lst = lst_word

    # replace letter
    for i in reversed(range(0, length)):
        for letter in ALPHABET:
            new_lst[i] = letter
            new_word = "".join(new_lst)
            if new_word in existing_words:
                correct_words += [str(new_word)]
        new_lst = list(word)

        # remove letter
        new_lst[i] = ''
        new_word = "".join(new_lst)
        if new_word in existing_words:
            correct_words += [str(new_word)]
        new_lst = list(word)

        # add a letter
        new_lst1 = new_lst[:i] + [0] + new_lst[i:]
        for letter in ALPHABET:
            new_lst1[i] = letter
            new_word = "".join(new_lst1)
            if new_word in existing_words:
                correct_words += [str(new_word)]
        new_lst = list(word)
    my_set = set(correct_words)
    my_set.add(word)
    my_set.remove(word)
    return list(my_set)


def only_complete_words(substring: str) -> list:
    optional_sentences = []
    lists_of_closed_words = []
    substring_list = substring.split(" ")
    sum_of_wrong_words = 0
    wrong_word = ''
    for word in range(len(substring_list)):
        if substring_list[word] not in set(GLOBAL_DICT.keys()):
            sum_of_wrong_words += 1
            wrong_word = substring_list[word]
    if sum_of_wrong_words > 1:
        return []
    if sum_of_wrong_words == 1:
        lists_of_closed_words.append(suggest_correction(wrong_word))
        list_of_closed_words = lists_of_closed_words[0]
        for closed_word in list_of_closed_words:
            optional_sentences.append(substring.replace(wrong_word, closed_word))
            # optional_sentences.append(substring.replace(" "+wrong_word+" ", " "+closed_word+" "))
    if sum_of_wrong_words == 0:
        optional_sentences.append(substring)
        for word in substring_list:
            lists_of_closed_words.append(suggest_correction(word))
        for i in range(len(lists_of_closed_words)):
            for closed_words in lists_of_closed_words[i]:
                optional_sentences.append(substring.replace(substring_list[i], closed_words))
    print("lists_of_closed_words: ", lists_of_closed_words)
    print("optional_sentences: ", optional_sentences)
    relevant_sentences = []
    for optional_sentence in optional_sentences:
        relevant_sentences += (search_substring(optional_sentence))
    return list(set(relevant_sentences))


def search_proper_sentence(substring: str) -> list:
    while substring[0] == " ":
        substring = substring[1:]
    if substring[-1] != " ":
        return only_complete_words(substring)
    while substring[-1] == " ":
        substring = substring[:-1]
    return only_complete_words(substring)


def search_substring(substring: str):
    print("substring: ", substring)
    match_1 = []
    if " " not in substring:  # One word search
        # (looking for part of word)
        # match = [value for key, value in GLOBAL_DICT.items() if substring in key]
        # (only complete word)
        match_1 = GLOBAL_DICT.get(substring)
        if match_1 == None:
            match_1 = []
    else:  # If the search has more than one word
        substring_list = substring.split(" ")
        # list of indexes for first word
        match_1 = GLOBAL_DICT.get(substring_list[0])
        if match_1 == None:
            match_1 = []
        for word in substring_list[1:]:
            # list of indexes for first word
            match_2 = GLOBAL_DICT.get(word)
            if match_2 == None:
                match_2 = []
            # list of pair lists, each pair has the same line and file, and different index
            # print("match_1: ", match_1)
            # print("match_2: ", match_2)
            intersection = my_intersection(match_1, match_2)
            # print("intersection: ", intersection)
            if intersection == []:
                return []
            # new list of relevant match, only the last index
            match_1 = relevant_matching(intersection)
    return match_1


def handle_input(my_str):
    return "".join([i for i in my_str.lower() if i in ALPHABET])


def print_by_tuple(list_of_tuples):
    if list_of_tuples:
        for i in list_of_tuples:
            with open(i[0], encoding='utf-8') as f:
                print(f.readlines()[i[1]])


if __name__ == '__main__':
    print("The system is ready. ")
    # offline
    initialization(PATH_OF_TEXT)
    # online
    substring = handle_input(input("Enter your text:"))
    while substring[0] == " ":
        substring = substring[1:]
    while "#" not in substring:
        print("Here are the suggestions:")
        list_of_sentences_with_substring = search_proper_sentence(substring)
        if list_of_sentences_with_substring == []:
            print('nothing')
            break
        print_by_tuple(list_of_sentences_with_substring)
        substring += handle_input(input(substring))
