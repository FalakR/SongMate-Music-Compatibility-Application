"""CSC111 project main runner file.

This file is Copyright (c) Krisha Kalsi, Harnehmat Kaur, Gurveen Kaur Sahni, Falak Rastogi.
"""

import tkinter as tk
import csv
import random
from typing import Any
import network
import recommender

list_tup1 = []
list_tup2 = []


def create_song_list(file: str) -> list[str]:
    """Returns a list of songs from the csv file."""
    songs1 = []
    with open(file, 'r') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            songs1.append(row[0])
    return songs1


songs = create_song_list('songs.csv')


def join_with_comma(my_set: set) -> str:
    """Returns a str containing all elements of the input set separated by commas."""
    return ', '.join(my_set)


class MainApplication(tk.Tk):
    """A class representing the main underlying interface, having several pages or 'frames'.
    """
    frames: dict

    def __init__(self, *args: tuple[Any], **kwargs: dict[str, tuple[Any]]) -> None:
        """Initialises the MainApplication class."""
        super().__init__(*args, **kwargs)

        self.title("SongMate")
        self.geometry("800x800+0+0")  # set size and center on screen
        self.config(width=600, height=600)

        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f'{width}x{height}+{x}+{y}')

        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (StartPage, PageOne, PageTwo, PageThree, PageFour):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(StartPage)

    def show_frame(self, cont: Any) -> None:
        """Shows the frame with the name 'cont'."""
        frame = self.frames[cont]
        frame.tkraise()

    def get_info(self, info: str, page_name: Any) -> None:
        """Configures the label of the page with name 'page_name' to show the text 'info'."""
        self.frames[page_name].label.config(text=f'Hello {info}!')

    def store_info(self, info: dict[str, int]) -> None:
        """Stores the 'info' dictionary in a global variable."""
        global list_tup1, list_tup2
        if self.frames[PageFour].dict1 == {}:
            self.frames[PageFour].dict1 = info
            list_tup1 = [(song, info[song]) for song in info]
        else:
            self.frames[PageFour].dict2 = info
            list_tup2 = [(song, info[song]) for song in info]

    def store_choice(self, info: str) -> None:
        """Stores the choice (of the Radiobutton from PageThree) and makes changes in the PageFour frame as required."""
        self.frames[PageFour].choice = info
        self.frames[PageFour].label1.config(text=f'{info}')
        new_network = network.read_csv_file('project_dataset.csv')
        user_id1, user_id2 = network.new_user_input(new_network, list_tup1, list_tup2)
        recommendations = recommender.song_rec(new_network, user_id1, user_id2)
        if isinstance(recommendations, list):
            my_list = recommendations
            self.frames[PageFour].label3.config(text=f'{my_list[0]}')
            self.frames[PageFour].label4.config(text=f'{my_list[1]}')
            self.frames[PageFour].label5.config(text=f'{my_list[2]}')
            self.frames[PageFour].label6.config(text=f'{my_list[3]}')
            self.frames[PageFour].label7.config(text=f'{my_list[4]}')
        else:
            self.frames[PageFour].label3.config(text=recommendations, wraplength=500)
        if info == 'Overall Similarity Score':
            similarity_score = new_network.get_similarity_score(user_id1, user_id2)
            self.frames[PageFour].label2.config(text=f'{int(similarity_score)}%', font=('Arial', 45))
        else:
            genre_similarity = recommender.get_similar_genres(list_tup1, list_tup2)
            self.frames[PageFour].label2.config(text=join_with_comma(genre_similarity), font=('Arial', 45),
                                                wraplength=400)


class StartPage(tk.Frame):
    """A class representing the frame for the introductory page of the GUI."""
    user1_entry: tk.Entry
    user2_entry: tk.Entry
    controller: Any

    def __init__(self, parent: Any, controller: Any) -> None:
        """Initialises the StartPage class."""
        super().__init__(parent)

        label = tk.Label(self, text='Welcome to Songmate!', font=("Arial", 24))
        label.pack(side='top', fill='both', expand=True, pady=10)

        label = tk.Label(self, text='Rate songs to find out your true songmate!', font=("Arial", 20))
        label.pack(side='top', fill='both', expand=True, pady=10)

        label = tk.Label(self, text='Please enter your names:', font=("Arial", 18))
        label.pack(side='top', fill='both', expand=True, pady=10)

        user1_label = tk.Label(self, text='User 1:', font=('Arial', 25))
        user1_label.pack(side='top', fill='both', expand=True, pady=5)
        self.user1_entry = tk.Entry(self, borderwidth=2)
        self.user1_entry.pack(side='top', fill='both', expand=True, pady=5)
        self.user1_entry.focus()

        user2_label = tk.Label(self, text='User 2:', font=('Arial', 25))
        user2_label.pack(side='top', fill='both', expand=True, pady=5)
        self.user2_entry = tk.Entry(self, borderwidth=2)
        self.user2_entry.pack(side='top', fill='both', expand=True, pady=5)

        button = tk.Button(self, text="Begin as User 1", command=self.submit)
        button.pack(pady=10, padx=10)

        self.controller = controller

    def submit(self) -> None:
        """Sends the inputs from the entry widgets to the respective frames, and transitions to the next frame."""
        name1 = self.user1_entry.get()
        name2 = self.user2_entry.get()
        self.controller.get_info(name1, PageOne)
        self.controller.get_info(name2, PageTwo)

        self.controller.show_frame(PageOne)


class PageOne(tk.Frame):
    """A class representing the frame for the first page of the GUI that takes inputs."""
    label: tk.Label
    entry1_entry: tk.Entry
    entry2_entry: tk.Entry
    entry3_entry: tk.Entry
    entry4_entry: tk.Entry
    entry5_entry: tk.Entry
    controller: Any
    subset: list

    def __init__(self, parent: Any, controller: Any) -> None:
        """Initialises the PageOne class."""
        super().__init__(parent)

        self.label = tk.Label(self, text="", font=("Arial", 20))
        self.label.pack(pady=10, padx=10)

        label = tk.Label(self, text='Please rate the following songs on a scale of 1 to 5:', font=("Arial", 20))
        label.pack(side='top', fill='both', expand=True, pady=10)

        label = tk.Label(self, text='(you cannot give the same rating to two different songs!)', font=("Arial", 12))
        label.pack(side='top', fill='both', expand=True, pady=10)

        self.subset = random.sample(songs, 5)

        song1_label = tk.Label(self, text=self.subset[0])
        song1_label.pack(side='top', fill='both', expand=True, pady=5)
        self.entry1_entry = tk.Entry(self)
        self.entry1_entry.pack(side='top', fill='both', expand=True, pady=5)
        self.entry1_entry.focus()

        song2_label = tk.Label(self, text=self.subset[1])
        song2_label.pack(side='top', fill='both', expand=True, pady=5)
        self.entry2_entry = tk.Entry(self)
        self.entry2_entry.pack(side='top', fill='both', expand=True, pady=5)

        song3_label = tk.Label(self, text=self.subset[2])
        song3_label.pack(side='top', fill='both', expand=True, pady=5)
        self.entry3_entry = tk.Entry(self)
        self.entry3_entry.pack(side='top', fill='both', expand=True, pady=5)

        song4_label = tk.Label(self, text=self.subset[3])
        song4_label.pack(side='top', fill='both', expand=True, pady=5)
        self.entry4_entry = tk.Entry(self)
        self.entry4_entry.pack(side='top', fill='both', expand=True, pady=5)

        song5_label = tk.Label(self, text=self.subset[4])
        song5_label.pack(side='top', fill='both', expand=True, pady=5)
        self.entry5_entry = tk.Entry(self)
        self.entry5_entry.pack(side='top', fill='both', expand=True, pady=5)

        button = tk.Button(self, text='Next', command=self.go_to_page_two)
        button.pack(expand=True, pady=5)

        self.controller = controller

    def go_to_page_two(self) -> None:
        """Stores the required values as a dictionary and transitions to the next frame."""
        dict1 = {}
        dict1[self.subset[0]] = int(self.entry1_entry.get())
        dict1[self.subset[1]] = int(self.entry2_entry.get())
        dict1[self.subset[2]] = int(self.entry3_entry.get())
        dict1[self.subset[3]] = int(self.entry4_entry.get())
        dict1[self.subset[4]] = int(self.entry5_entry.get())
        self.controller.store_info(dict1)

        self.controller.show_frame(PageTwo)


class PageTwo(tk.Frame):
    """A class representing the frame for the second page of the GUI that takes inputs."""
    label: tk.Label
    entry1_entry: tk.Entry
    entry2_entry: tk.Entry
    entry3_entry: tk.Entry
    entry4_entry: tk.Entry
    entry5_entry: tk.Entry
    controller: Any
    subset: list

    def __init__(self, parent: Any, controller: Any) -> None:
        """Initialises the PageTwo class."""
        super().__init__(parent)

        self.label = tk.Label(self, text="", font=("Arial", 20))
        self.label.pack(pady=10, padx=10)

        label = tk.Label(self, text='Please rate the following songs on a scale of 1 to 5:', font=("Arial", 20))
        label.pack(side='top', fill='both', expand=True, pady=10)

        label = tk.Label(self, text='(you cannot give the same rating to two different songs!)', font=("Arial", 12))
        label.pack(side='top', fill='both', expand=True, pady=10)

        self.subset = random.sample(songs, 5)

        song1_label = tk.Label(self, text=self.subset[0])
        song1_label.pack(side='top', fill='both', expand=True, pady=5)
        self.entry1_entry = tk.Entry(self)
        self.entry1_entry.pack(side='top', fill='both', expand=True, pady=5)
        self.entry1_entry.focus()

        song2_label = tk.Label(self, text=self.subset[1])
        song2_label.pack(side='top', fill='both', expand=True, pady=5)
        self.entry2_entry = tk.Entry(self)
        self.entry2_entry.pack(side='top', fill='both', expand=True, pady=5)

        song3_label = tk.Label(self, text=self.subset[2])
        song3_label.pack(side='top', fill='both', expand=True, pady=5)
        self.entry3_entry = tk.Entry(self)
        self.entry3_entry.pack(side='top', fill='both', expand=True, pady=5)

        song4_label = tk.Label(self, text=self.subset[3])
        song4_label.pack(side='top', fill='both', expand=True, pady=5)
        self.entry4_entry = tk.Entry(self)
        self.entry4_entry.pack(side='top', fill='both', expand=True, pady=5)

        song5_label = tk.Label(self, text=self.subset[4])
        song5_label.pack(side='top', fill='both', expand=True, pady=5)
        self.entry5_entry = tk.Entry(self)
        self.entry5_entry.pack(side='top', fill='both', expand=True, pady=5)

        button = tk.Button(self, text='Next', command=self.go_to_page_three)
        button.pack(expand=True, pady=5)

        self.controller = controller

    def go_to_page_three(self) -> None:
        """Stores the required values as a dictionary and transitions to the next frame."""
        dict2 = {}
        dict2[self.subset[0]] = int(self.entry1_entry.get())
        dict2[self.subset[1]] = int(self.entry2_entry.get())
        dict2[self.subset[2]] = int(self.entry3_entry.get())
        dict2[self.subset[3]] = int(self.entry4_entry.get())
        dict2[self.subset[4]] = int(self.entry5_entry.get())
        self.controller.store_info(dict2)

        self.controller.show_frame(PageThree)


class PageThree(tk.Frame):
    """A class representing the frame for the third page of the GUI that takes inputs."""
    choice: tk.StringVar
    controller: Any

    def __init__(self, parent: Any, controller: Any) -> None:
        """Initialises the PageThree class."""
        super().__init__(parent)

        label = tk.Label(self, text='Please select between the following options to see if you are songmates!',
                         font=("Arial", 30), wraplength=400)
        label.pack(side='top', fill='both', expand=True, padx=10, pady=10)

        self.choice = tk.StringVar(value='Overall Similarity Score')

        tk.Radiobutton(self, text="Overall Similarity Score", variable=self.choice, value='Overall Similarity Score',
                       font=("Arial", 30)).pack(expand=True, pady=10)
        tk.Radiobutton(self, text="Genre Similarity", variable=self.choice, value='Genre Similarity',
                       font=("Arial", 30)).pack(expand=True, pady=10)

        button1 = tk.Button(self, text='Next', command=self.go_to_page_four)
        button1.pack(padx=5, pady=5)

        self.controller = controller

    def go_to_page_four(self) -> None:
        """Stores the input choice from the frame into a variable, and transitions to the next frame."""
        choice = self.choice.get()
        self.controller.store_choice(choice)
        self.controller.show_frame(PageFour)


class PageFour(tk.Frame):
    """A class representing the frame for the last page of the GUI."""
    dict1: dict
    dict2: dict
    label1: tk.Label
    label2: tk.Label
    label3: tk.Label
    label4: tk.Label
    label5: tk.Label
    label6: tk.Label
    label7: tk.Label
    choice: str
    controller: Any

    def __init__(self, parent: Any, controller: Any) -> None:
        """Initialises the PageFour class."""
        super().__init__(parent)
        self.dict1, self.dict2 = {}, {}
        self.choice = ''

        self.label1 = tk.Label(self, text='', font=("Arial", 40))
        self.label1.pack(side='top', fill='both', expand=True, padx=10, pady=10)

        self.label2 = tk.Label(self, text='', font=("Arial", 40))
        self.label2.pack(side='top', fill='both', expand=True, padx=10, pady=10)

        label = tk.Label(self, text='Some songs that you and your songmate may vibe to together:', font=('Arial', 20))
        label.pack(side='top', fill='both', expand=True, padx=10, pady=10)

        self.label3 = tk.Label(self, text='', font=("Arial", 20))
        self.label3.pack(side='top', fill='both', expand=True, padx=10, pady=10)

        self.label4 = tk.Label(self, text='', font=("Arial", 20))
        self.label4.pack(side='top', fill='both', expand=True, padx=10, pady=10)

        self.label5 = tk.Label(self, text='', font=("Arial", 20))
        self.label5.pack(side='top', fill='both', expand=True, padx=10, pady=10)

        self.label6 = tk.Label(self, text='', font=("Arial", 20))
        self.label6.pack(side='top', fill='both', expand=True, padx=10, pady=10)

        self.label7 = tk.Label(self, text='', font=("Arial", 20))
        self.label7.pack(side='top', fill='both', expand=True, padx=10, pady=10)

        self.controller = controller


if __name__ == "__main__":
    app = MainApplication()
    app.mainloop()

    import python_ta

    python_ta.check_all(config={
        'extra-imports': ['tkinter', 'csv', 'random', 'network', 'recommender'],  # the names (strs) of imported modules
        'allowed-io': ['create_song_list'],  # the names (strs) of functions that call print/open/input
        'max-line-length': 120
    })
