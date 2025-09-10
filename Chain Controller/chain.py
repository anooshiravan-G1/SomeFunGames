class Segment:
    def __init__(self, x, y):
        self.x = x
        self.y = y


class Chain:
    def __init__(self, width, height, segment_size):
        self.width = width
        self.height = height
        self.segment_size = segment_size
        self.segments = [Segment(width // 2, height // 2)]
        self.direction = (0, 0)

    def move(self):
        if self.direction != (0, 0):
            new_x = self.segments[0].x + self.direction[0] * self.segment_size
            new_y = self.segments[0].y + self.direction[1] * self.segment_size
            self.segments.insert(0, Segment(new_x, new_y))
            self.segments.pop()

    def grow(self):
        last_segment = self.segments[-1]
        self.segments.append(Segment(last_segment.x, last_segment.y))

    def set_direction(self, direction):
        self.direction = direction

    def check_collision(self):
        # Check collision with self
        head = self.segments[0]
        for segment in self.segments[1:]:
            if len(self.segments) > 2 and head.x == segment.x and head.y == segment.y:
                return True
        # Check collision with boundaries
        if head.x < 0 or head.x >= self.width or head.y < 0 or head.y >= self.height:
            return True
        return False
