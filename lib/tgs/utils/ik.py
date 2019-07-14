from .nvector import NVector


def reach(head, tail, target, length=None):
    if length is None:
        length = (tail - head).length

    # calculate the stretched length
    s = tail - target

    # calculate how much to scale the stretched line
    scale = length / s.length

    return [
        # copy the target for the new head
        target.clone(),
        # scale the new tail based on distance from target
        target + s * scale
    ]


# http://sean.cm/a/fabrik-algorithm-2d
class Chain:
    def __init__(self, tail, fixed_tail=True):
        self.segments = [tail.clone()]
        self.fixed_tail = fixed_tail

    def add_point(self, point):
        self.segments.append(point.clone())

    def reach(self, target):
        base = self.segments[0]

        for i in range(len(self.segments)-1, 0, -1):
            head, tail = reach(self.segments[i], self.segments[i - 1], target)
            self.segments[i] = head
            target = tail
        self.segments[0] = target

        if self.fixed_tail:
            # at this point, our base has moved from its original
            # location... so perform the iterative reach in reverse,
            # with the target set to the initial base location
            target = base

            for i in range(len(self.segments)-1):
                head, tail = reach(self.segments[i], self.segments[i + 1], target)
                self.segments[i] = head
                target = tail
            self.segments[-1] = target

    def __reach(self, target):
        base = self.segments[-1]

        for i in range(len(self.segments)-1):
            head, tail = reach(self.segments[i], self.segments[i + 1], target)
            self.segments[i] = head
            target = tail
        self.segments[-1] = target

        if self.fixed_tail:
            # at this point, our base has moved from its original
            # location... so perform the iterative reach in reverse,
            # with the target set to the initial base location
            target = base

            for i in range(len(self.segments)-1, 0, -1):
                head, tail = reach(self.segments[i], self.segments[i - 1], target)
                self.segments[i] = head
                target = tail
            self.segments[0] = target
