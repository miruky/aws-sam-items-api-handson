import json
import logging

logger = logging.getLogger()


def api_response(status_code: int, body: dict) -> dict:
    return {
        "statusCode": status_code,
        "headers": {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "GET,POST,PUT,DELETE,OPTIONS"
        },
        "body": json.dumps(body, ensure_ascii=False, default=str)
    }


def error_response(status_code: int, message: str) -> dict:
    logger.error("Error %s: %s", status_code, message)
    return api_response(status_code, {"error": message})

