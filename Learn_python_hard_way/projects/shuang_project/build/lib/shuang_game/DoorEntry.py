# Define functions to enter the gates
import random
import pdb

class SafeGuard(object):
    ID  = input("Show ID> ")

    def __init(self, ID):
        self.ID = ID

    def enter(self):
        if int(self.ID) > 0:
            return 'building'
        else:
            return 'safeguard'

class Building(object):

    def enter(self):
        password1 = random.randint(1,10)
        ans1 = input(f"Enter the binary code for {password1}: ")

        try:
            int(ans1, 2)
        except ValueError:
            print('Not a valid binary number')
            ans1 = input(f"Enter the binary code for {password1}: ")

        if int(ans1, 2) != password1:
            print('Wrong!')
            return 'building'
        else:
            print('Correct!')
            password2 = random.randint(1,10)
            ans2 = input("Enter the decimal code for {0:#b}: ".format(password2))

        if int(ans2) == password2:
            print("Congrautations! You passed")
            exit(0)
        else:
            print('Wrong!')
            return 'building'
#
# scene = {
#     'building': Building(),
#     'safeguard': SafeGuard(),
# }
#
# scene_map = 'safeguard'
# while True:
#     current_scene = scene[scene_map]
#     scene_map = current_scene.enter()
