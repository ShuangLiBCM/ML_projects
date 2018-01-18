# Modules, Classes, and Objects

class Song():

    def __init__(self, lyrics):
        self.lyrics = lyrics

    def sing_me_a_song(self):
        for line in self.lyrics:
            print(line)

happy_bday = Song(["Happy birthday to you", "i don't want to get sued"])

bulls_on_parade = Song(["They rally around the family", "With pockest full of shells"])

happy_bday.sing_me_a_song()

bulls_on_parade.sing_me_a_song()
