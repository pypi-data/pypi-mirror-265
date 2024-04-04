from __future__ import annotations
import time
import requests


class Polyline:
    def __init__(self, map, name, points, **kwargs):
        self.map = map
        self.name = name
        self.points = points

    def extend(self, points):
        if type(points[0]) is float:
            points = [points]

        for point in points:
            response = requests.post(
                f"{self.map.url}/polylines/{self.name}/points",
                json={"latitude": point[0], "longitude": point[1]},
            )
            if not response.ok:
                print(response.reason)
                raise Exception(response.reason)


class Map:
    def __init__(self, url):
        self.url = url

    def polyline(self, name, points, color=None):
        line_data = {"name": name, "points": points}
        if color is not None:
            line_data["color"] = color

        response = requests.post(f"{self.url}/polylines", json=line_data)
        if not response.ok:
            raise Exception(response.reason)
        data = response.json()
        return Polyline(self, **data)
