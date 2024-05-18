""" Dataclasses module
"""


# contains the dataclasses for the objects in the graph

class User:
    """A class representing a user which is part of the music recommendation system's network.

    Instance Attributes:
        - user_id: a str representing a unique id associated to the user.
        - songs: a list containing tuples of song_id of the song listened to, and the ranking of the song by the
        user (on a scale of 1 to 5).
    """
    user_id: str
    songs: list[tuple[str, int]]

    def __init__(self, user_id: str) -> None:
        """Initialises the User class."""
        self.user_id = user_id
        self.songs = []

    def rate_song(self, song_id: str, ranking: int) -> None:
        """Adds a song and its ranking to the list 'self.songs' in the form of a tuple.
        Preconditions:
            - all(song_id not in song_tuple for song_tuple in self.songs)
        """
        self.songs.append((song_id, ranking))


class Song:
    """A class respresenting a song which is part of the music recommendation system's network.

    Instance Attributes:
        - song_id: a str representing a unique id associated to the song.
        - users: a list containing tuples of user_id of the user this song has been ranked by, and the ranking
        attributed to the song by that user (on a scale of 1 to 5).
    """
    song_id: str
    users: list[tuple[str, int]]

    def __init__(self, song_id: str) -> None:
        """Initialises the Song class."""
        self.song_id = song_id
        self.users = []

    def get_rating(self, user_id: str, ranking: int) -> None:
        """Adds a user and the ranking of the song by this user to the list 'self.users' in the form of a tuple.
        Preconditions:
            - all(user_id not in user_tuple for user_tuple in self.users)
        """
        self.users.append((user_id, ranking))


class Network:
    """A class representing the network of songs and users in a music recommendation system.
    This network is a weighted bipartite graph, with two types of nodes -- users and songs.

    Instance Attributes:
        - users: a dict having user ids as keys and the corresponding User objects as values.
        - songs: a dict having song ids as keys and the corresponding Song objects as values.
    """
    users: dict[str, User]
    songs: dict[str, Song]

    def __init__(self) -> None:
        """Initialises the Network class."""
        self.users = {}
        self.songs = {}

    def generate_user_id(self) -> str:
        """Generate a user id for the new user"""
        id_set = {int(key) for key in self.users}
        new_id = max(id_set) + 1
        return str(new_id)

    def add_user(self, user_id: str) -> None:
        """Adds the user with user_id to the network."""
        if user_id not in self.users:
            self.users[user_id] = User(user_id)

    def add_song(self, song_id: str) -> None:
        """Adds the song with song_id to the network"""
        if song_id not in self.songs:
            self.songs[song_id] = Song(song_id)

    def add_edge(self, user_id: str, song_id: str, weight: int) -> None:
        """Connects the user and the song with the corresponding ids and assigns a weight to the edge."""
        if user_id in self.users and song_id in self.songs:
            self.users[user_id].rate_song(song_id, weight)
            self.songs[song_id].get_rating(user_id, weight)

    def find_all_paths(self, source: str, destination: str, path: list = None, cache: dict = None) -> \
            list[list[tuple[str, int]]]:
        """Returns a list of all possible paths from the source node to the destination node.

        Preconditions:
            - source in self.users or source in self.songs
            - destination in self.users or destination in self.songs
        """
        # if path is None:
        #     path = []
        # if cache is None:
        #     cache = {}
        path = path if path is not None else []
        cache = cache if cache is not None else {}

        source_is_user = source in self.users

        # Add the current node to the path
        if source_is_user:
            path = path + [(source, weight_user) for _, weight_user in self.users[source].songs]
        else:
            path = path + [(source, weight_song) for _, weight_song in self.songs[source].users]

        # If the current node is the target node, add the path to the list of paths found
        if source == destination:
            return [path]

        # Check if the paths from this node have already been computed
        if source in cache:
            return cache[source]

        # If the paths have not been computed, explore its neighbors recursively
        # paths = []
        # if source_is_user:
        #     for neighbor, weight in self.users[source].songs:
        #         if neighbor not in [p[0] for p in path]:
        #             new_paths = self.find_all_paths(neighbor, destination, path, cache)
        #             for new_path in new_paths:
        #                 paths.append([(source, weight)] + new_path)
        # else:
        #     for neighbor, weight in self.songs[source].users:
        #         if neighbor not in [p[0] for p in path]:
        #             new_paths = self.find_all_paths(neighbor, destination, path, cache)
        #             for new_path in new_paths:
        #                 paths.append([(source, weight)] + new_path)

        paths = []
        for neighbor, weight in (self.users[source].songs if source_is_user else self.songs[source].users):
            if neighbor not in [p[0] for p in path]:
                new_paths = self.find_all_paths(neighbor, destination, path, cache)
                for new_path in new_paths:
                    paths.append([(source, weight)] + new_path)

        # Cache the paths for this node
        cache[source] = paths
        return paths

    def get_similarity_score(self, source: str, destination: str) -> float:
        """Returns the similarity score between the source user and the destination user.

        Preconditions:
            - source in self.users
            - destination in self.users
        """
        if source == destination:
            return 100

        else:
            all_paths = self.find_all_paths(source, destination)
            # add case for no paths to avoid returning zero division error
            if not all_paths:
                return 0

            avg_so_far = []
            for path in all_paths:
                path_sum = sum(tup[1] for tup in path)
                path_num = len(path)
                path_avg = path_sum / path_num
                avg_so_far.append(path_avg)

            sum_so_far = sum(avg_so_far)
            num_so_far = len(avg_so_far)

            similar_rating = sum_so_far / num_so_far

        return (similar_rating / 5) * 100


if __name__ == '__main__':
    # When you are ready to check your work with python_ta, uncomment the following lines.
    # (In PyCharm, select the lines below and press Ctrl/Cmd + / to toggle comments.)
    # You can use "Run file in Python Console" to run PythonTA,
    # and then also test your methods manually in the console.
    import python_ta

    python_ta.check_all(config={
        'extra-imports': [],  # the names (strs) of imported modules
        'allowed-io': [],  # the names (strs) of functions that call print/open/input
        'max-line-length': 120
    })
