from src.config import DEBUG, PORT, DevelopmentSettings, ProductionSettings
from src.main import create_app

if DEBUG:
    config_object = DevelopmentSettings
else:
    config_object = ProductionSettings

flask_app = create_app(config_object=config_object)
celery_app = flask_app.extensions["celery"]

if __name__ == "__main__":
    flask_app.run(port=PORT, debug=DEBUG)
