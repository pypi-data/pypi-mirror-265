from typing import Optional
import logging
from flask import Flask, render_template, redirect, request, jsonify
from flask_socketio import SocketIO, emit, join_room
from uuid import uuid4

from livemap.map import Map, Line

app = Flask(__name__, template_folder="templates", static_folder="static")
socketio = SocketIO(app)
map_state = Map()
room = "default"
room_members = []

logger = logging.getLogger(__name__)


@socketio.on("connect")
def connect():
    sid = request.sid
    print("connect", sid)
    join_room(room, sid)
    room_members.append(sid)
    socketio.emit("MAP_STATE", map_state.to_json(), to=sid)


@socketio.on("disconnect")
def disconnect():
    print("disconnect")
    sid = request.sid
    room_members.remove(sid)


@socketio.on("ADD_MARKER")
def add_marker(data):
    marker = data.get("marker")

    new_marker = map_state.add_marker(marker)
    logger.info(f"add marker at {new_marker.location}")
    emit("ADD_MARKER", new_marker.to_json(), to=room)


@socketio.on("MOVE_MARKER")
def move_marker(data):
    sid = request.sid

    marker_id = data.get("markerId")
    if not marker_id:
        app.logger.error("Invalid marker ID", marker_id)
        return

    marker = map_state.get_marker(marker_id)
    marker.location = data.get("location")
    logger.info(f"Move marker {marker_id} to {marker.location}")
    emit("MOVE_MARKER", marker.to_json(), to=room)


@app.route("/")
def home():
    return render_template("map.html")


@app.route("/polylines", methods=["POST"])
def post_polyline():
    data = request.json

    new_line = Line(**data)
    map_state.add_line(new_line)
    socketio.emit("POLYLINE_ADD", data, to=room)

    return jsonify(new_line.to_json())


@app.route("/polylines/<id>/points", methods=["POST"])
def post_path_point(id):
    data = request.json
    data["name"] = id

    line = map_state.get_line(id)
    new_point = (data["latitude"], data["longitude"])
    line.extend(new_point)

    socketio.emit("POLYLINE_EXTEND", data, to=room)

    return data, 200


def run_server(port, debug=False):
    socketio.run(app, port=port, debug=debug, log_output=True)
