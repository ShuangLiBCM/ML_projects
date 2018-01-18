# Script for running shuang's game
from shuang_game.DoorEntry import *

scene = {
    'building': Building(),
    'safeguard': SafeGuard(),
}

def main():

    scene_map = 'safeguard'
    while True:
        current_scene = scene[scene_map]
        scene_map = current_scene.enter()

if __name__ == '__main__':
    main()
