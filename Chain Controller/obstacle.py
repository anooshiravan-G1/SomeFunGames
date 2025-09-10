import random

class Obstacle:
    def __init__(self, width, height, segment_size):
        self.x = random.randint(0, (width - segment_size) // segment_size) * segment_size
        self.y = random.randint(0, (height - segment_size) // segment_size) * segment_size
