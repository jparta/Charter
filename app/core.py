from .config import Config
from app.sp_helpers import Flask
from app.controller import views, tasks, cache
from app.controller.api import api
from .db import db
import logging

def create_app(debug=False):
    return entrypoint(debug=debug, mode='app')

def create_celery(debug=False):
    return entrypoint(debug=debug, mode='celery')

def entrypoint(debug=False, mode='app'):
    app = Flask(__name__, instance_relative_config=True)
    app.configure(
        JWT_ALGORITHMS=['HS256'],
        APPS = [],
        USE_CDN=(app.env == 'production'),
    ) 
    app.config.from_envvar('APP_SETTINGS')
    app.config.from_object(Config)
    if app.config.get('BEHIND_PROXY', False):
        from werkzeug.contrib.fixers import ProxyFix
        app.config.setdefault('MIDDLEWARE', []).insert(0, ProxyFix)
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    with app.app_context():
        app.register_blueprint('app.views')
    app.load_apps()
    app.wrap_middleware()
    app.finalize_create()

    app.logger.setLevel(logging.DEBUG)

    configure_celery(app, tasks.celery)
    api.token = app.config.get('API_TOKEN')
    api.set_base_url_from(app.config.get('API_BASE_URL'))
    cache.cache.init_app(app)
    db.init_app(app)

    if mode=='app':
        return app
    elif mode=='celery':
        return tasks.celery


def configure_celery(app, celery):
    # set broker url and result backend from app config
    celery.conf.broker_url = app.config['CELERY_BROKER_URL']
    celery.conf.result_backend = app.config['CELERY_RESULT_BACKEND']

    # subclass task base for app context
    # http://flask.pocoo.org/docs/0.12/patterns/celery/
    TaskBase = celery.Task
    class AppContextTask(TaskBase):
        abstract = True
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)
    celery.Task = AppContextTask

    # run finalize to process decorated tasks
    celery.finalize()

