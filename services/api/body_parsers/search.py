from flask_restful.reqparse import RequestParser


class SearchParser:
    """ Request parser for a search request, the only argument possible
        is the service name or a blank string.
    """
    def __init__(self):
        parser = RequestParser()
        parser.add_argument(
            name='service_name',
            type=str,
            location='args',
            required=True
        )
        self.field = parser.parse_args()['service_name']
