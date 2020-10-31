import unittest

from services.utils.ngrams import make_ngrams


class MakeNgramsTestCase(unittest.TestCase):

    def test_get_mongo_adapter_first_call(self):
        # Setup
        word = 'ngrams'

        # Act
        word_ngrams = make_ngrams(word)

        # Assert
        self.assertEqual(len(word_ngrams), 49)
