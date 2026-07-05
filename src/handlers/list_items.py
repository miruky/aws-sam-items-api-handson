import logging
import os

from src.utils.dynamodb import get_table
from src.utils.response import api_response, error_response

logger = logging.getLogger()
logger.setLevel(os.environ.get("LOG_LEVEL", "INFO"))

table = get_table()


def lambda_handler(event, context):
    try:
        response = table.scan()
        items = response.get("Items", [])
        logger.info("Retrieved %s items", len(items))
        return api_response(200, {"items": items, "count": len(items)})
    except Exception as exc:
        return error_response(500, str(exc))

