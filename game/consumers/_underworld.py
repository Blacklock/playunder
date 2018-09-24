import random
from math import cos, sin, floor, sqrt, pi, ceil
import json


def underworld_data(self):
    self.generate_map()
    self.send_json({
        'type': 'page_data',
        'page': 'underworld'
    })


def generate_map(self):
    """
    Generates a map of the Underworld based on a seed.
    """
    # Define map dimensions and settings

    height = 50
    width = 50

    # We would use a seed if we wanted the map to be the same every single time
    # self.random = random.Random(config['SECRET_KEY'][:8] + str(self.cult.id))

    # Create a 2-dimensional list for the game map

    field = [['_'] * width for _ in range(height)]

    # Create random points that will be the starting positions of biomes

    points = poisson_disc_samples(width, height, 3, 5)
    random.shuffle(points)

    for i in range(len(points)):
        biome = '_'

        biome = random.choice(list(biomes.keys()))  # Set a random biome

        points[i][0] = int(round(points[i][0])) - 1  # x
        points[i][1] = int(round(points[i][1])) - 1  # y
        points[i].append(biome)

        field[points[i][1]][points[i][0]] = 'X'

    # Set the biomes

    field = set_biomes(field, points)


def set_biomes(field, points):
    for row in range(len(field)):
        # For every cell, we find the closest point
        for cell in range(len(field[row])):
            # Store the currently closest point:
            shortest_dist = -1
            # Stores the biome of the current point:
            current_biome = '_'

            # Iterate over the points to find the closest one
            for point in points:
                # Calculate the euclidean distance
                xdiff = point[0] - row
                ydiff = point[1] - cell
                distance = xdiff * xdiff + ydiff * ydiff  # Square root not needed since we're only comparing

                # If this is currently the shortest distance, set it
                if distance < shortest_dist or shortest_dist == -1:
                    shortest_dist = distance
                    # Set the biome that will be chosen if a shorter distance isn't found
                    current_biome = point[2]
            # Set this cell's field from available fields in the biome
            field[row][cell] = random.choice(list(biomes[current_biome]['fields'].keys()))

    return field


def poisson_disc_samples(width, height, r, k=5, rnd=random):
    """
    "Two-dimensional Poisson Disc Sampling using Robert Bridson's algorithm."
    Modified version of https://github.com/emulbreh/bridson.
    """
    tau = 2 * pi
    cellsize = r / sqrt(2)

    grid_width = int(ceil(width / cellsize))
    grid_height = int(ceil(height / cellsize))
    grid = [None] * (grid_width * grid_height)

    def distance(a, b):
        dx = a[0] - b[0]
        dy = a[1] - b[1]
        return sqrt(dx * dx + dy * dy)

    def grid_coords(p2):
        return [int(floor(p2[0] / cellsize)), int(floor(p2[1] / cellsize))]

    def fits(p2, gx, gy):
        yrange = list(range(max(gy - 2, 0), min(gy + 3, grid_height)))

        for x in range(max(gx - 2, 0), min(gx + 3, grid_width)):
            for y in yrange:
                g = grid[x + y * grid_width]
                if g is None:
                    continue
                if distance(p2, g) <= r:
                    return False
        return True

    p = [width * rnd.random(), height * rnd.random()]
    queue = [p]
    grid_x, grid_y = grid_coords(p)
    grid[grid_x + grid_y * grid_width] = p

    while queue:
        qi = int(rnd.random() * len(queue))
        qx, qy = queue[qi]
        queue[qi] = queue[-1]
        queue.pop()

        for _ in range(k):
            alpha = tau * rnd.random()
            d = r * sqrt(3 * rnd.random() + 1)
            px = qx + d * cos(alpha)
            py = qy + d * sin(alpha)

            if not (0 <= px < width and 0 <= py < height):
                continue
            p = [px, py]
            grid_x, grid_y = grid_coords(p)

            if not fits(p, grid_x, grid_y):
                continue
            queue.append(p)
            grid[grid_x + grid_y * grid_width] = p
    return [p for p in grid if p is not None]


# Biome data (might be moved to an ignored _data.py in the future)
# TODO: Be able to set field rarity

biomes = {
    'The Obsidian Plains': {  # Biomes have different fields in them that will be randomly picked from
        'description': 'You are out in the open, and they know where you are.',
        'fields': {
            'Empty Plains': {
                'description': 'There is nothing of interest here.',
                'hostility': 60,
                'shard_rate': 10,
                'loot_rate': 1
            },
            'Mineral Plains': {
                'description': 'You can see some shards growing around in this area.',
                'hostility': 60,
                'shard_rate': 50,
                'loot_rate': 1
            }
        }
    },
    'The Limbo': {
        'description': 'You do not know where you\'re going. Stay there for too long, and the limbo will \
        take you over and you will be wandering around aimlessly for eternity just like the others.',
        'fields': {
            'Walking Grounds': {
                'description': 'Victims of The Limbo are walking aimlessly all around this place.',
                'hostility': 20,
                'shard_rate': 20,
                'loot_rate': 5
            }
        }
    }
}