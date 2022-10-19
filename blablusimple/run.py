import os
from main import create_app
from api.config.config import ProductionConfig, DevelopmentConfig, \
    TestingConfig


app_config = None
if os.environ.get('WORK_ENV') == 'PROD':
    app_config = ProductionConfig
elif os.environ.get('WORK_ENV') == 'TEST':
    app_config = TestingConfig
else:
    app_config = DevelopmentConfig


if __name__ == "__main__":
    app = create_app(app_config)
    app.run()
