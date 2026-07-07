class PositionEDX:
    def __init__(self, x, y, angle, counts, results_dict, metadata):
        self.x = x
        self.y = y
        self.angle = angle
        self.counts = counts

        self.metadata = metadata
        self.elements = unpack_results_dict(results_dict)



