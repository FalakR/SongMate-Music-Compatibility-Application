""" Recommender module
"""

# contains functions that return similar genres between the two users and recommend songs that the users would like
# based on their common artists and sliked genres

from typing import Any
import pandas as pd
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from data_classes import Network


def get_track_metadata(song_name: str) -> dict[str, list[Any] | Any] | None:
    """

    :param song_name:
    :return:
    """
    # Spotify API credentials
    client_id = '37fa6c57bee34f3ab47ac9e2964480fd'
    client_secret = '1b659e87704f4bf3b5da098d03c87c99'

    client_credentials_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
    sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

    track_results = sp.search(q=song_name, type='track')

    if track_results['tracks']['total'] == 0:
        return None

    track_info = track_results['tracks']['items'][0]
    metadata = {
        'song_name': track_info['name'],
        'song_id': track_info['id'],
        'artist_name': track_info['artists'][0]['name'],
        'album_name': track_info['album']['name'],
        'duration_ms': track_info['duration_ms'],
        'popularity': track_info['popularity'],
        'genres': []
    }
    # Retrieve genre information for the song's artists
    artist_id = track_info['artists'][0]['id']
    artist_results = sp.artist(artist_id)
    for genre in artist_results['genres']:
        metadata['genres'].append(genre)
    return metadata


def get_similar_genres(user1_songs: list[tuple[str, int]],
                       user2_songs: list[tuple[str, int]]) -> \
        set[Any]:
    """
    Return a set of similar genres between the two lists of tuples of song and their corresponding rating

    Preconditions:
    - user1_songs != []
    - user2_songs != []
    """
    user1_song_list = [song_1[0] for song_1 in user1_songs]
    user2_song_list = [song_2[0] for song_2 in user2_songs]
    song_list = user1_song_list + user2_song_list  # List of songs to retrieve metadata for

    # Retrieve metadata for all songs and store in a DataFrame
    song_metadata = pd.DataFrame(
        columns=['song_name', 'song_id', 'artist_name', 'album_name', 'duration_ms', 'popularity', 'genres'])
    for song in song_list:
        metadata = get_track_metadata(song)
        if metadata is not None:
            song_metadata = song_metadata.append(metadata, ignore_index=True)

    lst_so_far_1 = []
    for i in range(0, len(user1_song_list)):
        value = song_metadata.iloc[i]['genres']
        lst_so_far_1.extend(value)

    lst_so_far_2 = []
    for i in range(len(user1_song_list), len(song_list)):
        value = song_metadata.iloc[i]['genres']
        lst_so_far_2.extend(value)

    user1_genres = set(lst_so_far_1)
    user2_genres = set(lst_so_far_2)

    sim_genres = user1_genres.intersection(user2_genres)

    return sim_genres


def get_similar_artists(user1_songs: list[tuple[str, int]],
                        user2_songs: list[tuple[str, int]]) -> \
        list[Any]:
    """
    Return a list of similar artists between the two lists of tuples of song and their corresponding rating

    Preconditions:
    - user1_songs != []
    - user2_songs != []
    """

    user1_song_list = [song_1[0] for song_1 in user1_songs]
    user2_song_list = [song_2[0] for song_2 in user2_songs]
    song_list = user1_song_list + user2_song_list

    # Retrieve metadata for all songs and store in a DataFrame
    song_metadata = pd.DataFrame(
        columns=['song_name', 'song_id', 'artist_name', 'album_name', 'duration_ms', 'popularity', 'genres'])
    for song in song_list:
        metadata = get_track_metadata(song)
        if metadata is not None:
            song_metadata = song_metadata.append(metadata, ignore_index=True)

    lst_so_far_1 = []
    for i in range(0, len(user1_song_list)):
        value = song_metadata.iloc[i]['artist_name']
        lst_so_far_1.append(value)

    lst_so_far_2 = []
    for i in range(len(user1_song_list), len(song_list)):
        value = song_metadata.iloc[i]['artist_name']
        lst_so_far_2.append(value)

    user1_artists = set(lst_so_far_1)
    user2_artists = set(lst_so_far_2)

    sim_artists = list(user1_artists.intersection(user2_artists))
    return sim_artists


def song_rec(given_network: Network, source: str, destination: str) -> list | str:
    """
    Return a list of all recommended songs based on the songs rated 3 and above by each user. The recommendation will be
    based on the genres and artists that are shared by the two users.
    """
    # Spotify API credentials
    client_id = '37fa6c57bee34f3ab47ac9e2964480fd'
    client_secret = '1b659e87704f4bf3b5da098d03c87c99'

    client_credentials_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
    sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

    user1_favs = [x for x in given_network.users[source].songs if x[1] >= 3]
    user2_favs = [y for y in given_network.users[destination].songs if y[1] >= 3]

    available_lst = sp.recommendation_genre_seeds()
    sim_genres = [x for x in list(get_similar_genres(user1_favs, user2_favs)) if x in available_lst['genres']]

    sim_artists_ids = []
    for artist_name in get_similar_artists(user1_favs, user2_favs):
        # search for the artist by name
        results = sp.search(q='artist:' + artist_name, type='artist')

        # get the artist ID from the search results
        if len(results['artists']['items']) > 0:
            sim_artists_ids.append(results['artists']['items'][0]['id'])

    if (sim_artists_ids == []) and (sim_genres == []):
        return "Sorry, no similarities found :( Try again with someone else, we hope you'll find your songmate!"
    else:
        recs = sp.recommendations(seed_artists=sim_artists_ids, seed_genres=sim_genres, limit=5)
        return [f"{track['name']} by {track['artists'][0]['name']}" for track in recs['tracks']]


if __name__ == '__main__':
    # When you are ready to check your work with python_ta, uncomment the following lines.
    # (In PyCharm, select the lines below and press Ctrl/Cmd + / to toggle comments.)
    # You can use "Run file in Python Console" to run PythonTA,
    # and then also test your methods manually in the console.
    import python_ta

    python_ta.check_all(config={
        'extra-imports': ['data_classes', 'pandas', 'spotipy', 'spotipy.oauth2'],
        # the names (strs) of imported modules
        'allowed-io': [],  # the names (strs) of functions that call print/open/input
        'max-line-length': 120
    })
