""" Networks module
"""
# creates and modifies network based on input data from users

import csv
from data_classes import Network


def read_csv_file(file: str) -> Network:
    """ Read csv file data to create a Network/graph with nodes.
    """
    with open(file) as f:
        reader = csv.reader(f, delimiter=',')
        next(reader)

        new_network = Network()
        for row in reader:
            user_id = row[0]
            song_name = row[1]  # access the song and call it my_song
            rating = int(row[2])  # access the rating and call it rating
            new_network.add_user(user_id)
            new_network.add_song(song_name)
            new_network.add_edge(user_id, song_name, rating)
        return new_network


def new_user_input(input_network: Network, user1_songs: list[tuple[str, int]], user2_songs: list[tuple[str, int]]) -> \
        tuple[str, str]:
    """ Takes the songs and ratings given by the two users and adds them to the network.

    user1_songs: a list of tuples of the form (song_name, rating) for the input selected by user1
    user2_songs:  a list of tuple of the form (song_name, rating) for the inpur selected by user2
    """

    # generate new user ids and add the 2 users to network
    user_1_id = input_network.generate_user_id()
    input_network.add_user(user_1_id)
    for single_song in user1_songs:
        input_network.add_song(single_song[0])
        user1_rating = single_song[1]
        input_network.add_edge(user_1_id, single_song[0], user1_rating)

    user_2_id = input_network.generate_user_id()
    input_network.add_user(user_2_id)
    for song_tuple in user2_songs:
        user2_song = song_tuple[0]
        input_network.add_song(user2_song)
        user2_rating = song_tuple[1]
        input_network.add_edge(user_2_id, user2_song, user2_rating)

    return (user_1_id, user_2_id)


if __name__ == '__main__':

    # When you are ready to check your work with python_ta, uncomment the following lines.
    # (In PyCharm, select the lines below and press Ctrl/Cmd + / to toggle comments.)
    # You can use "Run file in Python Console" to run PythonTA,
    # and then also test your methods manually in the console.
    import python_ta
    python_ta.check_all(config={
        'extra-imports': ['csv', 'data_classes'],  # the names (strs) of imported modules
        'allowed-io': ['read_csv_file'],  # the names (strs) of functions that call print/open/input
        'max-line-length': 120
    })
