

import click
import geojson 
import uuid

@click.group()
def cli():
    pass

@cli.command()
@click.option("--port", "-p", default=5689)
@click.option("--debug", is_flag=True)
def server(port, debug):
    from livemap.server import run_server
    run_server(port=port, debug=debug)


@cli.command()
@click.option("--port", "-p", default=5689)
@click.option("--host", "-h", default="127.0.0.1")
@click.option("--color", "-c", default=None, help="Set the color of the line, e.g. 'red, 'blue', 'green'")
@click.argument("file")
def load_file(port, host, file, color):
    from livemap.client import Map, Polyline

    map = Map(f"http://{host}:{port}")
    data = geojson.load(open(file))

    for feature in data.features:
        if feature.geometry.type == "LineString":
            points = [[lng, lat] for (lat, lng) in feature.geometry.coordinates]
            map.polyline(str(uuid.uuid4()), points, color=color)
        else:
            print(f"{feature.geometry.type} not supported yet")

if __name__ == '__main__':
    cli()