import json
import logging
import os
import uuid
from datetime import datetime, timezone
from decimal import Decimal

from src.utils.dynamodb import get_table
from src.utils.response import api_response, error_response

logger = logging.getLogger()
logger.setLevel(os.environ.get("LOG_LEVEL", "INFO"))

table = get_table()


def lambda_handler(event, context):
    try:
        body = json.loads(event.get("body", "{}"), parse_float=Decimal)

        if "name" not in body:
            return error_response(400, "name is required")

        now = datetime.now(timezone.utc).isoformat()
        item = {
            "id": str(uuid.uuid4()),
            "name": body["name"],
            "description": body.get("description", ""),
            "price": body.get("price", 0),
            "created_at": now,
            "updated_at": now
        }

        table.put_item(Item=item)
        logger.info("Created item: %s", item["id"])
        return api_response(201, {"item": item})
    except json.JSONDecodeError:
        return error_response(400, "Invalid JSON body")
    except Exception as exc:
        return error_response(500, str(exc))

