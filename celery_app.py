from celery import Celery
from flask import Flask

def create_flask_app():
    app = Flask(__name__)
    app.config['broker_url'] = 'redis://127.0.0.1:6379/0'
    app.config['result_backend'] = 'redis://127.0.0.1:6379/0'
    return app

flask_app = create_flask_app()

def make_celery(app):
    celery = Celery(
        app.import_name,
        backend=app.config['result_backend'],
        broker=app.config['broker_url']
    )
    celery.conf.update(app.config)
    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)
    celery.Task = ContextTask
    return celery

celery = make_celery(flask_app)
