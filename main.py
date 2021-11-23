from app.app import app
import os

if __name__ == "__main__":
    app.run(
        host='0.0.0.0',
        port=int(os.environ.get('PORT', 6768)),
        workers=int(os.environ.get('WEB_CONCURRENCY', 1)),
        debug=bool(os.environ.get('DEBUG', ''))
    )
