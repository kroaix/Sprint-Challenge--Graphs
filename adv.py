from room import Room
from player import Player
from world import World

import random
from ast import literal_eval

# Load world
world = World()


# You may uncomment the smaller graphs for development and testing purposes.
# map_file = "maps/test_line.txt"
# map_file = "maps/test_cross.txt"
# map_file = "maps/test_loop.txt"
# map_file = "maps/test_loop_fork.txt"
map_file = "maps/main_maze.txt"

# Loads the map into a dictionary
room_graph=literal_eval(open(map_file, "r").read())
world.load_graph(room_graph)

# Print an ASCII map
world.print_rooms()

player = Player(world.starting_room)

# Fill this out with directions to walk
# traversal_path = ['n', 'n']
traversal_path = []
#path for going backwards to find unvisited rooms
backward_path = []
#keeping track of visited rooms
visited = set()
#we'll need to backtrack to go to previously visited room that still has moves available
opposite_directions = {'n': 's', 's': 'n', 'e': 'w', 'w': 'e'}

#while there are still unvisited rooms
while len(visited) < len(room_graph):
    #temp variable to initialize the next room
    next_room = None
    #current room's neighbors or "exits"
    directions = player.current_room.get_exits()
    #for each neighbor in neighbors
    for direction in directions:
        #if not in visited, this will be our next room
        if player.current_room.get_room_in_direction(direction) not in visited:
            next_room = direction

    if next_room is not None:
        traversal_path.append(next_room)
        backward_path.append(opposite_directions[next_room])
        #player will move to the next room
        player.travel(next_room)
        #add to visited
        visited.add(player.current_room)
    
    else: #move backwards so we can find a room with an unviisted neighbor
        #popping last item
        next_room = backward_path.pop()
        #add that to the path
        traversal_path.append(next_room)
        #move there
        player.travel(next_room)


# TRAVERSAL TEST - DO NOT MODIFY
visited_rooms = set()
player.current_room = world.starting_room
visited_rooms.add(player.current_room)

for move in traversal_path:
    player.travel(move)
    visited_rooms.add(player.current_room)

if len(visited_rooms) == len(room_graph):
    print(f"TESTS PASSED: {len(traversal_path)} moves, {len(visited_rooms)} rooms visited")
else:
    print("TESTS FAILED: INCOMPLETE TRAVERSAL")
    print(f"{len(room_graph) - len(visited_rooms)} unvisited rooms")



#######
# UNCOMMENT TO WALK AROUND
#######
player.current_room.print_room_description(player)
while True:
    cmds = input("-> ").lower().split(" ")
    if cmds[0] in ["n", "s", "e", "w"]:
        player.travel(cmds[0], True)
    elif cmds[0] == "q":
        break
    else:
        print("I did not understand that command.")
