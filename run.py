import os

from app import create_app
from lib.config import config

app = create_app()

if __name__ == "__main__":
    app.run(
        host=os.getenv("HOST", "localhost"),
        port=int(config.PORT or 3000),
    )
