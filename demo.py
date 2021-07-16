#! /usr/lib/python3

from grid import *
from pawn import *
from damage import *
from capability import *

def print_grid(grid: MapGrid):
    for i in range(grid.size[0]):
        line = ""
        for j in range(grid.size[1]):
            tile = grid.grid[i][j]
            t = ' '
            if tile.holding:
                t = tile.holding.gridtext or '?'
            line = line + t
        print( "[" + line + "]")

def main():
    grid = MapGrid(4, 4)
    player = Actor("Player", grid.grid[0][0])
    player.gridtext = 'O'
    player.capabilities = [
        CAP_Attack(player, 300),
        CAP_Thunder(player, 250)
    ]

    enemy1 = Actor("Enemy 1", grid.grid[3][3])
    enemy1.health_max = 500
    enemy1.health = 500
    enemy1.gridtext = 'X'
    enemy1.capabilities = [
        CAP_Attack(enemy1, 150),
    ]

    enemy2 = Actor("Enemy 2", grid.grid[3][0])
    enemy2.health_max = 500
    enemy2.health = 500
    enemy2.gridtext = 'X'
    enemy2.capabilities = [
        CAP_Attack(enemy2, 150),
    ]
    enemies = [enemy1, enemy2]

    input_to_dir = {
        'n': Dir.NORTH,
        'e': Dir.EAST,
        's': Dir.SOUTH,
        'w': Dir.WEST,
    }

    while True:

        print_grid(grid)

        print("it is your turn")
        # player acts
        i = ""
        while i != "m" and i != "a" and i != "x":
            i = input("choose to move (m) or act (a); (x) to quit: ")

        if i == "x":
            return

        if i == "m":
            steps = 3
            d = ""
            while steps > 0:
                d = input(f"input a direction to move (n,e,s,w) or stop (x); {steps} steps left: ")
                if d == "x":
                    steps = 0
                elif input_to_dir[d]:
                    t = player.tile.neighbors[input_to_dir[d]]
                    if player.move(input_to_dir[d]):
                        steps = steps - 1
                        print_grid(grid)
                    else:
                        print("you can't move there!")
        elif i == "a":
            a = ""
            while True:
                a = input(f"input an action to take: attack(a) or thunder(t); (x) to skip: ")
                if a == "x":
                    break
                elif a != "a" and a != "t":
                    continue
                d = ""
                while not d in input_to_dir:
                    d = input(f"input a direction (n,e,s,w): ")
                if a == "a":
                    player.use_capability(player.capabilities[0], input_to_dir[d])
                else:
                    player.use_capability(player.capabilities[1], input_to_dir[d])
                break

        enemies = [e for e in enemies if e.is_alive()]
        if len(enemies) == 0:
            print("you win!")
            return

        print("it is the enemies' turn")
        # enemy acts
        for e in enemies:
            print_grid(grid)
            # attack if next to player
            if player.tile in e.tile.neighbors.values():
                for d in e.tile.neighbors:
                    if e.tile.neighbors[d] and e.tile.neighbors[d].holding == player:
                        e.use_capability(e.capabilities[0], d)
                        break
                continue
            # move towards player
            for i in range(2):
                empty = e.tile.get_empty_neighbors()
                d = None
                if e.tile.position[0] > player.tile.position[0] and e.tile.neighbors[Dir.NORTH] in empty:
                    d = Dir.NORTH
                elif e.tile.position[0] < player.tile.position[0] and e.tile.neighbors[Dir.SOUTH] in empty:
                    d = Dir.SOUTH
                elif e.tile.position[1] > player.tile.position[1] and e.tile.neighbors[Dir.WEST] in empty:
                    d = Dir.WEST
                elif e.tile.position[1] < player.tile.position[1] and e.tile.neighbors[Dir.EAST] in empty:
                    d = Dir.EAST
                if d:
                    print(f"{e.name} moves {d.name}")
                    e.move(d)
                else:
                    break
        
        if not player.is_alive():
            print("you lose!")
            return
                
if __name__ == "__main__":
    main()