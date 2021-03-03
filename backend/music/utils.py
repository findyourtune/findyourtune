# Grabbing some important information to display
def get_track_obj(track):
    return {
        'name': track['name'],
        'images': track['album']['images'],
        'artist': track['artists'][0],
        'popularity': track['popularity'],
        'url': track['external_urls']['spotify'],
        'item_id': track['id'],
        'preview_url': track['preview_url'],
        'item_type': track['type']
    }
    

def get_album_obj(album):
    return {
        'name': album['name'],
        'images': album['images'],
        'artist': album['artists'][0],
        'tracks': album['total_tracks'],
        'item_id': album['id'],
        'item_type': album['type']
    }
    
    
def get_playlist_obj(playlist):
    artist = {
        'name': playlist['owner']['display_name']
    }
    return {
        'name': playlist['name'],
        'images': playlist['images'],
        'artist': artist,
        'tracks': playlist['tracks']['total'],
        'item_id': playlist['id'],
        'item_type': playlist['type']
    }