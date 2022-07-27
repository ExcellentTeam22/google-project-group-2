import os

# Networking and
PATH_OF_FILES = r"C:\tar5\Archive"
PATH_OF_TEXT = r"C:\tar5\words_alpha.txt"
ALPHABET = "abcdefghijklmnopqrstuvwxyz1234567890 "
GLOBAL_DICT = {}
MAX_FILES = 1000
K = 5


class TrieNode:
    """A node in the trie structure"""

    def __init__(self, char):
        # the character stored in this node
        self.char = char

        # whether this can be the end of a word
        self.is_end = False

        # a counter indicating how many times a word is inserted
        # (if this node's is_end is True)
        self.counter = 0

        # a dictionary of child nodes
        # keys are characters, values are nodes
        self.children = {}


class Trie(object):
    """The trie object"""

    def __init__(self):
        """
        The trie has at least the root node.
        The root node does not store any character
        """
        self.root = TrieNode("")

    def insert(self, word):
        """Insert a word into the trie"""
        node = self.root

        # Loop through each character in the word
        # Check if there is no child containing the character, create a new child for the current node
        for char in word:
            if char in node.children:
                node = node.children[char]
            else:
                # If a character is not found,
                # create a new node in the trie
                new_node = TrieNode(char)
                node.children[char] = new_node
                node = new_node

        # Mark the end of a word
        node.is_end = True

        # Increment the counter to indicate that we see this word once more
        node.counter += 1

    def dfs(self, node, prefix):
        """Depth-first traversal of the trie

        Args:
            - node: the node to start with
            - prefix: the current prefix, for tracing a
                word while traversing the trie
        """
        if node.is_end:
            self.output.append((prefix + node.char, node.counter))

        for child in node.children.values():
            self.dfs(child, prefix + node.char)

    def query(self, x):
        """Given an input (a prefix), retrieve all words stored in
        the trie with that prefix, sort the words by the number of
        times they have been inserted
        """
        # Use a variable within the class to keep all possible outputs
        # As there can be more than one word with such prefix
        self.output = []
        node = self.root

        # Check if the prefix is in the trie
        for char in x:
            if char in node.children:
                node = node.children[char]
            else:
                # cannot found the prefix, return empty list
                return []

        # Traverse the trie to get all candidates
        self.dfs(node, x[:-1])

        # Sort the results in reverse order and return
        return sorted(self.output, key=lambda x: x[1], reverse=True)


GLOBAL_TREE = Trie()


def add_to_global_dict(filename: str) -> None:
    """
    A function that receives a path to a file and inserts all the words in it into the dictionary
    :param filename: A path to a file
    """
    with open(filename, encoding='utf-8') as fin:
        for lineno, line in enumerate(fin):
            for position, word in enumerate(line.split()):
                word = handle_input(word)
                GLOBAL_DICT.setdefault(word, []).append((filename, lineno, position))
                GLOBAL_TREE.insert(word)


def initialization(path: str) -> None:
    """
    You get a path of a folder that stores all the files (and additional folders)
    and puts all the words in them into the dictionary
    :param path: A path of the main folder
    """
    list_of_files = []
    for path, dirnames, filenames in os.walk(PATH_OF_FILES):
        for filename in filenames:
            list_of_files.append(path + "\\" + filename)
    for file_name in list_of_files[:MAX_FILES:]:
        # for file_name in list_of_files:
        add_to_global_dict(file_name)


# -------------------------------------------------------------------------- #
# -------------------------------------------------------------------------- #
# -------------------------------------------------------------------------- #


def my_intersection(set_1: list, set_2: list) -> list:
    """
    A function that builds the list of possible cuts between the input words (or similar).
    :param set_1: The set of words that have already been intersected
    :param set_2: Words to cut with set_1
    :return: List of all intersections
    """
    matches = {}
    for series_of_tuples in (set_1, set_2):
        for tuple in series_of_tuples:
            matches.setdefault(tuple[:2], []).append(tuple)

    return [values for values in matches.values() if len(values) > 1]


def relevant_matching(matchings: list, word_1, word_2) -> list:
    """
    A function that returns the list of intersections that do exist in the files
    :param matchings: A list of intersections between the input words or similar
    - not necessarily present in the files.
    :return: List of possible search results (unranked)
    """
    #
    ret = []
    for matching in matchings:
        for i in range(len(matching)):
            for j in range(len(matching)):
                if matching[i][2] + 1 == matching[j][2]:
                    with open(matching[i][0], encoding='utf-8') as f:
                        line = handle_input(f.readlines()[matching[i][1]]).split()
                        for i2 in range(len(line) - 1):
                            if line[i2] == word_1 and line[i2 + 1] == word_2:
                                ret.append(matching[j])

    return ret


def suggest_correction(word: str, offset: int) -> list:
    """
    A function that receives a word and an offset and returns a list
    of tuples of close words in the dictionary and a score on them
    :param word:
    :param offset:
    :return:
    """
    existing_words = GLOBAL_DICT.keys()
    length = len(word)
    # if length < 3:
    #    return []
    correct_words = []
    lst_word = list(word)
    new_lst = lst_word
    mistake = 0

    # replace letter
    for i in reversed(range(0, length)):
        if offset + i > 3:
            mistake = 1
        else:
            mistake = 5 - (offset + i)
        for letter in ALPHABET:
            new_lst[i] = letter
            new_word = "".join(new_lst)
            if new_word in existing_words:
                # incorrect letter removes also 2 from the score
                correct_words += [(new_word, mistake + 2)]
        new_lst = list(word)

    # remove letter
    for i in reversed(range(0, length)):
        if offset + i > 3:
            mistake = 2
        else:
            mistake = 10 - 2 * (offset + i)
        new_lst[i] = ''
        new_word = "".join(new_lst)
        if new_word in existing_words:
            # incorrect letter removes also 2 from the score
            correct_words += [(new_word, mistake + 2)]
        new_lst = list(word)

    # add a letter
    for i in reversed(range(0, length)):
        if offset + i > 3:
            mistake = 2
        else:
            mistake = 10 - 2 * (offset + i)
        new_lst1 = new_lst[:i] + [0] + new_lst[i:]
        for letter in ALPHABET:
            new_lst1[i] = letter
            new_word = "".join(new_lst1)
            if new_word in existing_words:
                correct_words += [(new_word, mistake)]
        new_lst = list(word)

    correct_words = list(set(correct_words))
    correct_words.sort(key=lambda a: a[1])
    l = []
    for i in correct_words:
        if i[0] != word:
            l.append(i)
    return l


def list_with_index(substring: str) -> list:
    """
    Receives a string and returns it as a list containing a tuple for each word in the string
    that is built from the word and its index relative to the position in the input
    :param substring: A string to be parsed into a list
    :return: The list of tuples: word and index
    """

    index = 0
    list_of_substring = substring.split(" ")
    list_of_tuples = [(list_of_substring[0], index)]
    for i in range(1, len(list_of_substring)):
        index += len(list_of_substring[i]) + 1
        list_of_tuples += [(list_of_substring[i], index)]
    return list_of_tuples


def not_only_complete_words(substring: str) -> list:
    options = GLOBAL_TREE.query(substring.split()[-1])
    print("option: ", options)
    options = [i[0] for i in options]
    len_without_last_word = len(substring) - len(substring.split()[-1])
    relevant_sentace = []
    for option in options:
        print(substring[:len_without_last_word] + option)
        relevant_sentace += only_complete_words(substring[:len_without_last_word] + option)
        if len(relevant_sentace) > 4:
            return relevant_sentace

    return relevant_sentace


def only_complete_words(substring: str) -> list:
    """
    Checks whether the user's input ends with a space - a whole word,
    and accordingly looks for completion
    :param substring: user's input
    :return: The list of optional sentences
    """
    optional_sentences = []
    lists_of_closed_words = []
    substring_list_with_index = list_with_index(substring)
    sum_of_wrong_words = 0
    index_in_substring = 0
    for word in range(len(substring_list_with_index)):
        if substring_list_with_index[word][0] not in set(GLOBAL_DICT.keys()):
            sum_of_wrong_words += 1
            wrong_word = substring_list_with_index[word][0]
        index_in_substring = index_in_substring + 1 + len(substring_list_with_index[word][0])
    if sum_of_wrong_words > 1:
        return []
    if sum_of_wrong_words == 1:
        lists_of_closed_words = suggest_correction(wrong_word, index_in_substring)
        for closed_word in lists_of_closed_words:
            optional_sentences.append(
                tuple([substring.replace(wrong_word, closed_word[0]), 2 * len(substring) - closed_word[1]]))
    if sum_of_wrong_words == 0:
        optional_sentences.append(tuple([substring, 2 * len(substring)]))
        for word in substring_list_with_index:
            lists_of_closed_words.append(suggest_correction(word[0], word[1]))
        for i in range(len(lists_of_closed_words)):
            for closed_words in lists_of_closed_words[i]:
                optional_sentences.append(tuple([substring.replace(substring_list_with_index[i][0], closed_words[0]),
                                                 2 * len(substring) - closed_words[1]]))
    optional_sentences.sort(key=lambda a: a[1], reverse=True)
    print("lists_of_closed_words: ", lists_of_closed_words)
    print("optional_sentences: ", optional_sentences)

    relevant_sentences = []
    for optional_sentence in optional_sentences:
        relevant_sentences += (search_substring(optional_sentence[0]))
        if len(relevant_sentences) > 4:
            return list(set(relevant_sentences))[:5]
    print("relevant_sentences", relevant_sentences)
    return list(set(relevant_sentences))


def search_proper_sentence(substring: str) -> list:
    """
    Checks that there are no spaces at the end of the input and downloads if there is,
    in order to avoid disruptions in the search
    :param substring: user's input
    :return: The list of optional sentences
    """
    if substring[-1] != " ":
        return not_only_complete_words(substring)
    while substring[-1] == " ":
        substring = substring[:-1]
    return only_complete_words(substring)


def search_substring(substring: str):
    # substring,score = substring_and_score
    # print("substring: ", substring)
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
        word_1 = substring_list[0]
        if match_1 == None:
            match_1 = []
        for word in substring_list[1:]:
            # list of indexes for first word
            match_2 = GLOBAL_DICT.get(word)
            word_2 = word
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
            match_1 = relevant_matching(intersection, word_1, word_2)
            word_1 = word
    return match_1


def handle_input(my_str) -> str:
    """
    Removes characters other than letters or numbers from the input
    in order to make the search more efficient
    :param my_str: user's input
    :return: User input without extra characters
    """
    return "".join([i for i in my_str.lower() if i in ALPHABET])


def print_by_tuple(list_of_tuples) -> None:
    """
    The function receives a list of tuples and print them in a way that is understandable to the user
    :param list_of_tuples: tuples in the structure of:
    (the completed sentence, source of the sentence, offset relative to the completed sentence)
    """
    counter = 0
    print("list_of_tuples: ", list_of_tuples)
    for i in list_of_tuples:
        file_name = i[0].split("\\")[-1].replace('.txt', '')
        counter += 1
        with open(i[0], encoding='utf-8') as f:
            line = f.readlines()[i[1]][:-1]
            print(counter, ". ", line, " (", file_name, ", ", i[2], " )")


if __name__ == '__main__':
    print("The system is ready. ")
    # offline
    initialization(PATH_OF_TEXT)
    # online
    substring = handle_input(input("Enter your text:"))
    while substring[0] == " ":
        substring = substring[1:]
    while "!" not in substring:
        while "#" not in substring:
            print("Here are the suggestions:")
            list_of_sentences_with_substring = search_proper_sentence(substring)
            if not list_of_sentences_with_substring:
                print('nothing')
                break
            print_by_tuple(list_of_sentences_with_substring)
            substring += input(substring)
            if "#" in substring:
                break
            substring += handle_input(substring)
        substring = handle_input(input("Enter your text:"))
