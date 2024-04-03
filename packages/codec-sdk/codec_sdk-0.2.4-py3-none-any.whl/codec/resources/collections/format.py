from codec.resources.collections.types import CollectionObject
from codec.resources.videos.types import VideoObject
from codec.utils.type_utils import is_list_of_dicts


def format_collection_object(collection_object):
    if is_list_of_dicts(collection_object.get("videos")):
        collection_object["videos"] = [VideoObject(**video) for video in collection_object["videos"]]
    
    collection_object = CollectionObject(**collection_object)

    return collection_object
