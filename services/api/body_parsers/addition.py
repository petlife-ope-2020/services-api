from flask_restful.reqparse import RequestParser


class AdditionParser:
    """ Request parser for adding the sender into the list of
        providers for the specified service.
    """
    def __init__(self):
        parser = RequestParser()
        fields = [
            {'name': 'service_id', 'type': str, 'location': 'form', 'required': True},
            {'name': 'petshop_username', 'type': str, 'location': 'form', 'required': True},
            {'name': 'petshop_name', 'type': str, 'location': 'form', 'required': True}
        ]
        for field in fields:
            parser.add_argument(**field)
        self.fields = parser.parse_args()
