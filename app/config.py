import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config():
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    BEHIND_PROXY = True
    BASE_URL = 'http://172.20.0.3:8000/api/v2/'
    SUBMISSIONS_URL = '/submissions/' 
    SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']
    CELERY_BROKER_URL='amqp://admin:admin@localhost:5672/vhost'
    CELERY_RESULT_BACKEND='amqp://guest@localhost//'
                


class ProductionConfig(Config):
    DEBUG = False


class StagingConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class TestingConfig(Config):
    TESTING = True
