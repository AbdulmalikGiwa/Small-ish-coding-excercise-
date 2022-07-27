import ast
import enum
import json

import requests
from celery import Celery

from .config import Config

app = Celery(__name__)
app.conf.broker_url = Config.BROKER_URL
app.conf.result_backend = Config.CELERY_RESULT_BACKEND


class MLServerResponse(enum.Enum):
    true = 1
    false = 2
    unavailable = 3


@app.task(
    name="check_foul_language",
    retry_backoff=True,
)
def check_foul_language(paragraphs: list, post_id: int):
    # Request to dummy ML service predicting if any sentence contains offensive words.
    # Offsetting this to celery so it can be executed concurrently in background.
    ml_service = Config.ML_API
    for paragraph in paragraphs:
        json_data = ast.literal_eval(json.dumps({"fragment": paragraph}))
        try:
            r = requests.post(url=ml_service, json=json_data)
        except Exception:
            return MLServerResponse.unavailable.value
        if r.status_code == 200:
            data = r.json()
            if data.get("hasFoulLanguage"):
                return MLServerResponse.true.value
        else:
            return MLServerResponse.unavailable.value
    return MLServerResponse.false.value
