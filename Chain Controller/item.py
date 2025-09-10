import random

class Item:
    def __init__(self, width, height, segment_size):
        self.width = width
        self.height = height
        self.segment_size = segment_size
        self.respawn()

    def respawn(self):
        self.x = random.randint(0, (self.width - self.segment_size) // self.segment_size) * self.segment_size
        self.y = random.randint(0, (self.height - self.segment_size) // self.segment_size) * self.segment_size
