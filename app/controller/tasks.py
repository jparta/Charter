from celery import Celery
from .api import api
from ..db import db
from flask import current_app as app
from pprint import pformat
from celery.utils.log import get_task_logger
from ..models import Submission

logger = get_task_logger(__name__)
celery = Celery('charter', autofinalize=True)


@celery.task(bind=True)
def save_submission(self, submission_id):
    #logger.info("api_token from task: %s", api.token)
    submission_from_api = api.load_data('{SUBMISSIONS_URL}{submission_id}'
                                        .format(submission_id=submission_id, **app.config))
    formkeyval = dict(submission_from_api.get_item('submission_data'))
    logger.info(pformat(formkeyval))
    submission_to_db = Submission(
    	id=submission_from_api.get('id'),
    	grade=submission_from_api.get('grade'),
    	minutes_reported=formkeyval.get('timespent'),
	    has_beginner=None	
    )
    db.session.add(submission_to_db)
    db.session.commit() 
