from celery import Celery
from .api import api
from flask import current_app as app
from pprint import pformat
from celery.utils.log import get_task_logger

logger = get_task_logger(__name__)
celery = Celery('charter', autofinalize=True)

@celery.task(bind=True)
def save_submission(self, submission_id):
    logger.info("api_token from task-yes: %s", api.token)
    submission_data = api.load_data('{SUBMISSIONS_URL}{submission_id}'
                                .format(submission_id=submission_id, **app.config))
    logger.info(pformat(list(submission_data.get('submission_data'))))

