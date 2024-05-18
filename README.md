# Songmate

## Introduction

Have you ever wanted to find out if someone has a similar taste in music as you? Look no further to find out if that
person is your‘Songmate!’

A person’s music taste is often a great way to find common ground for conversation and connect with them. However,
the long-winded approach of asking them what songs they listen to is often tedious and impractical. This is why our
group set out to devise a simpler way to find how similar your musical interests are to other people.

‘Songmate!’ is an interactive website that gives music taste compatibility between two users. Both users are asked
to choose two songs each from the given song directory. Based on its existing database (comprising multiple users,
and their song ratings recorded on file), the website not only returns a similarity score representing their musical
compatibility, but also gives recommendations of songs common to both the users, based on similar genre and artist.
All that the user is required to know to use this site is their song preferences. In the future, Songmate has the
potential to be the next social media trend, akin to ‘Spotify wrapped’ or ‘Receiptify’ since it could be a fun way for
people to share and repost their compatibility scores with friends on their social media.

## Datasets Description

The name and description of all datasets:

Project Dataset:We manually created a dataset containing information about User’s Ratings of songs. The songs
were picked up from Spotify’s Top 50 Songs of 2023 list. Each row represents user’s rating of a song, with the first
column indicating user’s ID, the second column indicating the name of the song that the user rated, and the third
column indicating the rating given by the user. The ratings range from 1 to 5 (both inclusive), with 1 being the
lowest and 5 being the highest. The dataset is for 20 users where each user has rated 10 songs and hence there are
200 entries (excluding header).

Song dataset: This dataset was manually created and the songs were picked up from Spotify’s Top 50 songs of 2023. The dataset consists of a single column containing the names of the songs.

Libraries Used :

- Tkinter: Tkinter is one of the few GUI frameworks that are built-in the standard Python library. This makes
    it a good choice for a Python-based project since it integrates well with other Python libraries and frameworks.
    As opposed to our initial decision to use Flask and JavaScript to create a webpage as our GUI, TKinter proved
    to be much more efficient and uniform in its implementation. It was easier for all the team members to get
    acquainted with since it was Python-based, and it was very convenient to be able to integrate frontend and
    backend. As described above, we used the various data types in TKinter like Frames, Apps, Label, Button,
    Entry and RadioButton to optimise our GUI.
- Spotipy: Spotipy is a python library for the Spotify Web API. Spotipy provides us with a simple and easy- to-
    use interface to the Spotify Web API. It handles authentication with Spotify and provides us a set of functions
    to access the API endpoints and retrieve data. In this project we first created a spotify developer account
    followed by creating a new Spotify App to get our Client ID and Client Secret. We used these credentials to set
    up authentication credentials for using Spotipy functions. We first use this function’s library of search which returns a track corresponding to the song name input. We also use the artist function to get the artist name for
that particular track. Then we finally use the recommendations function of this library to get recommendations
based on the input list of genres (genres they both like) and input list of artists (artists they both listen to).
- Pandas: Pandas is an open source library which provides fast, powerful, flexible and easy-to-use data analysis
    and manipulation tools. We have used this library in the gettrackmetadata function to return a dataframe
    containing information about each song, including the genres associated with the song. This information is
    then used by the getsimilargenres function to extract the genres associated with the songs listened to by
    each user and find the intersection of these sets, which represents the genres that both users have in common.
    Representing our data as data frames is useful because it allows us to use Pandas capabilities such as the‘loc’
    function. This function provides a clear and explicit way to select rows and columns of a DataFrame or Series
    using label-based indexing, making it easy to access and filter rows based on ‘songname’ for example.

## Computational Overview

We have used bipartite weighted graphs to store information from our Project Dataset. In this graph, there are two
types of vertices or nodes: ‘Song’ and ‘User’. The edges between these vertices has a weight associated with them,
representing how much a ‘User’ likes a ‘Song’ on a scale of 1 to 5. One of the key features of this graph is that an
edge can only exist between a ‘User’ and a ‘Song’, due to the graph being bipartite.

The functions where graphs play a central role are:findallpaths, getsimilarityscore,getsimilargenres, getsimilarartists,
songrec

In these functions, graphs play a central role in representing and analysing the relationships between users and
songs.

- In the findallpaths method, a bipartite weighted graph is used to represent the relationships between users
    and songs. The vertices of the graph represent users and songs, while the edges represent the ratings given by
    users to songs. The method uses this graph to find all possible paths between a source node and a destination
    node.
- In the getsimilarityscore method, the graph is used to calculate the similarity score between two users. The
    method calls the findallpaths method to find all possible paths between the two users and then calculates the
    average rating for each path. The overall average rating across all paths is then used to calculate the similarity
    score between the two users.
- getsimilargenres: Given two lists of songs and their corresponding ratings, the function first extracts a list of
    all song names from both lists. It then retrieves metadata for each song using the gettrackmetadata function,
    which returns a pandas DataFrame containing information about each song, including the genres associated
    with the song. The genres associated with the songs listened to by each user are then extracted and stored as
    sets. The function returns the intersection of these sets, which represents the genres that both users have in
    common.
- getsimilarartists: This function is similar to getsimilargenres, but instead of extracting genres, it extracts
    the artists associated with each song. The function returns a list of artists that both users have in common.
- The songrec function takes three arguments: givennetwork, source, and destination. It returns a list of
    recommended songs based on the songs rated 3 and above by both users and then finds the set of genres that
    are similar between the two users. It retrieves the list of available genres from the Spotify API and selects only
    the genres that are similar between both the users. The function then finds the set of artists that are similar
    between the two users and searches for their artist IDs on the Spotify API. If there are no similar artists or
    genres, the function returns a string with a message. Otherwise, it uses the Spotify API to retrieve a list of
    recommended tracks based on the similar artists and genres and returns a list of the recommended tracks.

We have defined a network data class that represents a weighted bipartite graph that is built using adduser and
addsong methods. These methods create new User and Song objects to add them to the users and songs dictionar-
ies respectively. Once the users and songs have been added to the network, the addedge method can be used to
connect users and songs by adding edges between them with specified weights. These weights represent the ratings
given by users to songs. (data filtering performed with the help of pandas data frames in recommendation function,


getsimilargenres, and getsimilarartists where we compute intersections in the likes of two users)

How the program reports the results of our computation in an interactive way?

Songmate uses the TKinter library to create a python-operated Graphical User Interface (GUI). We have used
inheritance in the GUI frontend code, by making a main class for the whole application (MainApplication) and other
children classes which act as individual pages or ‘frames’. Every frame uses some or all of the following widget types:

- Label: Single lines of text to be displayed and formatted using helper attributes like font, background etc.
- Entry: A block of text taking a user input and storing it in the backend to use in other required functions.
- Button: A button that performs a function like switching between pages, entering data etc.
- RadioButton: A way of representing options to be selected by the user.

The TKinter GUI makes use of all the other modules defined in the function to integrate all the functionalities
of SongMate on user inputs.


## Instructions to run the Project

- Firstly make sure Python 3.11 and Pycharm are installed on your computer.
- Download all files provided onto the computer, in a new folder.
- Install the additional Python libraries found in the requirements.txt file by opening the requirements.txt file
    and right-clicking and selecting ”Install All Packages”, or by installing each library individually in the PyCharm
    settings windows.
- Now download the dataset zip file and extract the datasets in the same folder as the python files.
- Now run the main.py file and a graphical user interface (GUI) will open up.
- On the very first page of the GUI, the user needs to click on the empty space below ‘User 1’ and ‘User 2’ to
    input the names of first user and second user in the Entry widgets. Then press “Begin as User 1” at the very
    bottom. Look at the image below for reference

![](Aspose.Words.e45fe2e8-af08-4019-8063-ba35e3e53447.001.png)

- Now on the second page, user 1 has to rate 5 songs given by writing a number between 1 to 5 (both inclusive) right below each song name. Look at the image for reference. Then press “Next”. Look at the image below for reference.

![](Aspose.Words.e45fe2e8-af08-4019-8063-ba35e3e53447.002.png)

- Repeat the above step for user 2. Then press “Next”. Look at the image below for reference
- Now on this page, choose one of the two options. If the two users want their similarity score and recommendations, select “Overall Similarity Score” and if the users want common genre and recommendations then select “Genre Similarity”. Now press “Next”.

![](Aspose.Words.e45fe2e8-af08-4019-8063-ba35e3e53447.003.png)

- This page would show the results based on the option chosen. If you chose “Overall Similarity Score”, the percentage displayed would be the similarity score between two users with a few common songs between the two users recommended below. Look at the image for reference if you choose this option.

![](Aspose.Words.e45fe2e8-af08-4019-8063-ba35e3e53447.004.png)

- If the option chosen was “Genre Similarity”, then first the common genres between the two users are

displayed, below which are again a few common songs between the two users that are recommended. Look at

the image below for reference.

![](Aspose.Words.e45fe2e8-af08-4019-8063-ba35e3e53447.005.png)

## Changes to Project Plan

While our goal for the project remains the same, there have been some modifications in the implementation. Firstly,
we had planned to assign rankings to our dataset of songs using python and the random module. However, we
decided to utilise the capabilities of Microsoft Excel by generating random integer ranking values for each song in
our csv file using the ‘RANDBETWEEN’ function.

Furthermore, instead of the initial idea of creating a website using HTML, CSS, Javascript and the Flask API,


we opted for Tkinter to build our user interface. Tkinter is a GUI framework that is built into the standard Python
library and it also creates a cross-platform GUI that can be accessed easily across WindowsOS, MacOS, Linux etc.
Also, it broadened the scope of python libraries that we were incorporating in our project.

Another design decision we made was to remove the search bar. Instead, each user will be shown 5 random songs
from the existing dataset (songs which are also in our graph). They will need to give each song a ranking between 1
and 5. These inputs will be the weights added to edges between songs and new user nodes.

Moreover, our former implementation simply gave the users their ‘SongMate percentage’ i.e. their similarity score.
In our current project, we have added more data analysis a give the users a wider array of parameters to assess their
‘music taste similarity’. These include getting similargenres in their song selection as well as getting a list of song
recommendations that both users are likely to enjoy.

## Discussion

We have two different kinds of results available based on what the users is asking. Our front end will provide the
users with two options which are “overall similarity score” and “genre similarity”

The first result i.e., overall similarity score is giving the similarity score of two users based on their music taste
which we achieve by the ratings that they provided for 5 songs each. So basically we are telling how good of “Song-
Mate” they both are. Also as an additional feature we will provide them song recommendations to the liking of both
users.

The second result i.e., genre similarity will return the genres that both the users like which will again be achieved
from the ratings they provided to 5 different songs each. The mechanism is as denoted in the computational overview.
Also after outputting the common genre, we will again provide them with song recommendations based on the com-
mon genre and any artist that they like in common.

Our results are directly addressing and fulfilling our project goal which was to provide music taste compatibility
between two users in the form of a similarity score and recommend songs based on their common liking of genres
and artists.

We did encounter a few limitations which were:

- Our dataset is comparatively small and hence the accuracy is not as great. There are a limited number of
    songs, users and a limited number of ratings and hence the graph is not as huge leading to less connectedness
    and hence less accuracy.
- Another limitation was the accuracy of the songs being recommended. Collaborative filtering is a technique
    used in recommender systems to provide personalised recommendations to users based on their past behaviour
    or preferences, as well as the behaviour and preferences of other similar users. Collaborative filtering has much
    higher accuracy because it has a realistic record and is using that to recommend songs. However we could not
    achieve collaborative filtering because of limited data. If we had the Spotify history of users or the listening
    history we could have provided better recommendations. Therefore, we achieved our goal of recommending
    songs by content- based filtering which is a technique used to provide personalised recommendations to users
    based on the characteristics or features of items that the user has interacted with or rated positively which
    we achieved by looking at neighbour nodes i.e., neighbour songs rated 3 and above. This has a drawback
    because the user may not have rated many songs 3 or above, reducing the data available used to provide
    recommendations. There may even be a possibility where the user rated all songs below 3 where we will not be
    able to provide any recommendations because there is no point of recommending songs based on songs that the
    user already dislikes. Hence content- based filtering has this drawback which won’t be present in collaborative
    filtering because of its nature of accessing past records.

Limitations: not accounting for errors due to invalid ranking values input by user due to time constraints in the
scope of the project. In the future, error frames could be added to the Tkinter GUI to circumvent this.

Certain steps we can take to increase accuracy and explore further in this domain are:


- Asking for further interests of users. For example instead of just asking them to rate 5 random songs, we can
    ask them to mention their favourite genres or their favourite artists. We can then recommend songs based on
    their own provided info. We can make it much more similar to apps like Pinterest or Spotify which before
    starting asks for areas we may like or would like to explore. This way we take into consideration the user’s will
    and then recommend accordingly with increased accuracy.
- Furthermore, as mentioned in the limitations, if we somehow get the music history of a user, we can increase the
    accuracy by large amounts. We can analyse the listening habits of users, make comparisons and connections
    using historical listening behaviour, and then predict what users would want to hear in the future.
- Another scope of exploration could be to find a better algorithm to find the similarity score. Instead of taking
    averages of all possible paths when we traverse in the graph from one user to another, we can come up with
    a better algorithm which restricts the traversal to paths whose rating/ weight is always 3 or above or another
    better condition. This way we would never take a path which uses a bad rating or does not fulfil that particular
    condition and hence limiting the paths and increasing the accuracy.

Therefore, our project shows varied results from similarity scores to common song recommendations by creating and
using a closely connected bipartite graph with users and songs. It still has some scope for improvement in terms of
accuracy which can always be explored in the future.

## References

GeeksforGeeks. (2022, December 15). Check whether a given graph is bipartite or not. GeeksforGeeks. Retrieved
March 8, 2023, from https://www.geeksforgeeks.org/bipartite-graph/

Lamere, Paul. “Welcome to Spotipy!¶.” Welcome to Spotipy! - Spotipy 2.0 Documentation, Spotipy,
https://spotipy.readthedocs.io/en/2.18.0/#spotipy.client.Spotify.recommendationgenreseeds.

“Build with Spotify’s 100 Million Songs.” Home — Spotify for Developers, Spotify https://developer.spotify.com/.

NumFOCUS, Inc. (n.d.). Pandas documentation#. pandas documentation - pandas 1.5.3 documentation. Re-
trieved March 8, 2023, from https://pandas.pydata.org/docs/

puja84375. “Dealing with Rows and Columns in Pandas DataFrame.” GeeksforGeeks, GeeksforGeeks, 13 Oct. 2021,
https://www.geeksforgeeks.org/dealing-with-rows-and-columns-in-pandas-dataframe/.

