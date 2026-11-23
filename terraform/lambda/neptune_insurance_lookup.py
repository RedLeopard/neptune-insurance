"""Neptune Insurance: read-only lookup of synthetic policy and claim records.

The demonstration customer ID is server-controlled configuration, not real
customer authentication. Replace it with a trusted authenticated identity before
using this handler with actual customer records.
"""

import json
import os
import re
import time

import boto3
from botocore.config import Config


TABLE = boto3.resource(
    "dynamodb",
    config=Config(
        connect_timeout=1,
        read_timeout=1,
        retries={"max_attempts": 0},
    ),
).Table(os.environ.get("TABLE_NAME", "NeptuneInsuranceLab"))

PREFIXES = {"policy": "POL", "claim": "CLM"}
ALLOWED_STATUSES = {
    "policy": {"ACTIVE", "LAPSED"},
    "claim": {"RECEIVED", "IN_REVIEW", "CLOSED"},
}


def lambda_handler(event, context):
    """Validate a Connect request and return a flat, sanitized String map."""
    request_id = context.aws_request_id

    def respond(code, reference="", status="", product=""):
        print(json.dumps({"requestId": request_id, "resultCode": code}))
        return {
            "resultCode": code,
            "reference": reference,
            "status": status,
            "product": product,
            "requestId": request_id,
        }

    if not isinstance(event, dict):
        return respond("MALFORMED")

    details = event.get("Details")
    if not isinstance(details, dict):
        return respond("MALFORMED")

    parameters = details.get("Parameters")
    if not isinstance(parameters, dict):
        return respond("MALFORMED")

    if set(parameters) != {"recordType", "reference"}:
        return respond("MALFORMED")

    record_type = parameters["recordType"]
    reference = parameters["reference"]
    if not isinstance(record_type, str) or record_type not in PREFIXES:
        return respond("MALFORMED")

    if not isinstance(reference, str) or not re.fullmatch(
        PREFIXES[record_type] + r"-[0-9]{4}", reference
    ):
        return respond("MALFORMED")

    # Only administrator configuration can introduce the bounded test delay.
    try:
        delay = float(os.environ.get("LOOKUP_DELAY_SECONDS", "0"))
        if not 0 <= delay <= 3:
            return respond("UNAVAILABLE")
    except ValueError:
        return respond("UNAVAILABLE")
    time.sleep(delay)

    # A fixed synthetic principal makes ownership behavior testable.
    # Never accept a customer identity chosen by the conversation or model.
    customer_id = os.environ.get("DEMO_CUSTOMER_ID", "")
    if customer_id != "DEMO-1001":
        return respond("UNAUTHORIZED")

    try:
        item = TABLE.get_item(
            Key={"pk": record_type.upper() + "#" + reference},
            ConsistentRead=True,
        ).get("Item")
    except Exception as error:
        print(json.dumps({
            "requestId": request_id,
            "backendErrorType": type(error).__name__,
        }))
        return respond("UNAVAILABLE")

    if not item:
        return respond("NOT_FOUND")

    if item.get("ownerId") != customer_id:
        return respond("UNAUTHORIZED")

    # Validate stored values as well as request inputs.
    status = item.get("status")
    if (
        not isinstance(status, str)
        or status not in ALLOWED_STATUSES[record_type]
        or item.get("product") != "AUTO"
    ):
        return respond("UNAVAILABLE")

    # Build an explicit response; internalNotes and ownerId stay in the backend.
    return respond("OK", reference, status, item["product"])
