from flask_restful.reqparse import RequestParser


class CreationParser:
    """ Request parser for creating a service, the only argument possible
        is the service name.
    """
    def __init__(self):
        parser = RequestParser()
        parser.add_argument(
            name='service_name',
            type=str,
            location='form',
            required=True
        )
        self.field = parser.parse_args()
