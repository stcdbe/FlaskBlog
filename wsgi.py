from src.config.enviroment import env
from src.config.settings import DevelopmentSettings, ProductionSettings
from src.main import create_app

match env.DEBUG:
    case True:
        config_obj = DevelopmentSettings
    case _:
        config_obj = ProductionSettings

app = create_app(config_object=config_obj)
celery_app = app.extensions["celery"]

if __name__ == "__main__":
    app.run(host=env.HOST, port=env.PORT, debug=env.DEBUG)
