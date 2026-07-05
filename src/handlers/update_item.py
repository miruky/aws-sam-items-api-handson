import json
import logging
import os
from datetime import datetime, timezone
from decimal import Decimal

from src.utils.dynamodb import get_table
from src.utils.response import api_response, error_response

logger = logging.getLogger()
logger.setLevel(os.environ.get("LOG_LEVEL", "INFO"))

table = get_table()


def lambda_handler(event, context):
    try:
        item_id = (event.get("pathParameters") or {})["id"]
        body = json.loads(event.get("body", "{}"), parse_float=Decimal)

        existing = table.get_item(Key={"id": item_id})
        if "Item" not in existing:
            return error_response(404, f"Item {item_id} not found")

        update_parts = []
        expression_values = {}
        expression_names = {}

        for key in ["name", "description", "price"]:
            if key in body:
                update_parts.append(f"#{key} = :{key}")
                expression_values[f":{key}"] = body[key]
                expression_names[f"#{key}"] = key

        update_parts.append("#updated_at = :updated_at")
        expression_values[":updated_at"] = datetime.now(timezone.utc).isoformat()
        expression_names["#updated_at"] = "updated_at"

        response = table.update_item(
            Key={"id": item_id},
            UpdateExpression="SET " + ", ".join(update_parts),
            ExpressionAttributeValues=expression_values,
            ExpressionAttributeNames=expression_names,
            ReturnValues="ALL_NEW"
        )

        logger.info("Updated item: %s", item_id)
        return api_response(200, {"item": response["Attributes"]})
    except json.JSONDecodeError:
        return error_response(400, "Invalid JSON body")
    except Exception as exc:
        return error_response(500, str(exc))

