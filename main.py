PATH_OF_TEXT = r"C:\tar5\words_alpha.txt"


def initialization(path: str) -> list:
    """
    Receive a file path and return list of all words in the file
    :param path:
    :return: list of words
    """
    with open(path) as f:
        all_lines = [line.rstrip() for line in f]
    f.close()
    return all_lines


def search_substring(list_of_words: list, substring: str) -> str:
    """
    Receive a list of words and a substring and return a list with only the words that
    contains the given substring
    :param list_of_words:
    :param substring:
    :return:
    """
    return [word for word in list_of_words if substring in word]


if __name__ == '__main__':
    print("The system is ready. ")
    substring = input("Enter your text:")
    list_of_words = initialization(PATH_OF_TEXT)
    print("Here are the suggestions:")
    print(*(x for x in search_substring(list_of_words, substring)), sep='\n')
