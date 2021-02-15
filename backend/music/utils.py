# Grabbing some important information to display
def get_track_obj(track):
    Dict = {}
    name = track['name']
    images = track['album']['images']
    artist = track['artists'][0]
    popularity = track['popularity']
    Dict['name'] = name
    Dict['images'] = images
    Dict['artist'] = artist
    Dict['popularity'] = popularity
    return Dict