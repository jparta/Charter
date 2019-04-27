from celery import Celery
from .api import api
from flask import current_app as app
from pprint import pformat

celery = Celery('charter', autofinalize=True)

@celery.task(bind=True)
def save_submission(self, submission_id):
    submission_data = api.load_data('{SUBMISSIONS_URL}{submission_id}'
                                .format(submission_id=submission_id, **app.config))
    app.logger.debug(pformat(list(submission_data.get('submission_data'))))

