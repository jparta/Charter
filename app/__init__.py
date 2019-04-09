import os

from sp_helpers import Flask

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.configure(
        test_config=test_config,
        JWT_ALGORITHMS=['HS256'],
        APPS = [],
        MIDDLEWARE=[],
        BEHIND_PROXY=False,
        USE_CDN=(app.env == 'production'),
    )
    if app.config.get('BEHIND_PROXY', False):
        from werkzeug.contrib.fixers import ProxyFix
        app.config.setdefault('MIDDLEWARE', []).insert(0, ProxyFix)
    #app.register_blueprint('')
    app.load_apps()
    app.wrap_middleware()
    app.finalize_create()

    @app.route('/api/v1/')
    def hello():
        return 'Hello, World!'

    return app
