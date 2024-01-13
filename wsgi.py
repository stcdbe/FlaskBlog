from src import create_app
from src.config import PORT, ProductionSettings

app = create_app(config_object=ProductionSettings)
celery_app = app.extensions['celery']

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=PORT)
