def make_ngrams(word):
    """ Creates a list of n-grams for a service name
        and turns it into a string, this is the backbone
        of this application's fuzzy search logic.

        Args:
            word (str): The word to be divided

        Returns:
            string containing all the n-grams
            separated by a blank space
    """
    min_size = 3
    length = len(word)
    size_range = range(min_size, max(length, min_size) + 1)
    n_grams_list = list(set(
        word[i:i + size]
        for size in size_range
        for i in range(0, max(0, length - size) + 1)
    ))
    return ' '.join(n_grams_list)
