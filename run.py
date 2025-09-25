from __future__ import annotations

import os
from app import create_app
from app.extensions import socketio


app = create_app()


if __name__ == "__main__":
	# Bind to 0.0.0.0 and honor PORT for Render
	port = int(os.getenv("PORT", "5000"))
	print(f"Ghost Chat starting... Open http://localhost:{port} in your browser.")
	socketio.run(app, host="0.0.0.0", port=port)
