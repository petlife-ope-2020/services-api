import re

from flask_restful import abort

from services.utils.ngrams import make_ngrams
from services.utils.db.adapter_factory import get_mongo_adapter
from services.api.body_parsers.search import SearchParser


# pylint: disable=inconsistent-return-statements
class SearchService:
    """ Searches for services on MongoDB using the ngrams text index
        for a fuzzy search capability.

        Args:
            service_name (str): Defined on parser, it can be blank, in which case
                                the search will return all of the available services.

        Returns:
            result (list): A list with the matched services
    """
    def __init__(self):
        self.parser = SearchParser()

    def search(self):
        """ Calls the field validations and converts
            the term into ngrams for index searching
        """
        user_query = self.parser.field
        self._check_forbidden_characters(user_query)
        search_term = make_ngrams(user_query)
        result = self._search_in_mongo(search_term)
        return result

    @staticmethod
    def _check_forbidden_characters(user_input):
        if re.match(r'{([^}]+)}', user_input):
            abort(403, extra='Invalid service name.')

    @staticmethod
    def _search_in_mongo(user_query_ngrams):
        mongo = get_mongo_adapter()
        try:
            return mongo.get_service_by_name(user_query_ngrams)
        except KeyError as error:
            abort(404, extra=f'{error}')
