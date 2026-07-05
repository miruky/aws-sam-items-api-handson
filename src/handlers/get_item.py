import logging
import os

from src.utils.dynamodb import get_table
from src.utils.response import api_response, error_response

logger = logging.getLogger()
logger.setLevel(os.environ.get("LOG_LEVEL", "INFO"))

table = get_table()


def lambda_handler(event, context):
    try:
        item_id = (event.get("pathParameters") or {})["id"]
        response = table.get_item(Key={"id": item_id})
        item = response.get("Item")

        if not item:
            return error_response(404, f"Item {item_id} not found")

        logger.info("Retrieved item: %s", item_id)
        return api_response(200, {"item": item})
    except Exception as exc:
        return error_response(500, str(exc))

