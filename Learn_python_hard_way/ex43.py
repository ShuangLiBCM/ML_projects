# Basic OOP analysis and design
from sys import exit
from random import randint
from textwrap import dedent

class Scene(object):

    def enter(self):
        print("This scene is not yet configured.")
        print("Subclass it and impletment enter().")
        exit(1)

class Engine(object):

    def __init__(self, scene_map):
        self.scene_map = scene_map

    def play(self):
        current_scene = self.scene_map.opening_scene()
        last_scene = self.scene_map.next_scene('finished')

        while current_scene != last_scene:
            next_scene_name = current_scene.enter()
            current_scene = self.scene_map.next_scene(next_scene_name)

        # be sure to print out the last scene
        current_scene.enter()

class Death(Scene):

    quips = [
    "You died.",
    "Your Mom would be proud...",
    "Such a luser",
    ]
    def enter(self):
        print(Death.quips[randint(0, len(self.quips)-1)])
        exit(1)

class CentralCorridor(Scene):

    def enter(self):
        print(dedent("""
            The Gothons of planet percal
            """))

            action = input(">")

            if action == "Shoot!":
                print(dedent("""
                Quick on the draw"""))

                return 'death'

            elif action == "dodge!":
                print(dedent("""
                like a world class boxer"""))

                return 'death'

            elif action == 'tell a joke':
                print(dedent("""
                Lucky for you they made you learn
                """))

                return 'laser_weapon_armory'
            else:
                print('DOES NOT COMPUTE!')
                return 'central_corridor'

class LaserWeaponArmory(Scene):

    def enter(self):
        print(dedent("""
        You do a dive roll into the weapon armory"""))

        code = f"{randint(1,9)}{randint(1,9){randint(1,9)}}"
        guess = input("[keypad]> ")
        guesses = 0

        while guess != code and guesses < 10:
            print("BZZZZEDDD!")
            guesses += 1
            guess = input("[keypad]> ")

        if guess == code:
            print(dedent("""
                The container click"""))

            return 'the bridge'
        else:
            print(dedent("""The lock buzzes one las time"""))
            return 'death'

class TheBridge(Scene):

    def enter(self):
        print(dedent("""You burst onto the dridge with the netron destruct bomb"""))

        action = input("> ")

        if action == "throw the bomb":
            print(dedent("""You point your blaster at the bomb"""))
            return 'death'
        elif action == 'slowly place the bomb'
            print(dedent("""You point your blaster at the bomb"""))

            return 'escape_pod'
        else:
            print("DOES NOT COMPUTE!")
            return "the_bridge"

class EscapePod(Scene):

    def enter(self):
        print(dedent("""You rush through the ship"""))

        good_pod = randint(1,5)
        guess = input("[pod #]> ")

        if int(guess) != good_pod:
            print(dedent("""You jump into pod {guess} and hit the eject button"""))
            return 'death'
        else:
            print(dedent("""You jump into pod {guess} and hit the eject button"""))
            return 'finished'

class Finished(Scene):

    def enter(self):
        print("You won! Good job.")
        return 'finished'

class Map(object):

    scenes = {
        'central_corridor': CentralCorridor(),
        'laser_weapon_armory': LaserWeaponArmory(),
        'the_bridge': TheBridge(),
        'escape_pod': EscapePod(),
        'death': Death(),
        'finished': Finished(),
    }

    def __init__(self, start_scene):
        self.start_scene = start_scene

    def next_scene(self, scene_name):
        val = Map.scenes.get(scene_name)
        return val

    def opening_scene(self):
        return self.next_scene(self.start_scene)

a_map = Map('central_corridor')
a_game = Engine(a_map)
a_game.play()
