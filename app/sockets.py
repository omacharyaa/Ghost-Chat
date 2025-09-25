from __future__ import annotations

from flask import session, request
from flask_socketio import emit, join_room, leave_room

from .extensions import socketio

# room_name -> set of session IDs
_presence = {}


@socketio.on("connect")
def handle_connect():
	emit("status", {"message": "connected"})


def _compose_room(region: str | None, room: str | None, code: str | None) -> str | None:
	if code:
		return f"GROUP:{code}"
	if region and room:
		return f"{region}:{room}"
	return None


def _update_presence(room_name: str, sid: str, joining: bool) -> int:
	room_set = _presence.setdefault(room_name, set())
	if joining:
		room_set.add(sid)
	else:
		room_set.discard(sid)
	return len(room_set)


@socketio.on("join")
def handle_join(data):
	room = data.get("room")
	region = data.get("region")
	code = data.get("code")
	nickname = data.get("nickname") or session.get("nickname") or "Ghost"
	room_name = _compose_room(region, room, code)
	if room_name:
		join_room(room_name)
		count = _update_presence(room_name, request.sid, True)
		emit("status", {"message": f"{nickname} joined"}, to=room_name)
		emit("presence", {"room": room_name, "count": count}, to=room_name)


@socketio.on("leave")
def handle_leave(data):
	room = data.get("room")
	region = data.get("region")
	code = data.get("code")
	room_name = _compose_room(region, room, code)
	if room_name:
		leave_room(room_name)
		count = _update_presence(room_name, request.sid, False)
		emit("presence", {"room": room_name, "count": count}, to=room_name)


@socketio.on("disconnect")
def handle_disconnect():
	# Remove this sid from all rooms it was in
	sid = request.sid
	for room_name, sids in list(_presence.items()):
		if sid in sids:
			sids.discard(sid)
			emit("presence", {"room": room_name, "count": len(sids)}, to=room_name)


@socketio.on("typing")
def handle_typing(data):
	room = data.get("room")
	region = data.get("region")
	code = data.get("code")
	nickname = data.get("nickname") or session.get("nickname") or "Ghost"
	room_name = _compose_room(region, room, code)
	if room_name:
		emit("typing", {"nickname": nickname}, to=room_name, include_self=False)


@socketio.on("message")
def handle_message(data):
	room = data.get("room")
	region = data.get("region")
	code = data.get("code")
	text = data.get("text")
	nickname = data.get("nickname") or session.get("nickname") or "Ghost"
	room_name = _compose_room(region, room, code)
	if room_name and text:
		emit("message", {"nickname": nickname, "text": text}, to=room_name)
