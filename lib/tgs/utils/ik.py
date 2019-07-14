from .nvector import NVector


# FABRIK
class Chain:
    def __init__(self, tail, fixed_tail=True, tolerance=0.5, max_iter=8):
        self.segments = [tail.clone()]
        self.fixed_tail = fixed_tail
        self.lengths = []
        self.total_length = 0
        self.tolerance = tolerance
        self.max_iter = max_iter

    def add_point(self, point):
        length = (point - self.segments[-1]).length
        self.lengths.append(length)
        self.total_length += length
        self.segments.append(point.clone())

    def backward(self, target):
        """
        target -> -> start
        """
        self.segments[-1] = target
        for i in range(len(self.segments)-2, -1, -1):
            r = self.segments[i+1] - self.segments[i]
            l = self.lengths[i] / r.length
            self.segments[i] = self.segments[i+1].lerp(self.segments[i], l)

    def forward(self, target):
        """
        start -> -> tail
        """
        self.segments[0] = target
        for i in range(0, len(self.segments)-1):
            r = self.segments[i+1] - self.segments[i]
            l = self.lengths[i] / r.length
            self.segments[i+1] = self.segments[i].lerp(self.segments[i+1], l)

    def reach(self, target):
        if not self.fixed_tail:
            self.backward(target)
            return

        distance = (target - self.segments[0]).length
        if distance >= self.total_length:
            for i in range(len(self.segments)-1):
                r = target - self.segments[i]
                l = self.lengths[i] / r.length
                self.segments[i+1] = self.segments[i].lerp(target, l)
            return

        base = self.segments[0]

        distance = (target - self.segments[-1]).length
        n_it = 0
        while distance > self.tolerance and n_it < self.max_iter:
            self.backward(target)
            self.forward(base)
            distance = (target - self.segments[-1]).length
            n_it += 1
