from src import app
from src.config import PORT


if __name__ == '__main__':
    # src.run(host='0.0.0.0', port=PORT)
    app.run(debug=True)
