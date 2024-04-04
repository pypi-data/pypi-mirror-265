from uuid import uuid4


class Line:
    def __init__(self, name, points, color=None):
        if not name:
            raise Exception("Name must be provided to create a line")

        self.name = name
        self.points = points
        self.color = color

    def extend(self, point):
        self.points.append(point)

    def to_json(self):
        return {
            "id": self.name,
            "name": self.name,
            "points": [point for point in self.points],
            "color": self.color,
        }


class Marker:
    def __init__(self, location, name=None):
        if name is None:
            name = str(uuid4())

        self.name = name
        self.location = location

    def to_json(self):
        return {"id": self.name, "name": self.name, "latlng": self.location}


class Map:
    def __init__(self):
        self.lines = []
        self.markers = []

    def add_line(self, line):
        self.lines.append(line)

    def get_line(self, name) -> Line:
        for line in self.lines:
            if line.name == name:
                return line

        raise Exception(f"No such line: {name}")

    def add_marker(self, marker) -> Marker:
        if isinstance(marker, dict):
            new_marker = Marker(marker["latlng"], marker.get("name"))
            self.markers.append(new_marker)
            return new_marker
        else:
            raise Exception("Can parse this marker", marker)

    def get_marker(self, marker_id) -> Marker:
        for marker in self.markers:
            if marker.name == marker_id:
                return marker

        raise Exception(f"No such marker: {marker_id}")

    def to_json(self):
        return {
            "lines": [line.to_json() for line in self.lines],
            "markers": [marker.to_json() for marker in self.markers],
        }
