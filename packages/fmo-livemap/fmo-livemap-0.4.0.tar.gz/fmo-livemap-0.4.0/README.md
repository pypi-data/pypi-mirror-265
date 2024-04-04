# Draw a on a map in real-time

Install the library
```bash
pip install fmo-livemap
```

Run the server
```bash
livemap server
```
You can view the map in your browser at `localhost:5689`.


## Draw a line with a script

This simple script will connect to the map, create a new line and update it every 2 seconds
```python
gps_data = [
  [38.91168232416608, -76.47992628575723,],
  [38.91167723745552, -76.47998040159345],
  [38.911660346950676, -76.48003362018159],  
  [38.91163193259245, -76.48008505529343],
  [38.91159245603817, -76.48013384887776],
  [38.91154255338108, -76.4801791845924],
  [38.91148818673626, -76.48022588905636],
  [38.91142387753969, -76.48026912019613],
  [38.91135045470874, -76.48030791267406],
  [38.911268963041756, -76.48034139145376],
  [38.91118060039576, -76.48036874891672],
  [38.9110867003822, -76.48038926174374],
  [38.91098871241652, -76.48040230666497],
  [38.9108881794186, -76.48040737474784],
  [38.91078671350825, -76.48040408391331],
  [38.910685970081836, -76.48039218939842],
  [38.9105876206919, -76.48037159191706],
  [38.91049332518039, -76.48034234331065],
  [38.91040470353717, -76.48030464952399],
  [38.9103233079686, -76.48025887079041],
  [38.91025059566554, -76.48020551896194],
]

import time
from livemap.client import Map

# Setup a connection to the map server
map = Map("http://127.0.0.1:5689")

# Create an empty line
my_line = map.polyline("myline", [])

# Extend the line with new coordinates over time
for p in gps_data:
    my_line.extend(p)
    time.sleep(2)
```

You can change the color of the line: `map.polyline("myline", [], color='red')`

## Load a geojson file

When the server is running, use the cli to load a file
```bash
livemap load-file mydata.json
```

This assumes the server is running at `http://127.0.0.1:5689`, but you can override it

```bash
livemap load-file -h 127.0.0.1 -p 5555 mydata.json
```

You can change the color of the line
```bash
livemap load-file mydata.json --color red
```

This is a sample geojson file that works with the `load-file` command:
```json
{
  "type": "FeatureCollection",
  "features": [
    {
      "type": "Feature",
      "properties": {},
      "geometry": {
        "type": "LineString",
        "coordinates": [
          [
            -75.7949705,
            38.0574904
          ],
          [
            -75.7950745,
            38.0572349
          ],
          [
            -75.7951317,
            38.0572322
          ]
        ]
      }
    }
  ]
}
```