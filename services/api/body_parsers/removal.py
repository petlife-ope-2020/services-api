from flask_restful.reqparse import RequestParser


class RemovalParser:
    """ Request parser for removing the sender into the list of
        providers for the specified service.
    """
    def __init__(self):
        parser = RequestParser()
        fields = [
            {'name': 'petshop_username', 'type': str, 'location': 'form', 'required': True},
            {'name': 'service_id', 'type': str, 'location': 'form', 'required': True}
        ]
        for field in fields:
            parser.add_argument(**field)
        self.fields = parser.parse_args()
