from services.utils.db.mongo_adapter import MongoAdapter


def get_mongo_adapter():
    if not get_mongo_adapter.adapter:
        get_mongo_adapter.adapter = MongoAdapter()
    return get_mongo_adapter.adapter


get_mongo_adapter.adapter = None
