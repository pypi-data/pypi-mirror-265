from codec.resources.collections.types import CollectionObject
from codec.resources.videos.types import VideoObject


def format_video_object(video_object):
    if isinstance(video_object.get("collection"), dict):
        video_object["collection"] = CollectionObject(**video_object["collection"])

    video_object = VideoObject(**video_object)

    return video_object
