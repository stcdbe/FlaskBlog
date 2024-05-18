from src.config import DevelopmentSettings, ProductionSettings, env
from src.main import create_app

match env.DEBUG:
    case True:
        config_obj = DevelopmentSettings
    case False:
        config_obj = ProductionSettings

flask_app = create_app(config_object=config_obj)
celery_app = flask_app.extensions["celery"]

if __name__ == "__main__":
    flask_app.run(port=env.PORT, debug=env.DEBUG)
