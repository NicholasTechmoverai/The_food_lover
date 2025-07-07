import socketio

# Create a custom namespace
class MainNamespace(socketio.AsyncNamespace):
    def on_connect(self, sid, environ):
        print(f"[Main] Connected: {sid}")

    def on_disconnect(self, sid):
        print(f"[Main] Disconnected: {sid}")

    async def on_join(self, sid, data):
        print(f"[Main] {sid} joined: {data}")
        await self.emit('message', {'msg': f"{sid} joined the main room"}, room=sid)

    async def on_message(self, sid, data):
        print(f"[Main] Message from {sid}: {data}")
        await self.emit('message', {'msg': f"You said: {data}"}, room=sid)
